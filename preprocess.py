# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 20:52:46 2015
preprocess.py reads the mbox file and creates a csv. 
It should be run only once.

@author: pdelboca
"""
import os
import mailbox
import csv
import email
import re
from progressbar import ProgressBar #ProgressBar2

path = os.path.dirname(os.path.abspath(__file__))

def get_domain(message):
    domain = ""
    match = re.search('\w+.com', message['from'])
    if match:
        domain = match.group()
    return domain


def get_message_from_id(message_id):
    for message in mail_box:
        if message['Message-ID'] == message_id:
            return message
    return None


def get_message_reply_dates(message):
    """If the message got replied, return the list of dates for all the 
        replies, else return empty list"""
    reply_dates = []
    for m in mail_box:
        if m['In-Reply-To'] == message['Message-ID']:
            reply_dates.append(m['date'])
    
    if not reply_dates:
        return []
    else:
        parsed_dates = [email.utils.parsedate(date) for date in reply_dates]
        return parsed_dates
        
def decode_header(headervalue): 
    """
       Decode message header and remove [pyar]  
    """    
    header_begin = headervalue.find("=")
    if header_begin == -1:
        headervalue = headervalue.replace("[pyar] ","")
    else:
        headervalue = headervalue[header_begin:]
    
    val,encoding = decode_header(headervalue)[0] 
    if encoding: 
        return val.decode(encoding) 
    else: 
        return val 
        
print "Reading mbox file and creating object..."
mbox_path = path + '/data/mbox.txt'
mail_box = mailbox.mbox(mbox_path)


print "Starting to write the csv file..."
csv_path = path + '/data/pyar.csv'
f = open(csv_path, 'wb')
writer = csv.writer(f, quoting=csv.QUOTE_ALL)

# Header row
writer.writerow(["member", "user_name", "subject", "date", "reply_date","amount_of_replies","domain"])
pbar = ProgressBar(maxval=len(mail_box)).start()
for i, message in enumerate(mail_box):
    #TODO: utf-8 encoding for subjects (ISSUE #3)
    subject = decode_header(message['subject']) #[8:] to remove [pyar] 
    member = email.utils.parseaddr(message['from'])[0]
    user_name = email.utils.parseaddr(message['from'])[1]
    domain = get_domain(message)
    #TODO: payload = get_payload(message) (ISSUE #4)
    date = message['date']
    reply_dates = get_message_reply_dates(message)
    if not reply_dates:
        first_reply_date = None
        amount_of_replies = 0
    else:
        first_reply_date = min(reply_dates)
        amount_of_replies = len(reply_dates)
    writer.writerow([member, user_name, subject, date, first_reply_date,amount_of_replies,domain])
    pbar.update(i)
f.close()
pbar.finish()

print "File created succesfully!"