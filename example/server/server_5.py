from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class ChatProtocol(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GET_NAME"

    def connectionMade(self):
        self.sendLine(b"What's your name?")

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GET_NAME":
            self.handle_get_name(line)
        else:
            self.handle_chat(line)

    def rawDataReceived(self, data):
        self.transport.write(data)

    def handle_get_name(self, name):
        if name in self.users:
            self.sendLine(b"Name taken, please choose another.")
            return
        self.sendLine(b"Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_chat(self, message):
        message = b"<%s> %s" % (self.name, message)
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self.users)


# telnet 127.0.0.1 8123
if __name__ == '__main__':
    reactor.listenTCP(8123, ChatFactory())
    reactor.run()
