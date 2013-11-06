from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody, HTTPConnectionPool
from twisted.web.http_headers import Headers

class HTTPQueryRunner:
	pool = HTTPConnectionPool(reactor)

	def __init__(self):
		self.agent = Agent(reactor, pool=self.pool)

	def send(
		self,
		method,
		uri,
		onResponse,
		bodyProducer = None,
		contentType = 'text/x-greeting'):	
		d = self.agent.request(
			method,
			"http://mpgx.rave.org:8080" + uri,
			Headers({'Content-Type': [contentType]}),
			bodyProducer)

		d.addCallback(onResponse)
		return d

	def sendSimple(
		self,
		method,
		uri,
		onResponseBody,
		bodyProducer = None,
		contentType = "application/json"):
		def onResponse(response):
			d = readBody(response)
			d.addCallback(onResponseBody)
			return d

		return self.send(method, uri, onResponse, bodyProducer, contentType)

	def reactOn(self,d):
		def onEnd(response):
			reactor.stop()
		d.addBoth(onEnd)
		reactor.run()

	#def sendHTTPWithReceiver(
	#	method,
	#	uri,
	#	receiver,
	#	contentType = "application/json",
	#	bodyProducer = None):
	#	def onResponse(response):
	#		finished = Deferred()
	#		response.deliverBody(response)
	#		d.addCallback(onResponseBody)
	#		return d
	#
	#	sendHTTP(method, uri, onResponse, contentType, bodyProducer)

http = HTTPQueryRunner()
