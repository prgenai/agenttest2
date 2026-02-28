import os
import sys
import time
from openai import OpenAI
import httpx

JACK_PROXY_PORT = os.getenv("JACK_PROXY_PORT", "8002")

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is missing.")
        sys.exit(1)

    print(f"🔄 Connecting to Jack Proxy on http://localhost:{JACK_PROXY_PORT}...")
    
    # We set a tight timeout on our client side (2 seconds)
    # The proxy should be configured to delay > 2s to force a Timeout error.
    client = OpenAI(
        api_key=api_key,
        base_url=f"http://localhost:{JACK_PROXY_PORT}/v1",
        timeout=2.0 
    )

    print("\n--- Test 3: Timeout Simulation ---")
    print("⚠️  Ensure you have enabled 'Timeout Simulation' (e.g. Fixed delay > 3000ms) on this proxy via Jack's UI.")
    print("⏰ Client timeout is explicitly set to 2.0s.")
    print("📤 Sending Request...")
    
    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, world!"}]
        )
        duration = time.time() - start_time
        print(f"❌ Test Failed: Received response in {duration:.2f}s when a timeout was expected.")
        print("Did you configure a Timeout Simulation in the Jack Dashboard?")
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"\n✅ Test Passed! Request timed out globally after {duration:.2f}s:")
        print(f"🐢 {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    main()
