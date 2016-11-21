import socket
import request, response, router

HOST, PORT = '', 8889
static_root = './www'

def sendStaticContent(uri, res):
	ext = uri.split('.')[-1]
	print ext

	if ext == 'html':
		res.sendHtml(uri)
	elif ext == 'png':
		res.sendPng(uri)
	elif ext == 'css':
		res.sendCss(uri)
	else:
		raise Exception('Unsupported file format')
	return

sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_conn.bind((HOST, PORT))
sock_conn.listen(3)

routes = router.Router()

print "Tiny is listening on", PORT

routes.add('/', lambda res: res.sendHtml('./www/index.html'))
routes.add('/index2', lambda res: res.sendHtml('./www/index2.html'))
routes.add('/tiny', lambda res: res.sendPng('./www/img/cat.png'))
routes.add('/tiny-css', lambda res: res.sendCss('./www/css/style.css'))

while True:
	conn, addr = sock_conn.accept()
	print "Connection from", addr

	data = conn.recv(1024)
	res = response.Response(conn);

	try:
		req = request.Request(data)
		res_worker = routes.get(req.headers['uri'])
		res_worker(res)
		conn.close()
	except KeyError:
		#try serving static content
		print "Falling back to static content..."
		req = request.Request(data)
		req_uri = static_root + req.headers['uri']
		sendStaticContent(req_uri, res)
		conn.close()
	except Exception:
		#send 404 when the route is not defined
		print "Resource not found..."
		res.sendNotFound()
		conn.close()

sock_conn.close()
