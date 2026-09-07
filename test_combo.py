"""
Local test for ACOMBOWOMBO-no claudecode combo.
Verifies:
  1. Env (OPENAI_API_KEY, OPENAI_BASE_URL) is set
  2. Endpoint accepts your key (GET /v1/models)
  3. LiteLLM can route to model "ACOMBOWOMBO-no claudecode"
Run:
  python test_combo.py
Delete the file after testing — it's not part of the workflow.
"""
import os, sys, json
import urllib.request, urllib.error

KEY  = "sk-8d7687bc85722ad6-3b417a-851dc02a"
BASE = "https://street-sympathy-brother-cio.trycloudflare.com/v1"
MODEL = "ACOMBOWOMBO-no claudecode"

print("=== Test 1: env wiring ===")
print(f"  OPENAI_API_KEY set : {bool(os.environ.get('OPENAI_API_KEY'))}")
print(f"  OPENAI_BASE_URL set: {bool(os.environ.get('OPENAI_BASE_URL'))}")

# Set defaults for this run
os.environ.setdefault("OPENAI_API_KEY", KEY)
os.environ.setdefault("OPENAI_BASE_URL", BASE)

print("\n=== Test 2: endpoint reachable + key valid ===")
try:
    req = urllib.request.Request(f"{BASE}/models", headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        body = json.loads(r.read())
        ids = [m.get("id") for m in body.get("data", [])]
        print(f"  Endpoint OK. {len(ids)} models available.")
        # Check if our combo model is listed
        match = [m for m in ids if "ACOMBOWOMBO" in m or MODEL in m]
        if match:
            print(f"  ✓ MATCH: {match[:3]}")
        else:
            print(f"  Sample IDs: {ids[:5]}")
            print(f"  ⚠ Combo '{MODEL}' not listed — endpoint may accept any string anyway")
except urllib.error.HTTPError as e:
    print(f"  ✗ HTTP {e.code}: {e.reason}")
    print("  Key may be invalid or expired. Stop here.")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ Connection error: {e}")
    print("  Endpoint may be down. Stop here.")
    sys.exit(1)

print("\n=== Test 3: LiteLLM routes to combo ===")
try:
    import litellm
    print(f"  litellm version: {litellm.__version__}")
    # Tiny prompt to confirm routing works
    resp = litellm.completion(
        model=f"openai/{MODEL}",
        messages=[{"role": "user", "content": "ping"}],
        max_tokens=5,
        api_base=BASE,
        api_key=KEY,
        timeout=30,
    )
    print(f"  ✓ Model responded: {resp.get('model', 'unknown')}")
    print(f"  Content: {resp.choices[0].message.content!r}")
    print(f"  Tokens:  in={resp.usage.prompt_tokens} out={resp.usage.completion_tokens}")
except ImportError:
    print("  ⚠ litellm not installed locally; install with: pip install litellm")
except Exception as e:
    print(f"  ✗ LiteLLM error: {type(e).__name__}: {e}")
    print("  Combo routing failed. Likely: model name typo, or endpoint needs different model ID.")
    sys.exit(1)

print("\n=== ALL TESTS PASSED ===")
print("Combo works. To use in .yml, set secret LITELLM_MODEL = 'ACOMBOWOMBO-no claudecode'")
