import os
import smtplib
import pandas as pd
import login_message

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.image import MIMEImage


username = login_message.USERNAME
password = login_message.PASSWORD
receiver = login_message.RECEIVER

films = pd.read_csv(os.path.join('.', 'data', 'films.csv'))


def build_text():
    text = '<p>Hello！今天电影天堂又有新的电影资源了。</p>'
    for i in range(films.shape[0]):
        url = "详情地址：%s" % films['url'][i]
        name = '电影名：%s' % films['name'][i]
        download_url = '下载链接：%s' % films['download_url'][i]
        text = text + '\n<p><img src="cid:image%d"></p>' % i
        text = text + '\n<p><a href="%s">%s</a>\n</p><p><a href="%s">下载链接</a></p>' % (url, name, download_url)
    return text


def attach_image(i):
    image_path = os.path.join('.', 'images', '%s.jpg' % films['name'][i])
    # with open(image_path, 'rb') as f:
    #     msg_image = MIMEImage(f.read())
    f = open(image_path, 'rb')
    msg_image = MIMEImage(f.read())
    f.close()
    msg_image.add_header('Content-ID', '<image' + str(i) + '>')
    return msg_image


def build_msg():
    text = build_text()
    text_plain = MIMEText(text, 'html', 'utf-8')
    msg = MIMEMultipart('related')
    msg['Subject'] = '【新电影】'
    msg['From'] = formataddr(['电影推送', username])
    msg['To'] = receiver
    msg.attach(text_plain)
    for i in range(films.shape[0]):
        msg.attach(attach_image(i))
    return msg


def delete_images(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))


def main():
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com', 25)
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.ehlo()
    # smtp.starttls()
    smtp.login(username, password)
    msg = build_msg()
    smtp.sendmail(username, receiver, msg.as_string())
    smtp.quit()

    delete_images(os.path.join('.', 'images'))


if __name__ == '__main__':
    main()
