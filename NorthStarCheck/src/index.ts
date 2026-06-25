import { buildApp } from './app.js';
import {
  DEMO_PRIMARY_USER,
  DEMO_SECONDARY_USER,
  DEMO_TENANT,
  demoCreateUrl,
  demoUiUrl,
  seedDemoData,
} from './demo/seed.js';

const PORT = Number(process.env.PORT ?? 3000);
const jobId = seedDemoData();
const base = `http://localhost:${PORT}`;

const app = buildApp();

app.get('/', (_req, res) => {
  res.type('html').send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>NorthStarCheck — CRM Demo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="/ui/pds.css"/>
</head>
<body>
  <div class="demo-hub">
    <div class="demo-hub__card">
      <h1>NorthStarCheck — CRM Demo</h1>
      <p>Phenom Design System UI modeling Pipeline <strong>Create New Job</strong> with Secondary Recruiter permission enforcement.</p>
      <p style="font-size:13px;color:var(--pds-text-muted);margin-bottom:20px;">Demo job: <code>${jobId}</code> · Flag: <code>hiring_team_expanded_roles</code> ON</p>
      <div class="demo-links">
        <a class="demo-link" href="${demoCreateUrl(base, DEMO_SECONDARY_USER)}">
          <div><strong>Create New Job — Secondary Recruiter</strong><span>Pipeline-style create flow; delete/close unavailable after creation</span></div>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        </a>
        <a class="demo-link" href="${demoUiUrl(base, jobId, DEMO_SECONDARY_USER)}">
          <div><strong>Job Details — Secondary Recruiter</strong><span>Close Job and Delete Job actions hidden</span></div>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        </a>
        <a class="demo-link" href="${demoUiUrl(base, jobId, DEMO_PRIMARY_USER)}">
          <div><strong>Job Details — Primary Recruiter</strong><span>Full lifecycle actions enabled</span></div>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        </a>
      </div>
    </div>
  </div>
</body>
</html>`);
});

app.listen(PORT, () => {
  console.log(`NorthStarCheck listening on ${base}`);
  console.log(`Demo hub:         ${base}/`);
  console.log(`Create (Secondary): ${demoCreateUrl(base, DEMO_SECONDARY_USER)}`);
  console.log(`Job view (Secondary): ${demoUiUrl(base, jobId, DEMO_SECONDARY_USER)}`);
  console.log(`Job view (Primary):   ${demoUiUrl(base, jobId, DEMO_PRIMARY_USER)}`);
});
