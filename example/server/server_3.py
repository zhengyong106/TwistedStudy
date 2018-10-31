from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class AnswerProtocol(LineReceiver):

    def __init__(self):
        self.answers = {b'How are you?': b'Fine', None: b"I don't know what you mean"}

    def lineReceived(self, line):
        if self.answers.get(line):
            self.sendLine(self.answers[line])
        else:
            self.sendLine(self.answers[None])

    def rawDataReceived(self, data):
        self.transport.write(data)


class AnswerFactory(Factory):

    def buildProtocol(self, addr):
        return AnswerProtocol()


# telnet 127.0.0.1 8234
if __name__ == '__main__':
    reactor.listenTCP(8234, AnswerFactory())
    reactor.run()
