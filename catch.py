import os
import re
import requests
import pandas as pd


original_url = 'https://www.dytt8.net/'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def main():
    path = os.path.join('.', 'data')
    if not os.path.exists(path):
        os.mkdir(path)

    r = requests.get(url = original_url, headers=headers)
    coding_style = re.search('(?<=charset=).*?(?=")', r.text).group()
    r.encoding = coding_style

    latest_films = re.findall('(?<=最新电影下载</a>\]).*?<.a>', r.text)

    url_list = []
    name_list = []
    for film in latest_films:
        # data = re.search("(?<=href=')(.*?)'>(.*?)<", film)
        data = re.search("(?<=href='/)(?P<url>.*?)'>(?P<name>.*?)<", film)
        # films_pd['url'] = data.group(1)
        # films_pd['name'] = data.group(2)
        url_list.append(original_url + data.group('url'))
        name_list.append(re.sub('/', ' ', data.group('name')))

    films_pd = pd.DataFrame()
    films_pd['url'] = url_list
    films_pd['name'] = name_list
    print(films_pd)

    try:
        films_old = pd.read_csv(os.path.join('.', 'data', 'films.csv'))
    except FileNotFoundError:
        print("第一次抓取")
        return False

    if films_pd['url'].to_list() == films_old['url'].to_list():
        print("已是最新")
        return True
    else:
        films_pd.to_csv(os.path.join('.', 'data', 'films.csv'), index=False)
        return False


if __name__ == '__main__':
    main()
