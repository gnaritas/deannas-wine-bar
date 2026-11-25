// Deanna's Wine Bar & Bert's Pig Shop — static host + contact-form relay (Railway)
// websites lane build 2026-11-25 (t_5c0aaeee). Relay = Brevo HTTP API over 443 ONLY
// (SMTP egress dead on Railway, field-proof t_41f1d177). htmlContent/textContent keys
// required by Brevo v3 (400 missing_parameter on legacy keys, tavern 2026-11-16).
// Fallback copy on 502 stays shop-identity-only — no mailbox, no builder token.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const PUB = path.join(__dirname, "public");
const SITE = "Deanna's Wine Bar & Bert's Pig Shop";
const SITE_ORIGIN = "https://deannas-wine-bar-demo.up.railway.app";
const LANE_INBOX = "jarvis+websites@onsmalltalk.com"; // internal envelope address only
const BREVO_KEY = process.env.BREVO_API_KEY || "";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".gif": "image/gif",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".ico": "image/x-icon",
};

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function thanksPage(err) {
  const note = err
    ? "<p>Something went wrong on our side and your message did not go through. Please try again in a minute.</p>"
    : "<p>Your message is on its way to the shop. When the opening day is set, this list hears it first.</p>";
  return [
    "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">",
    "<meta name=\"robots\" content=\"noindex, nofollow\">",
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
    "<title>You're on the list — " + SITE + "</title>",
    "<meta name=\"description\" content=\"Message received — Deanna's Wine Bar and Bert's Pig Shop will email you first when the doors open on Wappoo Road, Charleston SC.\">",
    "<link rel=\"canonical\" href=\"" + SITE_ORIGIN + "/thanks\">",
    "<link rel=\"icon\" href=\"/favicon.svg\" type=\"image/svg+xml\">",
    "<link rel=\"stylesheet\" href=\"/style.css\">",
    "</head><body><div class=\"topline\" aria-hidden=\"true\"></div>",
    "<main id=\"main\" style=\"max-width:1060px;margin:0 auto;padding:3rem 1.5rem\"><article class=\"page\">",
    "<p class=\"lab mono\">Received</p><h1>You're on the list</h1>",
    note,
    "<p class=\"cta-row\"><a class=\"btn\" href=\"/\">Back to the site</a></p>",
    "</article></main></body></html>",
  ].join("");
}

async function relayContact(fields) {
  const name = esc(fields.name || "no name");
  const email = esc(fields.email || "none given");
  const phone = esc(fields.phone || "");
  const msg = esc((fields.message || "").slice(0, 4000));
  if (!BREVO_KEY) return { ok: false, why: "no-key" };
  const text = [
    "New opening-day message from " + SITE + " demo",
    "Name: " + (fields.name || "no name"),
    "Email: " + (fields.email || "none given"),
    "Phone: " + (fields.phone || "none"),
    "",
    fields.message || "(no message body)",
    "",
    "Submitted: " + new Date().toISOString(),
  ].join("\n");
  const html = "<p><b>New opening-day message from " + SITE + " demo</b></p><ul>" +
    "<li>Name: " + name + "</li><li>Email: " + email + "</li><li>Phone: " + (phone || "none") + "</li></ul>" +
    "<p>" + (msg || "(no message body)").replace(/\n/g, "<br>") + "</p>" +
    "<p><small>Submitted: " + new Date().toISOString() + "</small></p>";
  try {
    const r = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": BREVO_KEY, "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({
        sender: { name: SITE + " demo", email: LANE_INBOX },
        to: [{ email: LANE_INBOX }],
        replyTo: fields.email ? { email: fields.email, name: fields.name || fields.email } : undefined,
        subject: "[OPENING-LIST " + SITE + "] " + (fields.name || "no name"),
        textContent: text,
        htmlContent: html,
      }),
    });
    if (!r.ok) return { ok: false, why: "brevo-" + r.status + ":" + (await r.text()).slice(0, 200) };
    return { ok: true, id: (await r.json()).messageId };
  } catch (e) {
    return { ok: false, why: String(e).slice(0, 200) };
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  let p = decodeURIComponent(url.pathname);

  if (p === "/healthz") { res.writeHead(200, { "content-type": "text/plain" }); return res.end("ok"); }

  // demand pixel: 43-byte transparent GIF, one row per GET with token in access log
  if (p === "/pixel.gif") {
    const buf = fs.readFileSync(path.join(__dirname, "pixel.gif"));
    res.writeHead(200, { "content-type": "image/gif", "cache-control": "no-store, no-cache, must-revalidate", "x-rails": "pixel" });
    return res.end(buf);
  }

  if (req.method === "POST" && p === "/contact") {
    let body = "";
    req.on("data", (c) => { if (body.length < 64 * 1024) body += c; });
    req.on("end", async () => {
      const fields = Object.fromEntries(new URLSearchParams(body));
      if (!fields.name && !fields.message) {
        res.writeHead(400, { "content-type": "text/html; charset=utf-8" });
        return res.end(thanksPage(true));
      }
      const relay = await relayContact(fields);
      if (!relay.ok) console.log("MAILERR " + relay.why);
      else console.log("MAILSENT " + relay.id);
      if (relay.ok) {
        res.writeHead(303, { location: "/thanks" });
        res.end();
      } else {
        res.writeHead(502, { "content-type": "text/html; charset=utf-8" });
        res.end(thanksPage(true));
      }
    });
    return;
  }

  if (req.method !== "GET" && req.method !== "HEAD") {
    res.writeHead(405, { allow: "GET, HEAD, POST" });
    return res.end();
  }

  let file = p === "/" ? "/index.html" : p;
  if (!path.extname(file)) file += ".html";
  const abs = path.join(PUB, path.normalize(file));
  if (!abs.startsWith(PUB)) { res.writeHead(403); return res.end(); }

  fs.readFile(abs, (err, buf) => {
    if (err) {
      const nf = path.join(PUB, "404.html");
      fs.readFile(nf, (e2, b2) => {
        res.writeHead(e2 ? 500 : 404, { "content-type": "text/html; charset=utf-8", "x-robots-tag": "noindex, nofollow" });
        res.end(e2 ? "server error" : b2);
      });
      return;
    }
    const ext = path.extname(abs);
    const headers = { "content-type": MIME[ext] || "application/octet-stream" };
    if (ext === ".html") headers["x-robots-tag"] = "noindex, nofollow";
    if (ext === ".gif" || ext === ".png") headers["cache-control"] = "public, max-age=86400";
    if (ext === ".css" || ext === ".svg") headers["cache-control"] = "public, max-age=3600";
    res.writeHead(200, headers);
    res.end(buf);
  });
});

server.listen(PORT, () => console.log(SITE + " demo up on :" + PORT));
