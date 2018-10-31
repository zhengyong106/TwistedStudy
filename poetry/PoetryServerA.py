from time import sleep
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol


class PoetryProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        with open(self.factory.poem_path, "rb") as f:
            for line in f:
                self.transport.socket.sendall(line)
                sleep(0.5)
        self.transport.loseConnection()


class PoetryFactory(Factory):

    def __init__(self, poem_path):
        self.poem_path = poem_path

    def buildProtocol(self, _):
        return PoetryProtocol(self)


# telnet 127.0.0.1 8807
if __name__ == '__main__':
    # from twisted.internet.selectreactor import SelectReactor
    # SelectReactor.listenTCP
    reactor.listenTCP(8807, PoetryFactory(r"..\poetry\fascination.txt"))
    reactor.run()
