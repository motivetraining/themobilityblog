// Search Console data for the monthly topic plan: what people searched to
// find the blog, which pages they landed on, and how that changed.
//
//   bun run audit:gsc            readable summary
//   bun run audit:gsc -- --json  everything, as JSON
//
// Needs GSC_SERVICE_ACCOUNT_KEY (a Google service-account key, as JSON or
// base64 JSON) whose account has been added as a user on the Search Console
// property. No dependencies. In the Claude cloud environment, Node's fetch
// only goes through the network proxy when NODE_USE_ENV_PROXY=1 is set, which
// the package.json script does.
import crypto from "node:crypto";

const SITE = process.env.GSC_SITE ?? "sc-domain:themobilityblog.com";
const API = "https://searchconsole.googleapis.com/webmasters/v3";
const asJson = process.argv.includes("--json");

function loadKey() {
  const raw = process.env.GSC_SERVICE_ACCOUNT_KEY;
  if (!raw) throw new Error("GSC_SERVICE_ACCOUNT_KEY is not set.");
  try {
    return JSON.parse(raw);
  } catch {
    return JSON.parse(Buffer.from(raw, "base64").toString("utf8"));
  }
}

async function accessToken(key) {
  const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const unsigned =
    b64({ alg: "RS256", typ: "JWT" }) +
    "." +
    b64({
      iss: key.client_email,
      scope: "https://www.googleapis.com/auth/webmasters.readonly",
      aud: "https://oauth2.googleapis.com/token",
      iat: now,
      exp: now + 3000,
    });
  const jwt = unsigned + "." + crypto.sign("RSA-SHA256", Buffer.from(unsigned), key.private_key).toString("base64url");
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }),
  });
  const body = await res.json();
  if (!body.access_token) throw new Error(`Google sign-in failed: ${JSON.stringify(body).slice(0, 300)}`);
  return body.access_token;
}

const day = (offset) => new Date(Date.now() - offset * 864e5).toISOString().slice(0, 10);
// Search Console data lags two to three days, so every window ends 3 days ago.
const LAG = 3;
const windows = {
  last28: { startDate: day(LAG + 27), endDate: day(LAG) },
  prior28: { startDate: day(LAG + 55), endDate: day(LAG + 28) },
  last90: { startDate: day(LAG + 89), endDate: day(LAG) },
};

async function main() {
  const key = loadKey();
  const token = await accessToken(key);
  const auth = { authorization: `Bearer ${token}` };

  const sites = await (await fetch(`${API}/sites`, { headers: auth })).json();
  const visible = (sites.siteEntry ?? []).map((s) => s.siteUrl);
  if (!visible.includes(SITE)) {
    throw new Error(
      `The service account ${key.client_email} has no access to ${SITE}. ` +
        `Add it in Search Console: Settings, Users and permissions, Add user (Restricted is enough). ` +
        `It can currently see: ${visible.join(", ") || "nothing"}.`
    );
  }

  const query = async (window, dimensions, rowLimit = 500) => {
    const res = await fetch(`${API}/sites/${encodeURIComponent(SITE)}/searchAnalytics/query`, {
      method: "POST",
      headers: { ...auth, "content-type": "application/json" },
      body: JSON.stringify({ ...window, dimensions, rowLimit }),
    });
    const body = await res.json();
    if (body.error) throw new Error(`Search Console query failed: ${body.error.message}`);
    return (body.rows ?? []).map((r) => ({
      ...Object.fromEntries(dimensions.map((d, i) => [d, r.keys[i]])),
      clicks: r.clicks,
      impressions: r.impressions,
      ctr: +(r.ctr * 100).toFixed(2),
      position: +r.position.toFixed(1),
    }));
  };

  const out = { site: SITE, windows };
  for (const [name, window] of Object.entries(windows)) {
    out[name] = {
      queries: await query(window, ["query"]),
      pages: await query(window, ["page"], 200),
      // Which page each query lands on: shows gaps (a query with no page built
      // for it) and two pages competing for one query.
      queryPages: name === "prior28" ? undefined : await query(window, ["query", "page"], 1000),
    };
  }

  if (asJson) {
    console.log(JSON.stringify(out, null, 2));
    return;
  }
  const total = (rows, k) => rows.reduce((n, r) => n + r[k], 0);
  for (const name of ["last28", "prior28", "last90"]) {
    const { pages, queries } = out[name];
    console.log(
      `${name} (${windows[name].startDate} to ${windows[name].endDate}): ` +
        `${total(pages, "clicks")} clicks, ${total(pages, "impressions")} impressions, ${queries.length} queries`
    );
  }
  console.log("\nTop queries, last 28 days (impressions | clicks | position):");
  for (const q of [...out.last28.queries].sort((a, b) => b.impressions - a.impressions).slice(0, 40)) {
    console.log(`  ${String(q.impressions).padStart(6)} | ${String(q.clicks).padStart(4)} | ${String(q.position).padStart(5)} | ${q.query}`);
  }
  console.log("\nRun with --json for every query, page, and query-page pair.");
}

main().catch((err) => {
  console.error(`ACTION NEEDED: ${err.message}`);
  process.exit(1);
});
