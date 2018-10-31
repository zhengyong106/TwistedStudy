from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint


class QOTDProtocol(Protocol):
    def connectionMade(self):
        self.transport.write(b"An apple a day keeps the doctor away\r\n")
        self.transport.loseConnection()


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTDProtocol()


# telnet 127.0.0.1 8007
if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 8007)
    endpoint.listen(QOTDFactory())
    reactor.run()
