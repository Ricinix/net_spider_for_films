import os
import re
import pandas as pd
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def main(left=0):
    films_pd = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
    path = os.path.join('.', 'images')
    if not os.path.exists(path):
        os.mkdir(path)
    for m in range(left, films_pd.shape[0]):
        print("正在下载第%d个图片" % m)
        try:
            r = requests.get(url=films_pd['image_url'][m], headers=headers)
        except Exception:
            return films_pd.shape[0] - m
        # r = requests.get(url=films_pd['image_url'][m], headers=headers)
        with open(os.path.join('.', 'images', '%s.jpg' % films_pd['name'][m]), 'wb') as f:
            f.write(r.content)

    return 0


if __name__ == '__main__':
    main()
