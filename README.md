Read unread messages through imap and get it via http interface.

Configure accounts (config.conf).
-------------------------
    cfg:
      accounts:
        testaccount:
        server: 'imap.gmail.com'
        login: 'smth@gmail.com'
        password: 'smth'
        rootAttachdir: '/core/git/gfm/mail_attachs'


Launch.
-------------------------
    sudo ./server.py

Use from another application.
-------------------------
    curl -d '{"account":"testaccount"}' http://localhost/api/getthefuckingmail

Answer.
-------------------------
    {"586": {"From": "Daria <king.king.1001@gmail.com>", "attachments": {"0": "6.jpg"}, "text": {"0": "Tot \r\n\r\n\r\n", "1": "Tot\u00a0"}, "To": "smth@gmail.com", "date": [2016, 4, 9, 17, 47, 31, 0, 1, -1], "Subject": "=?utf-8?B?0JXRidC1INC+0LTQuNC9INGC0LXRgdGC?="}, "587": {"From": "Google <no-reply@accounts.google.com>", "attachments": {"0": "google_logo_white_characters.png", "1": "title_blue_shield.png"}, "text": {"0": "New sign-in from Safari on iPhone\r\n\r\nDidn't get a new phone? Someone may have your password."},"To": "smth@gmail.com", "date": [2016, 4, 9, 12, 47, 31, 0, 1, -1], "Subject": "=?utf-8?B?0JXRidC1INC+0LTQuNC9INGC0LXRgdGC?="}}

Attachments will be downloaded to the specified rootdir (and /account_name/mail_uid/ path will be created).

    cd /core/git/gfm/mail_attachs; ls testaccount/586/
    
    6.jpg
