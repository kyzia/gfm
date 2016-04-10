def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def download_attachments_in_email(email_message, outputdir):
    num=0
    returndict={}
    if email_message.get_content_maintype() != 'multipart':        
        return 'MAintype is not multipart'
    for part in email_message.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))
            returndict[num]=part.get_filename()
            num+=1
    return returndict

