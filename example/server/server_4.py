from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class LoggingProtocol(LineReceiver):

    def lineReceived(self, line):
        self.factory.file.write(line + b'\n')

    def rawDataReceived(self, data):
        self.transport.write(data)


class LoggingFactory(Factory):

    protocol = LoggingProtocol

    def __init__(self, filename):
        self.file = None
        self.fileName = filename

    def startFactory(self):
        self.file = open(self.fileName, 'a')

    def stopFactory(self):
        self.file.close()


# telnet 127.0.0.1 8816
if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 8816)
    endpoint.listen(LoggingFactory())
    reactor.run()
