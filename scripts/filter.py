import re
from mitmproxy import http

API_HOSTS = re.compile(r"(foodpanda|fd-api|deliveryhero|foodora)", re.I)
SKIP_EXT = re.compile(r"\.(png|jpg|jpeg|gif|svg|woff2?|ttf|css|ico|webp|mp4|js|map)(\?|$)", re.I)
SKIP_HOSTS = re.compile(r"^(images|micro-assets|cdn|static)\.", re.I)
JUNK_PATHS = re.compile(r"^/(static|assets|images|fonts|favicon)", re.I)

def response(flow: http.HTTPFlow):
    r = flow.request
    host = r.pretty_host
    if not API_HOSTS.search(host):
        return
    if SKIP_HOSTS.match(host):
        return
    path = r.path.split("?")[0]
    if SKIP_EXT.search(path) or JUNK_PATHS.match(path):
        return
    ct = flow.response.headers.get("content-type", "") if flow.response else ""
    if flow.response and not any(t in ct for t in ("json", "xml", "graphql", "text/plain", "javascript")):
        return
    s = flow.response.status_code if flow.response else "-"
    print(f"{r.method:6} {s} {r.pretty_url}")
