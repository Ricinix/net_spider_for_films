import catch
import get_download_url
import image_save


if __name__ == '__main__':
    catch.main()
    get_download_url.main()
    left = image_save.main()
    while left != 0:
        left = image_save.main(left)
