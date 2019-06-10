import time
import catch
import get_download_url
import image_save
import send_email


if __name__ == '__main__':
    flag = True
    while True:
        if time.localtime().tm_hour == 0 and flag:
            if not catch.main():
                get_download_url.main()
                left = image_save.main()
                while left != 0:
                    left = image_save.main(left)
                send_email.main()
                print("今日已发送")
            flag = False
        elif time.localtime().tm_hour == 16 and not flag:
            print("发送任务重置")
            flag = True
        time.sleep(30)
