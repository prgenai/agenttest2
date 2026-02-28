# Jack Agent Examples

This directory contains simple demonstration scripts showing how to route native LLM API calls through your local Jack proxy instead of directly to the provider. 

## OpenAI Example (`openai_example.py`)
This script uses the official Python `openai` package.

To run it:
1. Ensure Jack is running locally and you have created an active OpenAI proxy (e.g. on port 8002).
2. Export your API Key: `export OPENAI_API_KEY="sk-..."`
3. Export your proxy port: `export JACK_PROXY_PORT="8002"`
4. Run the script: `python openai_example.py`

*Note: The script specifically points `base_url` to `http://localhost:<PORT>/v1` to seamlessly hook into Jack's reverse proxy router without any code modifications required beyond the URL swap.*
