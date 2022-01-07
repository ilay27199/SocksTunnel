#!/usr/bin/env python3

from twisted.web import server
from twisted.internet import reactor

from tunneling.server.server import Server


def main():
    s = server.Site(Server())
    reactor.listenTCP(9990, s)
    reactor.run()


if __name__ == '__main__':
    main()
