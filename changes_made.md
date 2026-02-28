# Jack Codebase Changes

If you have cloned the original `Zipstack/jack` repository, you will encounter a few issues that prevent it from running out of the box.

Apply the following changes to fix initialization, dependency conflicts, and test suite execution.

---

## 1. Backend Dependency Fixes (`requirements.txt`)

The original `requirements.txt` has version incompatibilities out-of-the-box (specifically between newer `bcrypt` versions, `passlib`, and `pydantic`). 

Open `requirements.txt` and make the following replacements:

**Change:**
```txt
fastapi==0.104.1
```
**To:**
```txt
fastapi>=0.104.1
pydantic<2.7.0
```

**Change:**
```txt
bcrypt>=4.2.0
```
**To:**
```txt
bcrypt<4.0.0
```

*(Reasoning: `passlib` throws a 72-byte string hashing error with `bcrypt >= 4.0.0`. `pydantic` needs pinning to avoid attribute missing errors in the `fastapi_users` integration during migrations.)*

---

## 2. Missing LLM SDK Dependencies

The repository expects provider SDKs to be present when testing or initializing specific mock routers, but they are completely missing from the requirement files. 

Run the following in your backend virtual environment:
```bash
pip install requests openai anthropic google-generativeai
```

---

## 3. Frontend Test Setup Fix (`frontend/src/test/setup.ts`)

If you want to run `npm run test`, the tests immediately crash complaining that `localStorage.getItem is not a function`. The Vitest environment needs a mock.

Open `frontend/src/test/setup.ts` and replace its entire contents with:

```typescript
import '@testing-library/jest-dom';
import { vi } from 'vitest';

const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

vi.stubGlobal('localStorage', localStorageMock);
```

---

## 4. Frontend Async Test Fix (`frontend/src/test/ProxyConfigModal.test.tsx`)

The UI tests for the Proxy Configuration rely on synchronous rendering methods (`getByRole`) for elements that are actually rendered asynchronously after an initial loading state. 

If you want the tests to pass green, you must:
1. Make all the `it(...)` callback functions `async`.
2. Convert instances of `screen.getByRole('checkbox', ...)` to `await screen.findByRole('checkbox', ...)`.
3. Convert instances of `screen.getByText('Response Delay')` to `await screen.findByText('Response Delay')`. 

*(We applied this using a Python regex script dynamically during setup, but be aware of it if manually debugging the frontend tests).*

---

## 5. Port Conflicts on Startup

If you run `python run.py` and get an `[Errno 48] Address already in use` error for port `9000`, the server is orphaned in the background.

Kill it before starting:
```bash
lsof -ti:9000 | xargs kill -9
```
