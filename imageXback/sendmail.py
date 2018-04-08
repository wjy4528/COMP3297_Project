import os
import datetime

emailpath = 'emailfiles'
email_from = 'info@imagex.tech'
time_str_format = '%y%m%d_%H%M%S'

if not os.path.isdir(emailpath):
    os.mkdir(emailpath)

def send_email(title, content, from_email, to_email):

    time_str = datetime.datetime.now().strftime(time_str_format)

    fp = os.path.join(emailpath, '{}_{}.txt'.format(to_email, time_str))

    with open(fp, 'w') as fw:
        fw.write( 'from : {}\nto : {} \ntitle : {}\ncontent: {}'.format(
            from_email, to_email, title, content) )
