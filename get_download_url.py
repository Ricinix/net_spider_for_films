import re
import os
import requests
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def main():
    films_pd = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
    # print(type(films_pd.iloc[0]['url']))
    # print(type(films_pd[0: 1]['url']))
    urls = films_pd['url']
    download = []
    image = []
    for url in urls:
        r = requests.get(url=url, headers=headers)
        r.encoding = re.search('(?<=charset=).*?(?=")', r.text).group()
        download.append(re.search('magnet:.*?(?=")', r.text).group())
        image.append(re.search('http.*?\.jpg', r.text).group())
    films_pd['download_url'] = download
    films_pd['image_url'] = image
    print(films_pd)
    films_pd.to_csv(os.path.join('.', 'data', 'films.csv'), index=False)


if __name__ == '__main__':
    main()
