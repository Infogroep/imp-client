from __future__ import division
from twisted.internet import reactor
import os
from twisted.web.client import FileBodyProducer

class ProgressAdapter():
	def __init__(self,producer,onProgress,size):
		self.producer = producer
		self.length = producer.length
		self.onProgress = onProgress
		self.sizeProcessed = 0
		self.sizeTotal = size

	def startProducing(self, consumer):
		self.consumer = consumer
		self.sizeProcessed = 0
		return self.producer.startProducing(self)

	def stopProducing(self):
		self.producer.stopProducing()

	def pauseProducing(self):
		self.producer.pauseProducing()

	def resumeProducing(self):
		self.producer.resumeProducing()

	def registerProducer(self,producer, streaming):
		self.length = self.producer.length
		self.sizeProcessed = 0
		self.consumer.registerProducer(self, streaming)

	def unregisterProducer(self):
		self.consumer.unregisterProducer()

	def write(self,data):
		self.sizeProcessed += len(data)
		self.onProgress(self.sizeProcessed / self.sizeTotal)
		self.consumer.write(data)


class FileProgressProducer(ProgressAdapter):
	def __init__(self,fil,onProgress):
		f = open(fil,"r")
		ProgressAdapter.__init__(self,FileBodyProducer(f),onProgress,os.path.getsize(fil))

