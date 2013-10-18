from twisted.internet.defer import Deferred, succeed
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from zope.interface import implements
from twisted.web.iweb import IBodyProducer
from twisted.internet.task import react

class HTTPQueryRunner:
	def send(
		self,
		method,
		uri,
		onResponse,
		bodyProducer = None,
		contentType = 'text/x-greeting'):
		def main(reactor):
			agent = Agent(reactor)
			d = agent.request(
				method,
				"http://localhost:8080" + uri,
				Headers({'Content-Type': [contentType]}),
				bodyProducer)

			d.addCallback(onResponse)
			return d

		react(main)

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

		self.send(method, uri, onResponse, bodyProducer, contentType)

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
