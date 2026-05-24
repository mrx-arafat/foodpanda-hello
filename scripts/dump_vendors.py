import json
from mitmproxy import http
def response(flow: http.HTTPFlow):
    r = flow.request
    if "fd-api.com" not in r.pretty_host: return
    if "/vendors" not in r.path: return
    print("=" * 80)
    print(f"{r.method} {r.pretty_url}")
    print("--- headers ---")
    for k, v in r.headers.items():
        if k.lower() in ("authorization","cookie","x-pd-language-id","perseus-client-id","x-fp-api-key","app-version","platform","dps-session-id","perseus-session-id","app-name"):
            print(f"  {k}: {v[:120]}")
    if flow.response:
        body = flow.response.get_text() or ""
        try:
            j = json.loads(body)
            if isinstance(j, dict):
                keys = list(j.keys())
                print(f"--- response keys: {keys}")
                if "data" in j and isinstance(j["data"], dict):
                    print(f"--- data keys: {list(j['data'].keys())[:20]}")
                    if "items" in j["data"]:
                        print(f"--- items count: {len(j['data']['items'])}")
                    if "returned_count" in j["data"]:
                        print(f"--- returned_count: {j['data'].get('returned_count')}")
                    if "available_count" in j["data"]:
                        print(f"--- available_count: {j['data'].get('available_count')}")
        except Exception as e:
            print(f"--- not json: {e}")
