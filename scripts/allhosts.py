from mitmproxy import http
def response(flow: http.HTTPFlow):
    print(flow.request.pretty_host)
