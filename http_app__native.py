import http.server
import urllib

MEM = dict()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        pth = urllib.parse.urlparse(self.path)
        qstr = pth.query

        if qstr:
            for kvstr in qstr.split('&'):
                kv = kvstr.split('=', 1)
                if len(kv) == 2:
                    k, v = kv
                    MEM[k] = v
        
            self.send_response(200)
        else:
            self.send_response(400)
        
        self.end_headers()

    def do_GET(self):
        pth = urllib.parse.urlparse(self.path)
        qstr = pth.query

        queryHasKey = False
        if qstr:
            for kvstr in qstr.split('&'):
                kv = kvstr.split('=', 1)
                if len(kv) == 2 and kv[0] == 'key':
                    v = kv[1]
                    if v in MEM:
                        respBody = MEM[v]
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(respBody.encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.end_headers()
                    queryHasKey = True
                    break
        if not queryHasKey:
            self.send_response(400)
            self.end_headers()
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=4000)
    args = parser.parse_args()

    httpd = http.server.HTTPServer(('localhost', args.port), Handler)
    httpd.serve_forever()
