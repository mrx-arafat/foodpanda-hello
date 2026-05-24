from mitmproxy import http
WROTE = False
def response(flow: http.HTTPFlow):
    global WROTE
    if WROTE: return
    r = flow.request
    if "/vendors-gateway/api/v1/pandora/vendors" not in r.path: return
    if r.method != "GET": return
    if not flow.response or flow.response.status_code != 200: return
    print("URL:", r.pretty_url[:200])
    print("--- ALL HEADERS ---")
    for k,v in r.headers.items():
        print(f"  {k}: {v[:200]}")
    print("--- COOKIES ---")
    for k,v in r.cookies.items():
        print(f"  {k}: {v[:120]}")
    WROTE = True
