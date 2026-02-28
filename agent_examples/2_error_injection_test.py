import os
import sys
from openai import OpenAI

JACK_PROXY_PORT = os.getenv("JACK_PROXY_PORT", "8002")

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is missing.")
        sys.exit(1)

    print(f"🔄 Connecting to Jack Proxy on http://localhost:{JACK_PROXY_PORT}...")
    client = OpenAI(
        api_key=api_key,
        base_url=f"http://localhost:{JACK_PROXY_PORT}/v1",
        max_retries=0  # Disable auto-retries to see the raw error immediately
    )

    print("\n--- Test 2: Error Injection ---")
    print("⚠️  Ensure you have enabled 'Error Injection' (e.g. 500 status code) on this proxy via Jack's UI.")
    print("📤 Sending Request (Expect Simulated Failure)...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Tell me a joke."}]
        )
        print("❌ Test Failed: Received a successful response when an error was expected.")
        print(f"Response: {response.choices[0].message.content}")
        print("Did you configure an Error Injection rate in the Jack Dashboard?")
        
    except Exception as e:
        print("\n✅ Test Passed! Jack successfully intercepted the request and injected an error:")
        print(f"💥 {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    main()
