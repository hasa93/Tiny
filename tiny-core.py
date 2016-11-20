import socket
import request, response, router

HOST, PORT = '', 8889

sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	except:
		#send 404 when the route is not defined
		res.sendNotFound()
		conn.close()

sock_conn.close()
