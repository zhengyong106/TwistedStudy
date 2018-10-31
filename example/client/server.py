from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class SimpleProtocol(LineReceiver):
    def lineReceived(self, line):
        print("%s:%s>> " % self.transport.client + line.decode("gbk"))

    def rawDataReceived(self, data):
        self.transport.write(data)

    def connectionMade(self):
        print("Welcome! %s:%s" % self.transport.client)

    def connectionLost(self, reason):
        print("Goodbye! %s:%s" % self.transport.client)


class SimpleFactory(Factory):
    def buildProtocol(self, address):
        return SimpleProtocol()


# telnet 127.0.0.1 8654
if __name__ == '__main__':
    reactor.listenTCP(8654, SimpleFactory())
    reactor.run()
