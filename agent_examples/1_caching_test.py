import os
import sys
import time
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
        base_url=f"http://localhost:{JACK_PROXY_PORT}/v1"
    )

    print("\n--- Test 1: Intelligent Caching ---")
    prompt = "Give me a unique haiku about a rubber duck turning into a robot."

    # First Request (Cache Miss)
    print("📤 Sending Request 1 (Expect Cache Miss)...")
    start_time = time.time()
    response1 = client.chat.completions.with_raw_response.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    duration1 = time.time() - start_time
    
    body1 = response1.parse()
    is_hit1 = response1.headers.get("x-cache") == "HIT"
    
    print(f"✅ Received in {duration1:.2f}s")
    print(f"📦 X-Cache Header: {response1.headers.get('x-cache', 'MISS')}")
    print(f"🤖 Output: {body1.choices[0].message.content}")

    # Second Request (Should be Cache Hit)
    print("\n📤 Sending Request 2 (Identical Prompt - Expect Cache Hit)...")
    start_time = time.time()
    response2 = client.chat.completions.with_raw_response.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    duration2 = time.time() - start_time
    
    body2 = response2.parse()
    
    print(f"✅ Received in {duration2:.2f}s")
    print(f"📦 X-Cache Header: {response2.headers.get('x-cache', 'MISS')}")
    print(f"🤖 Output: {body2.choices[0].message.content}")
    
    if duration2 < duration1 and response2.headers.get("x-cache") == "HIT":
        print("\n🎉 CACHING WORKS! The second request successfully hit Jack's local cache and completely bypassed the upstream LLM.")

if __name__ == "__main__":
    main()
