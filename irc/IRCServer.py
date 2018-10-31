import time
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.words.protocols.irc import IRC


class IRCServerProtocol(IRC):
    b = True
    def connectionMade(self):
        super().connectionMade()
        print("%s:%s is connected!" %  self.transport.client)

    def irc_NICK(self, prefix, params):
        if len(params) != 1:
            raise Exception('needmoreparams', 'NICK :Not enough parameters')

        if self.b:
            self.sendMessage("ERR_NICKNAMEINUSE", self.hostname)
            self.b = False

        self.nickname = params[0]

    def irc_USER(self, prefix, params):
        if len(params) != 4:
            raise Exception('needmoreparams', 'USER :Not enough parameters')
        self.username, self.hostname, self.servername, self.realname = params
        self.sendMessage("RPL_WELCOME", self.hostname)

    def irc_JOIN(self, prefix, params):
        self.join(self.username, params[0])
        self.privmsg("Bot", self.username, "hello! %s"%self.username)

    def irc_unknown(self, prefix, command, params):
        pass

class IRCServerFactory(Factory):
    def buildProtocol(self, addr):
        return IRCServerProtocol()

# telnet 127.0.0.1 8764
if __name__ == '__main__':
    # from twisted.internet import defer
    # from twisted.internet.selectreactor import SelectReactor
    # defer.Deferred()
    # SelectReactor().listenTCP()
    reactor.listenTCP(8764, IRCServerFactory())
    reactor.run()