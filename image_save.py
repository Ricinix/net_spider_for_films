import os
import re
import pandas as pd
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def main():
    films_pd = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
    for m in range(films_pd.shape[0]):
        print("正在下载第%d个图片" % m)
        r = requests.get(url=films_pd['image_url'][m], headers=headers)
        with open(os.path.join('.', 'images', '%s.jpg' % films_pd['name'][m]), 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    main()
