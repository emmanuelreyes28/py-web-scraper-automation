'''
use source venv/bin/activate to activate virtual environment 
use deactive to turn off virtual environment 
'''
import re
import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# website being requested
BASE_URL = 'https://remoteok.com/api/'

# user agent lets website know to respond by determinig the device in use
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

# send request to website and return contents in json format


def get_job_postings():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return res.json()


def output_jobs_to_xls(data):
    wb = Workbook()  # create new excel wb
    job_sheet = wb.add_sheet('Jobs')  # create new sheet
    # grab keys from json object to use as headers
    headers = list(data[0].keys())

    # add each header to a column within row 0 of job_sheet
    for i in range(0, len(headers)):
        job_sheet.write(0, i, headers[i])  # (row 0, col i, value)

    # add contents to each row repectively to col header
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            job_sheet.write(i + 1, x, str(values[x]))

    wb.save('remote_jobs.xls')


def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()
    smtp.login(send_from, '')  # enter account psswd
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)
    send_email('dummyaccount557@yahoo.com', ['xxxxxxxx@gmail.com'], 'Jobs Posting',
               'Please, find attached a list of job postings to this email', files=['remote_jobs.xls'])
