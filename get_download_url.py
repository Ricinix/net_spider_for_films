import pandas as pd
import requests
import re


def main():
    films_pd = pd.read_csv('.\\data\\films.csv')
    # print(type(films_pd.iloc[0]['url']))
    # print(type(films_pd[0: 1]['url']))
    urls = films_pd['url']
    download = []
    for url in urls:
        r = requests.get(url = url)
        r.encoding = re.search('(?<=charset=).*?(?=")', r.text).group()
        download.append(re.search('magnet:.*?(?=")', r.text).group())
    films_pd['download_url'] = download
    print(films_pd)
    films_pd.to_csv('.\\data\\films.csv', index=False)


if __name__ == '__main__':
    main()