import requests
import re
import pandas as pd


original_url = 'https://www.dytt8.net/'


def main():
    is_same = False
    r = requests.get(url = original_url)
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
        name_list.append(data.group('name'))

    films_pd = pd.DataFrame()
    films_pd['url'] = url_list
    films_pd['name'] = name_list
    print(films_pd)

    try:
        films_old = pd.read_csv('.\\data\\films.csv')
    except FileNotFoundError:
        print("第一次抓取")
        is_same = True

    if not is_same and films_pd['url'].to_list() == films_old['url'].to_list():
        print("已是最新")
        return True
    else:
        films_pd.to_csv('.\\data\\films.csv', index=False)
        return False


if __name__ == '__main__':
    main()
