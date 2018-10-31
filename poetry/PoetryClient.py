import sys

from twisted.internet import defer, reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver


class PoetryProtocol(Protocol):

    poem = b''

    def dataReceived(self, data):
        self.poem += data
        msg = 'Port:%s got %d bytes of poetry'
        print(msg % (self.transport.getPeer().port, len(data)))

    def connectionLost(self, reason):
        self.poem_received(self.poem)

    def poem_received(self, poem):
        self.factory.poem_received(poem)


class PoetryClientFactory(ClientFactory):

    protocol = PoetryProtocol

    def __init__(self, deferred):
        self.deferred = deferred

    def poem_received(self, poem):
        if self.deferred is not None:
            self.deferred.callback(poem)
            _, self.deferred = self.deferred, None

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            self.deferred.errback(reason)
            _, self.deferred = self.deferred, None


class TransformProtocol(NetstringReceiver):

    def connectionMade(self):
        self.send_request(self.factory.poem)

    def stringReceived(self, string):
        self.transport.loseConnection()
        self.poem_received(string)

    def send_request(self, poem):
        self.sendString(poem)

    def poem_received(self, poem):
        self.factory.poem_received(poem)


class TransformClientFactory(ClientFactory):

    protocol = TransformProtocol

    def __init__(self, poem, deferred):
        self.poem = poem
        self.deferred = deferred

    def poem_received(self, poem):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(poem)

    def clientConnectionLost(self, _, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)


def get_transform(host, port, poem):
    deferred = defer.Deferred()
    reactor.connectTCP(host, port, TransformClientFactory(poem, deferred))
    return deferred


def get_poetry(host, port):
    deferred = defer.Deferred()
    reactor.connectTCP(host, port, PoetryClientFactory(deferred))
    return deferred


def main():
    poem_addresses = [("localhost", 8807), ("localhost", 8808)]
    transform_address = ("localhost", 8806)

    def poem_finish(poem):
        host, port = transform_address
        deferred = get_transform(host, port, poem)
        deferred.addCallbacks(transform_finish, transform_failed)

    def poem_failed(err):
        print('Poem failed:', err, file=sys.stderr)

    def transform_finish(poem):
        print(poem.decode("utf-8"))

    def transform_failed(err):
        print('Transform failed:', err, file=sys.stderr)

    for address in poem_addresses:
        host, port = address
        deferred = get_poetry(host, port)
        deferred.addCallbacks(poem_finish, poem_failed)

    reactor.run()


if __name__ == '__main__':
    main()
