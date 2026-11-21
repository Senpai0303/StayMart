## 2026-11-02T20:18:54Z
You are Milestone 4 Iteration 2 Explorer 3 (Frontend Reverse-Proxy & API Client Investigator).
Working directory: d:\Mini5th\.agents\teamwork\m4_it2_explorer_3\
Mandatory specification to read: d:\Mini5th\.agents\teamwork\ORIGINAL_REQUEST.md
Also read:
- Master plan: d:\Mini5th\PROJECT.md
- Scope: d:\Mini5th\.agents\teamwork\orchestrator_gen2\SCOPE.md
- Iteration 1 Challenger 2 handoff: d:\Mini5th\.agents\teamwork\m4_challenger_2_gen2\handoff.md
- Target files: d:\Mini5th\frontend\js\api.js, d:\Mini5th\vercel.json, d:\Mini5th\frontend\vercel.json, and other frontend js callers

Objective:
Investigate and design the exact fix for `frontend/js/api.js`:
1. In `frontend/js/api.js` lines 2–6:
   ```javascript
   const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
   const BASE_URL = isLocal
     ? 'http://localhost:8080/api'
     : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
   ```
   Challenger 2 and Reviewer 2 identified that:
   - The fallback URL `'https://staymart.onrender.com/api'` is missing `-backend` (`staymart-backend.onrender.com`).
   - If deployed on Vercel, having an absolute URL bypasses Vercel's edge CDN reverse proxy rewrites (`vercel.json`), forcing unnecessary CORS preflight requests directly to Render.
   - If `window.STAYMART_API_URL` or `localStorage` is not set, a relative `'/api'` fallback works seamlessly with Vercel's reverse proxy rewrites (`/api/(.*)` -> `https://staymart-backend.onrender.com/api/$1`).
2. Verify all other frontend files that import or use `BASE_URL` or `apiFetch` (e.g. `auth.js`, `listings.js`, `stats.js`, `charts.js`). Check if relative `'/api'` or `window.STAYMART_API_URL` handles both local development, Vercel deployments, and direct Render deployments.
3. Formulate concrete, exact code changes for `frontend/js/api.js`.

Rules:
- Read-only investigation: do NOT modify any project source files directly.
- Formulate concrete, exact recommendations and code diffs for the subsequent worker.
- Write your comprehensive report to `d:\Mini5th\.agents\teamwork\m4_it2_explorer_3\handoff.md`.
- Follow the communication protocol: update progress.md, and send a completion message to the parent orchestrator when done.
