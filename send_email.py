import os
import smtplib
import pandas as pd
import login_message
import requests

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.image import MIMEImage


receiver = login_message.RECEIVER

films = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def build_text():
    text = '<p>Hello！今天电影天堂又有新的电影资源了。</p>'
    for i in range(films.shape[0]):
        url = "详情地址：%s" % films['url'][i]
        name = '电影名：%s' % films['name'][i]
        download_url = '下载链接：%s' % films['download_url'][i]
        text = text + '\n<p><img src="cid:image%d"></p>' % i
        text = text + '\n<p><a href="%s">%s</a>\n</p><p><a href="%s">下载链接</a></p>' % (url, name, download_url)
    return text


def attach_image(i, read_picture):
    if read_picture:
        image_path = os.path.join('.', 'images', '%s.jpg' % films['name'][i])
        with open(image_path, 'rb') as f:
            msg_image = MIMEImage(f.read())
    else:
        download_image_fail, r = True, None
        while download_image_fail:
            try:
                r = requests.get(url=films['image_url'][i], headers=headers)
                download_image_fail = False
            except Exception:
                print("下载%s失败，正在重试..." % films['name'][i])
        msg_image = MIMEImage(r.content)

    msg_image.add_header('Content-ID', '<image' + str(i) + '>')
    return msg_image


def build_msg(read_picture, username):
    text = build_text()
    text_plain = MIMEText(text, 'html', 'utf-8')
    msg = MIMEMultipart('related')
    msg['Subject'] = '【新电影】'
    msg['From'] = formataddr(['电影推送', username])
    msg['To'] = receiver
    msg.attach(text_plain)
    for i in range(films.shape[0]):
        msg.attach(attach_image(i, read_picture))
    return msg


def delete_images(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))


def main(email_kind, read_picture=False):
    smtp, username, password = None, 0, 0
    if email_kind == "gmail":
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        username = login_message.USERNAME_GMAIL
        password = login_message.PASSWORD_GMAIL
    elif email_kind == "163":
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', 25)
        username = login_message.USERNAME_163
        password = login_message.PASSWORD_163

    smtp.login(username, password)
    print("登录成功")
    msg = build_msg(read_picture, username)
    print("邮件内容已生成")
    smtp.sendmail(username, receiver, msg.as_string())
    print("已成功发送邮件")
    smtp.quit()

    if read_picture:
        delete_images(os.path.join('.', 'images'))


if __name__ == '__main__':
    main("gmail")
