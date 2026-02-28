# Jack Agent Examples

This directory contains demonstration scripts showing how to route native LLM API calls through your local Jack proxy instead of directly to the provider. 

## Testing Jack's Core Features

Built-in to Jack is a comprehensive emulation engine. We provide 4 scripts to verify these feature capabilities:

1. **`1_caching_test.py`**: Tests the semantic caching engine. It sends two identical requests, explicitly monitoring the `X-Cache` response headers and the latency drop between a HIT and a MISS.
2. **`2_error_injection_test.py`**: Validates simulated provider failures. Disables automatic client retries to catch and report the immediate mock HTTP 500/400 errors configured in Jack.
3. **`3_timeout_test.py`**: Evaluates system behavior under high latency. Sets a tight client-side timeout constraints (2.0s) and monitors for the expected timeout exception when Jack delays the response.
4. **`4_rate_limiting_test.py`**: Demonstrates the token bucket rate limiter. Spans rapid rapid requests in a loop to forcefully trigger a mock `429 Too Many Requests` error.

### Setup Instructions

**1. Install Dependencies**
Ensure you have the `openai` Python package installed in your active environment:
```bash
pip install openai
```

**2. Configure Your Mock Proxy**
Run the Jack server and open the web dashboard (`http://localhost:5173`). 
Navigate to the **Proxies** page and create a new proxy with the provider set to `openai`. Once created, click "Start" and note the **Port** it binds to (e.g., `8002`).
To test Scripts 2, 3, and 4, you must click **Configure** on your proxy in the UI and purposefully inject those failures (e.g., set Error Rate, Fixed Delay, and narrow the RPM limits).

**3. Configure Environment Variables**
Export your real OpenAI API key and the port number of your active Jack proxy:
```bash
export OPENAI_API_KEY="sk-..."
export JACK_PROXY_PORT="8002"
```

**4. Run the Scripts**
Execute the demonstration scripts independently:
```bash
python agent_examples/1_caching_test.py
python agent_examples/2_error_injection_test.py
```

*Note: The scripts specifically point `base_url` to `http://localhost:<PORT>/v1` to seamlessly hook into Jack's reverse proxy router without any code modifications required beyond the URL swap.*
