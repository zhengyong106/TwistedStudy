import time

from twisted.internet import reactor, defer
from twisted.internet.protocol import Protocol, ClientFactory


class GreeterProtocol(Protocol):
    def connectionMade(self):
        self.factory.deferred.callback(self)

    def send_message(self, msg):
        self.transport.socket.sendall(msg + b"\r\n")


class GreeterFactory(ClientFactory):
    protocol = GreeterProtocol

    def __init__(self, deferred):
        self.deferred = deferred

    def startedConnecting(self, connector):
        print('Started to connect.')


def get_greeter_deferred():
    deferred = defer.Deferred()
    reactor.connectTCP('localhost', 8654, GreeterFactory(deferred))
    return deferred


def greet(protocol):
    protocol.send_message(b"Hello")
    reactor.callLater(5, protocol.send_message, bytes(time.ctime(), "utf-8"))
    reactor.callLater(10, reactor.stop)


if __name__ == '__main__':
    _deferred = get_greeter_deferred()
    _deferred.addCallback(greet)
    reactor.run()
