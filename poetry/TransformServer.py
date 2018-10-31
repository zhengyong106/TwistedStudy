from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol


class TransformProtocol(Protocol):
    def dataReceived(self, data):
        self.transport.write(data.upper())


class TransformServerFactory(Factory):
    protocol = TransformProtocol


# telnet 127.0.0.1 8806
if __name__ == '__main__':
    # from twisted.internet.selectreactor import SelectReactor
    # SelectReactor.listenTCP
    reactor.listenTCP(8806, TransformServerFactory())
    reactor.run()
