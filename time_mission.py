import time


if __name__ == '__main__':
    flag = True
    while True:
        if time.localtime().tm_hour == 0 and flag:
            import catch
            if not catch.main():
                import get_download_url
                get_download_url.main()
                import image_save
                left = image_save.main()
                # while left != 0:
                #     left = image_save.main(left)
                time.sleep(3)
                import send_email
                send_email.main("gmail")
            flag = False
        elif time.localtime().tm_hour == 16 and not flag:
            print("发送任务重置")
            flag = True
        time.sleep(30)
