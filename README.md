# QafiaSaz (قافیہ ساز) ✒️

**QafiaSaz** is a high-performance, blazing-fast web application and API designed to help Urdu and Arabic poets find rhyming words (Qafiya) and match exact poetic meters (Aruuz).

With an optimized SQLite database containing over 170,000 words mapped to their exact meters, QafiaSaz provides instant prefix and suffix search capabilities.

## Features ✨
* **Instant Rhyme Search:** Find words ending in a specific suffix instantly (uses an optimized reversed-string database index).
* **Smart Meter Matching (Afa'il):** Search for exact meters. The system natively understands standard prosody patterns (د = 2, ا = 1). For example, searching `دا` acts as `21`.
* **Beautiful RTL Interface:** An elegant, classically styled UI designed with premium Urdu typography (Jameel Noori Nastaleeq / Noto Nastaliq).
* **FastAPI Backend:** Fully asynchronous, deployment-ready backend.
* **Serverless Ready:** Configured to be deployed on Vercel seamlessly (`vercel.json` included).

## How to Run Locally 💻

1. **Install Dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API Server:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

3. **Open the Website:**
   Simply double-click `index.html` in your browser, or serve it via any local server.

4. **API Documentation:**
   Once the server is running, visit `http://localhost:8000/docs` to see the automated Swagger UI for the API.

## Deployment on Vercel 🚀

This repository is strictly organized and perfectly set up for one-click Vercel deployment:
1. Push this code to a new GitHub repository.
2. Go to [Vercel.com](https://vercel.com/) and click "Add New Project".
3. Import your GitHub repository.
4. Click "Deploy". Vercel will automatically host both your `index.html` frontend and the `main.py` Python API.

---
*Created for the Urdu poetry community.*
