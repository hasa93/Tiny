class Router:

	def __init__(self):
		self.routes = {}

	def get(self, route):
		try:
			return self.routes[route]
		except:
			raise KeyError("NotDefined")

	def add(self, route, resource):
		self.routes[route] = resource