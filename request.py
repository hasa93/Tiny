class Request:

	def __init__(self, header):
		r_headers = header.split('\r\n')
		print r_headers
		status = r_headers[0].strip().split(" ")

		self.headers = { 'uri': status[1], 'headers': r_headers[1:] }
		print self.headers