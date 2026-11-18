from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import threading,time
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/slow':time.sleep(3)
        code=503 if self.path=='/error' else (200 if self.path in ('/health','/slow') else 404)
        payload=({'200':b'OK','503':b'SERVICE UNAVAILABLE','404':b'NOT FOUND'}[str(code)])
        try:
            self.send_response(code);self.send_header('Content-Type','text/plain');self.end_headers();self.wfile.write(payload)
        except BrokenPipeError:pass
    def log_message(self,fmt,*args): pass
servers=[ThreadingHTTPServer(('127.0.0.1',p),H) for p in (8765,8766)]
for s in servers:threading.Thread(target=s.serve_forever,daemon=True).start()
print('Started: http://127.0.0.1:8765 and :8766; Ctrl+C to stop',flush=True)
try:
    while True:time.sleep(1)
except KeyboardInterrupt:pass
finally:
    for s in servers:s.shutdown();s.server_close()
