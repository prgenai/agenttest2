# Jack Agent Examples

This directory contains demonstration scripts showing how to route native LLM API calls through your local Jack proxy instead of directly to the provider. 

## OpenAI Example (`openai_example.py`)
This script uses the official Python `openai` package to connect to a Jack-managed mock LLM node.

### Setup Instructions

**1. Install Dependencies**
Ensure you have the `openai` Python package installed in your active environment:
```bash
pip install openai
```

**2. Create a Mock Proxy**
Run the Jack server and open the web dashboard (`http://localhost:5173`). 
Navigate to the **Proxies** page and create a new proxy with the provider set to `openai`. Once created, click "Start" and note the **Port** it binds to (e.g., `8002`).

**3. Configure Environment Variables**
Export your real OpenAI API key and the port number of your active Jack proxy:
```bash
export OPENAI_API_KEY="sk-..."
export JACK_PROXY_PORT="8002"
```

**4. Run the Script**
Execute the demonstration script:
```bash
python agent_examples/openai_example.py
```

*Note: The script specifically points `base_url` to `http://localhost:<PORT>/v1` to seamlessly hook into Jack's reverse proxy router without any code modifications required beyond the URL swap.*
