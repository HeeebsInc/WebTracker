import smtplib
import datetime
from emailverifier import Client

linespace = '---------------------------------------------------------------------------------------------------'
email_verifier_key = 'at_egFaAwKfOX6NCnj4oElHwwIFkR5j2'


def email_sender(*args, **kwargs):#(dictionary, email, total_changes):
    dictionary = kwargs.get('dictionary', None)
    email = kwargs.get('email', None)
    total_changes = kwargs.get('total_changes', None)

    date = datetime.datetime.now()
    day = date.day
    month = date.month
    year = date.year
    message_list = []
    timestamp = f'Website Report: {month}/{day}/{year}'
    #print('\n\n\n')
    for name in dictionary.items():
        for i in name:
            message_list.append(i)
        #message_list.append('\n\n\n')

    #print(message_list)

    word_list = []
    word_list.append('\t\t\tWORD REPORT')
    for position, item in enumerate(message_list):
        if position == 0:
            word_list.append(f'\n{linespace}\n')
            word_list.append(f'\t\t\t{item}')
            word_list.append(f'New Words\t\t\t\t\tOld Words')
            word_list.append('(Word\tCount)\t\t\t\t(Word\tCount)')  # -New')
            continue
        elif position % 2 == 0:
            word_list.append(f'\n\n\n{linespace}\n')
            word_list.append(f'\t\t\t{item}')
            word_list.append(f'New Words\t\t\t\t\tOld Words')
            word_list.append('(Word\tCount)\t\t\t\t(Word\tCount)')#-New')
            continue
        else:
            for key, value in item.items():
                #print(key,value)
                if value.get('New') == 'N':
                    row = f'\t\t\t\t\t{key.capitalize()}\t{value.get("Count")}'#{value.get("New")}'
                    word_list.append(row)
                    continue
                else:

                    row = f'{key.capitalize()}\t+{value.get("Count")}'#//{value.get("New")}'
                    word_list.append(row)
                    continue
    email_message = '\n'.join(word_list)
    #print(email_message)

    if kwargs.get('email', None) == None: #if there is no email --> only for console view
        return(True,email_message)
        #print(position, item)
    else:
        # creates SMTP session
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login("LilyScraper@gmail.com", "Lilyscraper555!")

            # message to be sent
            message = "Message_you_need_to_send"

            # sending the mail
            s.sendmail("LilyScraper@gmail.com", f'{email}', f'Subject: {total_changes} Total Changes {timestamp} \n\n {email_message}')

            # terminating the session
            s.quit()

            statement = f'Successfully Sent Email.... There were a total of {total_changes} changes across your websites'
            return (True, statement)
        except:
            #raise
            statement = 'We could not send the email.  An error occurred when trying to connect to LilyScraper@gmail.com'
            return (False,statement)






def email_verifer(email):
    client = Client(email_verifier_key)
    valid_statement = 'This is a valid email'
    error_statement = 'This is an invalid email... Check your input and try again'
    try:
        data = client.get(email)
        return (True,valid_statement) if data.smtp_check == True else (False,error_statement)

    except:
        #raise
        return (False,error_statement)

