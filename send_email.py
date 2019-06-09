import os
import smtplib
import pandas as pd
import login_message

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


username = login_message.USERNAME
password = login_message.PASSWORD
receiver = login_message.RECEIVER


def build_text():
    text = "Hello！今天电影天堂又有新的电影资源了。\n"
    films = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
    for i in range(films.shape[0]):
        url = "详情地址：%s" % films.iloc[i][0]
        name = '电影名：%s' % films.iloc[i][1]
        download_url = '下载链接：%s' % films.iloc[i][2]
        text = text + "\n%s    %s\n%s" % (name, url, download_url)
    return text


def build_msg():
    text = build_text()
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【新电影】'
    msg['From'] = formataddr(['电影推送', username])
    msg['To'] = receiver
    msg.attach(text_plain)
    return msg


def main():
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.ehlo()
    # smtp.starttls()
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com', 25)
    smtp.login(username, password)
    msg = build_msg()
    smtp.sendmail(username, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    main()
