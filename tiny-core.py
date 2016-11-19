import socket
import request, response, router

HOST, PORT = '', 8889

sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_conn.bind((HOST, PORT))
sock_conn.listen(3)

res = response.Response();
routes = router.Router()

print "Tiny is listening on", PORT

routes.add('/', './www/index.html')
routes.add('/index2', './www/index2.html')
routes.add('/tiny', './www/img/cat.png')

while True:
	conn, addr = sock_conn.accept()
	print "Connection from", addr

	data = conn.recv(1024)

	try:
		req = request.Request(data)
		resource = routes.get(req.headers['uri'])
		conn.sendall(res.compileHtmlResponse(resource))
		conn.close()
	except:
		#send 404 when the route is not defined
		conn.sendall(res.compileNotFoundResponse())
		conn.close()

sock_conn.close()
