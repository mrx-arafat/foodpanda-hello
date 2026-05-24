"""Pull headers + cookies from a real captured vendors request -> auth.json"""
import json
from mitmproxy import http

KEEP = {"x-fp-api-key","perseus-client-id","perseus-session-id","dps-session-id",
        "authorization","x-pd-language-id","user-agent","app-name","platform","app-version",
        "accept","accept-language","origin","referer"}

WROTE = False
def response(flow: http.HTTPFlow):
    global WROTE
    if WROTE: return
    r = flow.request
    if r.method != "GET": return
    if "fd-api.com" not in r.pretty_host: return
    if "/vendors-gateway/api/v1/pandora/vendors" not in r.path: return
    if not flow.response or flow.response.status_code != 200: return
    headers = {k: v for k, v in r.headers.items() if k.lower() in KEEP}
    cookies = dict(r.cookies)
    body = flow.response.get_text() or ""
    try:
        j = json.loads(body)
        item = j["data"]["items"][0] if j.get("data",{}).get("items") else None
    except: item = None
    out = {"headers": headers, "cookies": cookies, "sample_item_keys": list(item.keys()) if item else [], "sample_item": item}
    with open("captures/auth.json","w") as f:
        json.dump(out, f, indent=2, default=str)
    print("wrote captures/auth.json")
    WROTE = True
