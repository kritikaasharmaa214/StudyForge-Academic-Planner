"""Threaded standard-library HTTP server; local development only."""
import json
import mimetypes
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
from . import db, service, repository, validators

WEB = Path(__file__).resolve().parent / 'web'
MAX_BODY=1024*1024

class Handler(BaseHTTPRequestHandler):
    def json_response(self, payload, status=200):
        data=json.dumps(payload,ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(data)

    def request_data(self):
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':
            raise validators.ValidationError('Content-Type must be application/json')
        try: size=int(self.headers.get('Content-Length','0'))
        except ValueError: raise validators.ValidationError('Invalid Content-Length') from None
        if size<=0 or size>MAX_BODY: raise validators.ValidationError('Invalid JSON body size')
        try: return validators.mapping(json.loads(self.rfile.read(size)))
        except (UnicodeDecodeError,json.JSONDecodeError): raise validators.ValidationError('Malformed JSON') from None

    def route(self):
        parsed=urlsplit(self.path)
        path=parsed.path
        if not path.startswith('/api/'):
            if self.command!='GET': return self.json_response({'error':'Method not allowed'},405)
            return self.static(path)
        chunks=path.strip('/').split('/')
        try:
            if self.command=='GET' and len(chunks)==2:
                key=chunks[1]
                if key=='dashboard':return self.json_response(service.dashboard())
                if key=='plan':
                    minutes=parse_qs(parsed.query).get('minutes',['120'])[0]
                    return self.json_response(service.plan(minutes))
                return self.json_response(service.collection(key))
            if self.command=='POST' and len(chunks)==2:
                return self.json_response(service.create(chunks[1],self.request_data()),201)
            if self.command=='PATCH' and len(chunks)==3 and chunks[1]=='tasks':
                return self.json_response(service.update_task(chunks[2],self.request_data()))
            if self.command=='DELETE' and len(chunks)==3:
                return self.json_response(service.remove(chunks[1],chunks[2]))
            return self.json_response({'error':'Unknown API endpoint'},404)
        except validators.ValidationError as e:
            return self.json_response({'error':str(e)},400)
        except repository.NotFound as e:
            return self.json_response({'error':str(e)},404)
        except sqlite3.IntegrityError as e:
            return self.json_response({'error':'Duplicate course code or invalid related data'},409)
        except ValueError as e:
            return self.json_response({'error':str(e)},400)

    def static(self,path):
        if path=='/':path='/index.html'
        if path not in ('/index.html','/app.js','/styles.css'):
            return self.json_response({'error':'Not found'},404)
        target=WEB/path.lstrip('/')
        payload=target.read_bytes()
        mime=mimetypes.guess_type(str(target))[0] or 'application/octet-stream'
        self.send_response(200)
        self.send_header('Content-Type',mime + ('; charset=utf-8' if mime.startswith('text/') or mime=='application/javascript' else ''))
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers();self.wfile.write(payload)

    def do_GET(self):self.route()
    def do_POST(self):self.route()
    def do_PATCH(self):self.route()
    def do_DELETE(self):self.route()

def run(host='127.0.0.1',port=8765):
    db.initialize()
    server=ThreadingHTTPServer((host,port),Handler)
    print(f'StudyForge running at http://{host}:{port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
