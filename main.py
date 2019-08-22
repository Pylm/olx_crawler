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
    
    now = datetime.now()
    name = f'olx-{search.replace("+", "-")}-{now.year}-{now.hour}-{now.minute}-{now.second}'
    df.to_csv('olx-' + name + '.csv')
    print(f'Dataframe salvo em {getcwd()} como {name}.csv')
