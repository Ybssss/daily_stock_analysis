"""Quick local test: does ACOMBOWOMBO-no claudecode respond at this endpoint?"""
import os, sys
os.environ["OPENAI_API_KEY"] = "sk-8d7687bc85722ad6-3b417a-851dc02a"
os.environ["OPENAI_BASE_URL"] = "https://street-sympathy-brother-cio.trycloudflare.com/v1"

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_BASE_URL"])
    models = client.models.list()
    print("OK endpoint responded. Models:", [m.id for m in models.data[:5]])
except Exception as e:
    print("FAIL endpoint:", type(e).__name__, e)
    sys.exit(1)

try:
    resp = client.chat.completions.create(
        model="ACOMBOWOMBO-no claudecode",
        messages=[{"role":"user","content":"Reply OK only."}],
        max_tokens=10,
        temperature=0
    )
    content = resp.choices[0].message.content
    usage = resp.usage
    print("OK chat response:", repr(content))
    print("Usage -> prompt:", usage.prompt_tokens, "completion:", usage.completion_tokens, "total:", usage.total_tokens)
except Exception as e:
    print("FAIL chat call:", type(e).__name__, e)
