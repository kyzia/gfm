#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, request
from json import loads, dumps
from yaml import load

from utils import get_first_text_block, download_attachments_in_email,get_alltext_block,convert2text
import email
import imaplib

app = Flask(__name__)

CONF='config.conf'

with open(CONF) as f:
        conf = load("".join(f.readlines()))

ACCOUNTS_DICT=conf['cfg']['accounts']



@app.route("/api/getthefuckingmail", methods=('POST',))
def getthefuckingmaiil():
    if request.form:
        data, = request.form.keys()
    elif request.data:
        data = request.data
    data = loads(data)
    print("Request is: {0}".format(data))
    return getmail(data)


def getmail(data):
    account=data['account']
    rootAttachdir=ACCOUNTS_DICT[account]['rootAttachdir']
    server=ACCOUNTS_DICT[account]['server']
    login=ACCOUNTS_DICT[account]['login']
    password=ACCOUNTS_DICT[account]['password']

    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox", readonly=True) # connect to inbox.

    result, data = mail.uid('search', None, "(UNSEEN)") # search and return uids instead
    uid_list = data[0].split()
    print uid_list
    uid_list.reverse()

    if not uid_list:
        return '{"Error":"empty_uidlist"}'

    response_dict={}
    for uid in uid_list:
        response_dict[uid]={}
        result, datamail = mail.uid('fetch', uid, '(RFC822)')
        raw_email = datamail[0][1]
        email_message = email.message_from_string(raw_email)
        response_dict[uid]['text']=get_alltext_block(email_message)

        curent_dir='{0}/{1}/{2}'.format(rootAttachdir,account,uid)
        if not os.path.exists(curent_dir):
            os.makedirs(curent_dir)

        response_dict[uid]['attachments']=download_attachments_in_email(email_message, curent_dir)
        response_dict[uid]['date']=email.utils.parsedate(email_message.get('date'))        
        response_dict[uid]['Subject']=email.header.decode_header(email_message.get('Subject'))
        response_dict[uid]['From']=email_message.get('From')
        response_dict[uid]['To']=email_message.get('To')
    return dumps(response_dict)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
