import os
import sys
import time
from openai import OpenAI
from openai import RateLimitError

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
        max_retries=0 
    )

    print("\n--- Test 4: Rate Limiting ---")
    print("⚠️  Ensure you have enabled 'Rate Limiting' (e.g. 2 Requests per Minute) on this proxy via Jack's UI.")
    print("📤 Spanning multiple rapid requests to trigger the limit...")
    
    success_count = 0
    hit_limit = False
    
    for i in range(5):
        try:
            print(f"[{i+1}/5] Sending request...", end=" ")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Say the number {i}"}]
            )
            success_count += 1
            print(f"✅ Success (Cache: {response.x_cache if hasattr(response, 'x_cache') else 'Unknown'})")
        except RateLimitError as e:
            hit_limit = True
            print(f"❌ RateLimitError caught! (429 Too Many Requests)")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {type(e).__name__}: {str(e)}")
            
    if hit_limit:
        print(f"\n✅ Test Passed! Jack rate limited you after {success_count} successful requests.")
    else:
        print(f"\n❌ Test Failed! All {success_count} requests succeeded. Did you configure Rate Limiting in Jack?")

if __name__ == "__main__":
    main()
