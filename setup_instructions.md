# Jack: Setup and Usage Guide

This guide covers everything you need to know to install, configure, run, and use the Jack LLM proxy testing application from scratch.

---

## 🚀 1. Installation & Setup

### Prerequisites
*   **Python 3.11+**
*   **Node.js 18+** 
*   **Git**

### Step-by-Step Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Zipstack/jack.git
   cd jack
   ```

2. **Set up the Python Virtual Environment:**
   Run the following commands in the project root to create and activate your environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies (With Important Fixes):**
   *Note: To prevent hashing errors with `passlib` and backend test failures, we need to enforce slightly modified dependency versions.*
   
   Ensure that your `requirements.txt` contains:
   ```txt
   fastapi>=0.104.1
   pydantic<2.7.0
   bcrypt<4.0.0
   ```
   *The rest of the `requirements.txt` remains standard.*
   
   Install the necessary base and LLM packages:
   ```bash
   pip install -r requirements.txt
   ```
   If you plan to run automated tests or need the proxy to act as a proper pass-through without throwing import errors, also install:
   ```bash
   pip install requests openai anthropic google-generativeai
   ```

4. **Initialize the Database:**
   Run the included installation script to set up SQLite and run Alembic migrations:
   ```bash
   ./scripts/fresh_install.sh
   ```
   *Wait for the "Fresh installation completed successfully" message.*

5. **Set up the Frontend (React):**
   Open a new terminal window, navigate to the frontend directory, and install its dependencies:
   ```bash
   cd frontend
   npm install
   ```

---

## 🏃 2. Running the Application

You will need **two terminal windows** open—one for the backend API and one for the frontend UI.

### Terminal 1: Backend Server
Navigate to the `jack` root directory, activate your virtual environment, and start the Python server:
```bash
source venv/bin/activate
python run.py
```
*The backend API will run on `http://localhost:9000`.*
*(If you ever face "Address already in use" errors for port 9000, kill the rogue process using `lsof -ti:9000 | xargs kill -9` before starting).*

### Terminal 2: Frontend Server
Navigate to the `frontend` folder and start the React dev server:
```bash
cd frontend
npm run dev
```
*The web interface will be available at `http://localhost:5173`.*

---

## 🎮 3. How to Use Jack

### Step 1: Log into the Dashboard
1. Open your browser and go to `http://localhost:5173`.
2. Use the default local admin credentials to log in:
   *   **Email:** `admin@example.com`
   *   **Password:** `admin`

### Step 2: Create a New Testing Proxy
Jack acts as an intelligent intermediary between your application code and an actual LLM provider (like OpenAI or Anthropic).
1. Go to the **Proxies** tab on the left sidebar.
2. Click **Create Your First Proxy** (or the Create button).
3. Fill in the details:
   *   **Name:** Give it a memorable name (e.g., "Main OpenAI Gateway").
   *   **Provider:** Select your target LLM provider (e.g., OpenAI).
4. Click **Create Proxy**.

### Step 3: Configure Failure Injection (Chaos Engineering)
Once created, your proxy starts in a "Stopped" state. Click the **Configure** (gear) icon next to your proxy to set up testing constraints:
*   **Timeouts:** Configure a fixed delay or an indefinite hang.
*   **Error Rates:** Force the proxy to return simulated HTTP 429 (Rate Limit) or 500 (Server Error) responses at a percentage basis (e.g., 20% of requests).
*   **Response Delay:** Add an artificial delay (e.g., 2 seconds) specifically for cached responses to mimic realistic LLM loading times.
*   Save your configuration.

### Step 4: Start the Proxy
Click the **Start (Play Arrow)** button next to your proxy. 
*   It will automatically assign a unique local port (e.g., `8001`, `8002`).
*   The status will turn green and say "Running".

### Step 5: Route Your Code Through Jack
In your application code, replace the official base URL with the Jack proxy URL. It transparently passes your actual API keys.

**Python (OpenAI SDK Example):**
```python
import openai

client = openai.OpenAI(
    api_key="your-real-openai-key", # Jack passes this through securely
    base_url="http://localhost:8001" # The port assigned to your running proxy
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

**JavaScript/TypeScript (OpenAI SDK Example):**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'your-real-openai-key',
  baseURL: 'http://localhost:8001', // The port assigned to your running proxy
});

const response = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Hello!' }]
});
console.log(response);
```

### Step 6: Monitor Logs and Caching
1. Navigate to the **Logs** tab in the Jack UI.
2. Every request your application makes will show up here in real-time.
3. You will be able to see:
   *   If the request hit the cache or went upstream.
   *   If a simulated failure (like a 429 error or timeout) was injected.
   *   The overall token usage footprint of your application.
