#!/usr/bin/env python3

import sys

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from pyquery import PyQuery as pq

class TymoteuszBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        super(TymoteuszBot, self).__init__(jid, password)

        self.botname = 'Tymoteusz XMPP Bot'
        self.botver = '0.2.50-dev'

        self.nick = nick

        #self.register_plugin('xep_0030')    #Disco
        self.register_plugin('xep_0092')    #Version
        self.register_plugin('xep_0045')    #MUC

        # version
        self['xep_0092'].software_name = self.botname
        self['xep_0092'].version = self.botver

        # Identify
        #self['xep_0030'].add_identity(category='client',
        #                              itype='bot',
        #                              name=self.botname,
        #                              node='foo',
        #                              jid=self.boundjid.bare,
        #                              lang='no')


        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('groupchat_message', self.muc_message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        self.cmds(msg)

    def muc_message(self, msg):
        self.url_title(msg)

    def cmds(self, msg):
        if msg['body'].startswith('!'):
            cmdsplit = msg['body'].split(None, 1)

            if len(cmdsplit) == 2:
                cmd, arg = cmdsplit
            else:
                cmd = cmdsplit[0]

            if cmd == '!join':
                self.joinChat(arg)
            if cmd == '!leave':
                self.leaveChat(msg['mucroom'])

    def joinChat(self, room):
        self['xep_0045'].joinMUC(room,
                                 self.nick,
                                 wait=True)
        self.send_message(mto=room,
                          mbody='Witam!',
                          mtype='groupchat')

    def leaveChat(self, room):
        self.send_message(mto=room,
                          mbody='Żegnam!',
                          mtype='groupchat')
        self['xep_0045'].leaveMUC(room,
                                 self.nick,
                                 msg='A teraz drogie dzieci poczałujcie bota w dupę...')

    def url_title(self, msg):
        for word in msg['body'].split():
            if word.startswith(('http://', 'https://', '(http://', '(https://', '<http://', '<https://',
                                '[http://', '[https://', '{http://', '{https://')):
                try:
                    url = pq(url=word.strip('()<>[]{}'))
                    if url.is_('title'):
                        title = url('title').text()
                        self.send_message(mto=msg['mucroom'],
                                          mbody='[URL] ' + title,
                                          mtype='groupchat')
                except:
                    self.send_message(mto=msg['mucroom'],
                                      mbody='[URL] Nie można odczytać tytułu',
                                      mtype='groupchat')




if __name__ == '__main__':
    xmpp = TymoteuszBot(sys.argv[1], sys.argv[2], 'Tymoteusz-dev')

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')
