from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol

class FileDownloadProtocol(Protocol):
	def __init__(self,fObj,onProgress):
		self.fObj = fObj
		self.finish = Deferred()
		self.onProgress = onProgress
		self.downloaded = 0

	def notifyFinish(self):
		return self.finish

	def dataReceived(self, bytes):
		try:
			self.fObj.write(bytes)
			self.downloaded += len(bytes)
			self.onProgress(self.downloaded)
		except Exception as e:
			print e

	def connectionLost(self, reason):
		self.fObj.close()
		self.finish.callback(None)
