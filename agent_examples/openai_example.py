import os
import sys
from openai import OpenAI

# The proxy port Jack uses. By default, the first proxy binds to 8001 or 8002.
# Update this if your Jack proxy is running on a different port.
JACK_PROXY_PORT = os.getenv("JACK_PROXY_PORT", "8002")

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is missing.")
        print("Please provide your API key to test the proxy.")
        sys.exit(1)

    print(f"🔄 Connecting to Jack Proxy on http://localhost:{JACK_PROXY_PORT}...")
    
    # Initialize the OpenAI client pointing to the Jack local proxy
    # We include /v1 here so the Python SDK sends requests directly to 
    # http://localhost:PORT/v1/chat/completions natively matching Jack's routes.
    client = OpenAI(
        api_key=api_key,
        base_url=f"http://localhost:{JACK_PROXY_PORT}/v1"
    )

    try:
        print("📤 Sending request: 'Explain the concept of rubber duck debugging in one short sentence.'")
        response = client.chat.completions.create(
            model="gpt-4o-mini", # or gpt-4, depending on your proxy's target setup
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain the concept of rubber duck debugging in one short sentence."}
            ]
        )
        
        reply = response.choices[0].message.content
        print("\n✅ Success! Received response from LLM through Jack:")
        print(f"🤖 {reply}")
        
    except Exception as e:
        print(f"\n❌ Error connecting to proxy or LLM: {str(e)}")

if __name__ == "__main__":
    main()
