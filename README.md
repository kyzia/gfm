Read unread messages through imap and get it via http interface.

Configure accounts (config.conf).

cfg:
  accounts:
    testaccount:
      server: 'imap.gmail.com'
      login: 'smth@gmail.com'
      password: 'smth'


Launch.

sudo ./server.py

Use from another application.

curl -d '{"account":"testaccount"}' http://localhost/api/getthefuckingmail

Answer.

{"586": {"text": "\r\n\r\nTot \r\n\r\n\r\n", "attachments": {"0": "6.jpg"}}, "588": {"text": "\r\n\r\nSmth \r\n\r\n\r\n", "attachments": {"0": "7.jpg"}}}

Attachments is downloaded to the workdir (and /account_name/mail_uid/ path will be created).

cd gfm; ls testaccount/586/

6.jpg
