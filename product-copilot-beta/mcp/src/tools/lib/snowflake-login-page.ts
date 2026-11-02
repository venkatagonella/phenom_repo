/**
 * Page shown in the browser tab after the Okta SSO redirect back to the
 * Snowflake driver. Self-contained (no external assets) so it renders offline.
 * `error` arrives HTML-escaped from the driver.
 */
export function renderSnowflakeLoginPage({ error }: { error: string | null }): string {
  const ok = !error;
  const title = ok ? "You're signed in to Snowflake" : "Snowflake sign-in failed";
  const body = ok
    ? "Product Copilot can now run your Snowflake queries. You can close this tab and go back to Cursor or Claude Code."
    : `${error}<br><br>Go back to Cursor or Claude Code and run the query again to retry.`;
  const icon = ok
    ? `<path d="M5.5 12.5l4.2 4.2L18.5 8" />`
    : `<path d="M7.5 7.5l9 9M16.5 7.5l-9 9" />`;

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${ok ? "Signed in" : "Sign-in failed"} · Product Copilot</title>
<style>
  :root {
    --bg: #f4f5fb; --card: #ffffff; --ink: #1a1c2e; --muted: #6b6b73; --line: #e6e7ef;
    --navy: #131a4a; --accent: ${ok ? "#2f9e8f" : "#c2410c"}; --accent-soft: ${ok ? "#daf3f2" : "#f6e2d5"};
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0d1030; --card: #161a42; --ink: #f2f3fa; --muted: #a9abc4; --line: #262b5c;
      --accent: ${ok ? "#5fd0c0" : "#f29a6b"}; --accent-soft: ${ok ? "#1d3d42" : "#43261a"};
    }
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; margin: 0; }
  body {
    display: flex; align-items: center; justify-content: center; padding: 24px;
    background: radial-gradient(1200px 600px at 50% -10%, var(--accent-soft), transparent 60%), var(--bg);
    color: var(--ink);
    font-family: Poppins, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  .card {
    width: 100%; max-width: 440px; padding: 40px 36px 32px; text-align: center;
    background: var(--card); border: 1px solid var(--line); border-radius: 20px;
    box-shadow: 0 20px 50px -20px rgba(19, 26, 74, 0.25);
    animation: rise 0.45s ease-out both;
  }
  .badge {
    width: 72px; height: 72px; margin: 0 auto 22px; border-radius: 50%;
    display: grid; place-items: center; background: var(--accent-soft);
  }
  .badge svg { width: 38px; height: 38px; fill: none; stroke: var(--accent); stroke-width: 2.4;
    stroke-linecap: round; stroke-linejoin: round; }
  .badge path { stroke-dasharray: 24; stroke-dashoffset: 24; animation: draw 0.5s 0.25s ease-out forwards; }
  h1 { margin: 0 0 10px; font-size: 22px; font-weight: 600; letter-spacing: -0.01em; }
  p { margin: 0; font-size: 15px; line-height: 1.6; color: var(--muted); }
  .meta {
    margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--line);
    display: flex; align-items: center; justify-content: center; gap: 8px;
    font-size: 12px; color: var(--muted); letter-spacing: 0.02em;
  }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
  @keyframes draw { to { stroke-dashoffset: 0; } }
  @media (prefers-reduced-motion: reduce) {
    .card, .badge path { animation: none; stroke-dashoffset: 0; }
  }
</style>
</head>
<body>
  <main class="card">
    <div class="badge"><svg viewBox="0 0 24 24" aria-hidden="true">${icon}</svg></div>
    <h1>${title}</h1>
    <p>${body}</p>
    <div class="meta"><span class="dot"></span>Phenom Product Copilot · Snowflake SSO</div>
  </main>
</body>
</html>`;
}
