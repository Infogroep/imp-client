from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import Agent, readBody, HTTPConnectionPool
from twisted.web.http_headers import Headers
from twisted.internet.task import react
import getpass

class HTTPQueryRunner:
	pool = HTTPConnectionPool(reactor)

	def __init__(self,config):
		self.agent = Agent(reactor, pool=self.pool)

		host = config["host"].encode('latin-1') if "host" in config else "mpgx.rave.org"
		port = config["port"] if "port" in config else 8080

		self.rootUri = "http://%s:%d" % (host, port)

	def send(
		self,
		method,
		uri,
		bodyProducer = None,
		contentType = "application/json"):
		return self.agent.request(
			method,
			self.rootUri + uri,
			Headers({'Content-Type': [contentType],'Imp-Requesting-User': [getpass.getuser()]}),
			bodyProducer)

	def sendSimple(
		self,
		method,
		uri,
		bodyProducer = None,
		contentType = "application/json"):

		def onResponse(response):
			return readBody(response)

		responseDeferred = self.send(method, uri, bodyProducer, contentType)
		responseDeferred.addCallback(onResponse)
		return responseDeferred

	def sendWithReceiver(
		self,
		method,
		uri,
		receiver,
		bodyProducer = None,
		contentType = "application/json"):
		def onResponse(response):
			response.deliverBody(receiver)
			return receiver.notifyFinish()
	
		responseDeferred = self.send(method, uri, bodyProducer, contentType)
		responseDeferred.addCallback(onResponse)
		return responseDeferred


	def sendCB(
		self,
		method,
		uri,
		onResponse,
		bodyProducer = None,
		contentType = "application/json"):	
		d = self.send(method, uri, bodyProducer, contentType)
		d.addCallback(onResponse)
		return d

	def sendSimpleCB(
		self,
		method,
		uri,
		onResponseBody,
		bodyProducer = None,
		contentType = "application/json"):
		d = self.sendSimple(method, uri, bodyProducer, contentType)
		d.addCallback(onResponseBody)
		return d

	def reactOn(self,d):
#		def onEnd(response):
#			reactor.stop()
#		d.addBoth(onEnd)
#		reactor.run()
		def main(r):
			return d
		react(main)



