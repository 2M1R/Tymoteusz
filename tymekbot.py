#!/usr/bin/env python3

import sys

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from pyquery import PyQuery as pq

class TymoteuszBot(ClientXMPP):

    def __init__(self, jid, password, room, nick):
        super(TymoteuszBot, self).__init__(jid, password)

        self.botname = 'Tymoteusz XMPP Bot'
        self.botver = '0.2.30-dev'

        self.room = room
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
        #self.add_event_handler('message', self.message)
        self.add_event_handler('groupchat_message', self.muc_message)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self['xep_0045'].joinMUC(self.room,
                                 self.nick,
                                 wait=True)

    def message(self, msg):
        pass

    def muc_message(self, msg):
        self.url_title(msg)

    def url_title(self, msg):
        for word in msg['body'].split():
            if word.startswith(('http://', 'https://', '(http://', '(https://', '<http://', '<https://',
                                '[http://', '[https://', '{http://', '{https://')):
                try:
                    url = pq(url=word.strip('()<>[]{}'))
                    if url.is_('title'):
                        title = url('title').text()
                        self.send_message(mto=msg['mucroom'],
                                          mbody="[URL] " + title,
                                          mtype='groupchat')
                except:
                    self.send_message(mto=msg['mucroom'],
                                      mbody="[URL] Nie można odczytać tytułu",
                                      mtype='groupchat')




if __name__ == '__main__':
    xmpp = TymoteuszBot(sys.argv[1], sys.argv[2], 'n00b.code()@conf.netlab.cz', 'Tymoteusz')

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')
