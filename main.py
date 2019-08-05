#!/usr/bin/env python3

from sys import argv
from os import getcwd

from olx_crawler import OlxCrawler
from datetime import datetime

if __name__ == '__main__':
    if len(argv) > 1:
        args = ' '.join(argv[1:]).replace(' ', '+')
        search = args
    else:
        search = input('Termo de pesquisa: ')
        search = search.replace(' ', '+')

    crawler = OlxCrawler(search=search, state='br')
    html = crawler.get_html()
    soup = crawler.process_html(html)
    results = crawler.get_results(soup=soup)
    df = crawler.generate_df(results)
    df.to_csv('olx-' + str(datetime.now()) + '.csv')
    print(f'Dataframe salvo em {getcwd()} como olx-{str(datetime.now())}.csv')
    print(df)
