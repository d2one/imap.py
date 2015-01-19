# -*- coding: utf8 -*-
"""
Module displaying the number of unread messages
on an IMAP inbox (configurable).

@author obb
"""

import imaplib
from time import time


class Py3status:

    # available configuration parameters
    cache_timeout = 60
    imap_server = 'YOUR_IMAP_SERVER'
    name = '@'
    password = 'YOUR_PASS'
    port = '143'
    user = 'YOUR_LOGIN'

    def check_mail(self, i3s_output_list, i3s_config):
        mail_count = self._get_mail_count()
        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': '{}: {}'.format(self.name, mail_count)
        }

        new_mail_color = i3s_config['color_good']
        check_failed_color = i3s_config['color_bad']

        if mail_count == 'N/A':
            response['color'] = check_failed_color
        elif mail_count != '0':
            response['color'] = new_mail_color
        return response

    def _get_mail_count(self):
        unseen_messages = 0;
        try:
            imap = imaplib.IMAP4(self.imap_server)
            imap.login(self.user, self.password)
            folders = [folder.split(' "/" ')[1] for folder in imap.list()[1]]
            for box in folders:
                typ, data = imap.select(box)
                typ, data = imap.search(None, 'UNSEEN')
                unseen_messages += len(data[0].split())
                
            imap.logout()
            return unseen_messages
        except:
            return 'N/A'

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    while True:
        print(x.check_mail([], {}))
        sleep(1)
