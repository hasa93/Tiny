class Response:

	def __init__(self, conn):
		self.headers = []
		self.conn = conn
		pass

	def setStatus(self, code, status):
		status_header = "HTTP/1.1 " + `code` + " " + status + "\r\n"
		self.headers.insert(0, status_header)
		return

	def setHeader(self, header):
		self.headers.append(header + "\r\n")
		return

	def appendHeaderTo(self, body):
		res_string = "".join(self.headers) + "\r\n" + body
		self.headers = []
		return res_string


	def sendTest(self):
		self.setStatus(200, "OK")
		self.setHeader("Content-Type:text/html")

		body = "<b> Hola! </b>"

		self.conn.sendall(self.appendHeaderTo(body))

	def sendNotFound(self, path=None):
		self.setStatus(404, "Not Found")
		self.setHeader("Content-Type:text/html")

		body = "<h1> 404 - Not Found </h1><b>Requested Resouce Not Found</b>"

		if path != None:
			try:
				f = open(path, 'r')
				body = reduce(lambda a, b: a.strip() + b.strip(), f.readlines())
			except IOError:
				pass

		self.conn.sendall(self.appendHeaderTo(body))


	def sendHtml(self, path):
		try:
			f = open(path, 'r')
			body = reduce(lambda a, b: a.strip() + b.strip(), f.readlines())
			f.close()

			self.setStatus(200, "OK")
			self.setHeader("Content-Type:text/html")
			self.conn.sendall(self.appendHeaderTo(body))

		except IOError:
			return self.sendNotFound('./www/error.html')

	def sendPng(self, path):
		try:
			f = open(path, 'r')
			body = f.read()
			f.close()

			self.setStatus(200, "OK")
			self.setHeader("Content-Type:image/png")
			self.conn.sendall(self.appendHeaderTo(body))

		except:
			self.sendNotFound('./www/error.html')


