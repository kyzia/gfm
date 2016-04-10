def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        maintext=email_message_instance.get_payload()
                
        return email_message_instance.get_payload()

def get_alltext_block(email_message_instance):
#    for part in email_message_instance.walk() 
    maintype = email_message_instance.get_content_maintype()
    returndict={}
    if maintype == 'multipart':
        num=0
        for part in email_message_instance.walk():
            charset = part.get_content_charset()
            if part.get_content_maintype() == 'text':
                string = part.get_payload(decode=1)
                if charset:
                    returndict[num]= convert2text(string.decode(charset))
                else:
                    returndict[num]= convert2text(string)
                num+=1
        return returndict
    elif maintype == 'text':
        charset = email_message_instance.get_content_charset()
        string=email_message_instance.get_payload(decode=1)
        returndict['0']=convert2text(string.decode(charset))
        return returndict

def download_attachments_in_email(email_message, outputdir):
    num=0
    returndict={}
    if email_message.get_content_maintype() != 'multipart':        
        return 'Maintype is not multipart'
    for part in email_message.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))
            returndict[num]=part.get_filename()
            num+=1
    return returndict

def convert2text(message):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(message)
    return soup.get_text('\n')
