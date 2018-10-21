#-*- coding:utf-8 -*-

import sys
import imaplib
import email
from email.header import decode_header, make_header

server="imap.gmail.com"
user="ky.cm010079@gmail.com"
password="cx0me33680113784"

try:
    Mm = imaplib.IMAP4_SSL(server)
    Mm.login(user,password)
    Mm.select()
    typ, data = Mm.search(None, 'UNSEEN')
    for num in data[0].split():
        typ, data = Mm.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
#
        email_from = str(make_header(decode_header(email_message['From'])))
        print(email_from)
        subject = str(make_header(decode_header(email_message['Subject'])))
        print(subject)

        date = str(make_header(decode_header(email_message['Date'])))
        print(date)

        msg_encoding = 'iso-2022-jp'

        if email_message.is_multipart() == False: # シングルパート
            try:
                msg_encoding = 'iso-2022-jp'
                byt  = bytearray(email_message.get_payload(), msg_encoding)
                body = byt.decode(encoding=msg_encoding)

            except Exception as ee:
                sys.stderr.write("*** error ***\n")
                sys.stderr.write(str(ee) + '\n')

        else:   # マルチパート
            try:
                msg_encoding = 'iso-2022-jp'
                prt  = email_message.get_payload()[0]
                byt  = prt.get_payload(decode=True)
                body = byt.decode(encoding=msg_encoding)
            except Exception as ee:
                msg_encoding = 'utf-8'
                prt  = email_message.get_payload()[0]
                byt  = prt.get_payload(decode=True)
                if(byt):
                    body = byt.decode(encoding=msg_encoding)
#
        print(body)
#
    Mm.close()
    Mm.logout()
except Exception as ee:
    sys.stderr.write("*** error ***\n")
    sys.stderr.write(str(ee) + '\n')

sys.stderr.write("*** 終了 ***\n")
