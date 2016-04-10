#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, request
from json import loads, dumps
from yaml import load

from utils import get_first_text_block, download_attachments_in_email
import email
import imaplib

app = Flask(__name__)

CONF='config.conf'

with open(CONF) as f:
        conf = load("".join(f.readlines()))

ACCOUNTS_DICT=conf['cfg']['accounts']
print ACCOUNTS_DICT



@app.route("/api/getthefuckingmail", methods=('POST',))
def getthefuckingmaiil():
    print request
    if request.form:
        data, = request.form.keys()
    elif request.data:
        data = request.data

    data = loads(data)
#    data = loads(data)
#    return dumps(data)
    return getmail(data)


def getmail(data):
    account=data['account']
    server=ACCOUNTS_DICT[account]['server']
    login=ACCOUNTS_DICT[account]['login']
    password=ACCOUNTS_DICT[account]['password']

    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox", readonly=True) # connect to inbox.


    result, data = mail.uid('search', None, "(UNSEEN)") # search and return uids instead
    print data
    uid_list = data[0].split()
    uid_list.reverse()

    if not uid_list:
        return '{"Error":"empty_uidlist"}'
    print uid_list

    response_dict={}
    for uid in uid_list:
        response_dict[uid]={}
        result, datamail = mail.uid('fetch', uid, '(RFC822)')
        raw_email = datamail[0][1]
        email_message = email.message_from_string(raw_email)
        response_dict[uid]['text']=get_first_text_block(email_message)

        curent_dir='{0}/{1}/{2}'.format(os.getcwd(),account,uid)
        os.makedirs(curent_dir)

        response_dict[uid]['attachments']=download_attachments_in_email(email_message, curent_dir)
#        print
#    response_dict['attachments']=attach_dict
    return dumps(response_dict)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
