from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory


class EchoProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(b"Welcome! There are currently %d open connections.\n" % (self.factory.numProtocols,))

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(Factory):
    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return EchoProtocol(self)


# telnet 127.0.0.1 8123
if __name__ == '__main__':
    reactor.listenTCP(8123, EchoFactory())
    reactor.run()
