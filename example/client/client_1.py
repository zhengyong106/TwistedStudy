from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol


class GreeterProtocol(Protocol):
    def send_message(self, msg):
        self.transport.write(msg + b"\r\n")


def got_protocol(protocol):
    protocol.send_message(b"Hello")
    reactor.callLater(5, protocol.send_message, b"This is sent in five second")
    reactor.callLater(10, protocol.transport.loseConnection)


if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, "localhost", 8654)
    deferred = connectProtocol(endpoint, GreeterProtocol())
    deferred.addCallback(got_protocol)
    reactor.run()
