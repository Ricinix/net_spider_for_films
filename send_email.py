import pandas as pd
import smtplib
import email


username = 'XXX@163.com'
password='XXX'
receiver='XXX@163.com'


def main():
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com,25')
    smtp.login(username, password)
    smtp.sendmail(username, receiver, msg.as_string())


if __name__ == '__main__':
    main()