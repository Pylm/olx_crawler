#!/usr/bin/env python3

import bs4
import pandas as pd
import requests
from numpy import mean, nan


class OlxCrawler:

    """Class for the OLX web scrapper, gets the results, process
    and output a pandas dataframe """

    def __init__(self, search, state, url=''):
        """Inicia as variáveis necessárias para operação do programa
        search = Pesquisa a ser realizada
        state = Estado no qual a pesquisa será realizada, utilize br
        para pesquisar em todo Brasil"""

        self.search = search
        self.state = state

        if state != 'br'.lower():
            url = 'https://' + self.state + '.olx.com.br/?q=' + self.search
        else:
            url = 'https://' + 'olx.com.br/brasil?q=' + self.search

        self.url = url

    def get_html(self):

        """Requests the main results page"""

        page = requests.get(self.url)
        page.raise_for_status()
        return page

    def process_html(self, html):

        """Process the requested page into a BeautifulSoup element
        HTML = the requested page thar get_html returned"""

        soup = bs4.BeautifulSoup(html.text, features='lxml')
        return soup

    def get_results(self, soup, parser='lxml'):
        """Gets the processed page and crawls every result link on it,
        then proceds to append those links, titles and prices to a dictionary

        SOUP = BeautifulSoup object
        PARSER = The parser to be used by BeautifulSoup"""

        titles = []
        prices = []
        links = []

        print("\x1b[2J")

        links_soup = soup.findAll('a', {'class': 'OLXad-list-link'}, href=True)

        progress = 0

        print('Pesquisando...')

        for i, link in enumerate(links_soup):
            page = requests.get(link['href'])
            soup = bs4.BeautifulSoup(page.text, features=parser)
            cur_title = soup.findAll('div', {'class': 'OLXad-title-box'})

            progress = 100 / (int(len(links_soup))) * i

            print('\r', end='', flush=True)
            print(f'\033[7;36m[{"#" * int(progress)}{" " * (100 - int(progress))}]\033[27m \
                  {progress:.2f}%', end='', flush=True)

            if cur_title == []:
                cur_title = soup.findAll('h1', {'id': 'ad_title'})
            elif cur_title == []:
                cur_title = soup.findAll('h1', {'class': 'OLXad-title'})

            cur_price = soup.findAll('span', {'class': 'OLXad-price'})

            try:
                titles.append(cur_title[0].text.strip())
            except IndexError:
                titles.append(nan)

            try:
                prices.append(int(cur_price[0].text.
                                  replace('R$', '').replace('.', '').strip()))
            except IndexError:
                prices.append(0)
            try:
                links.append(link['href'])
            except IndexError:
                links.append(nan)

        print('\u001b[0m')
        print("\x1b[2J")
        results = {'Título': titles, 'Preço': prices, 'Link': links}
        return results

    def generate_df(self, data, remove_outliers=True, deviation=1):

        """
        Takes the dictionary returned earlier and turns it
        into a pandas dataframe
        DATA = The dictionary to be used
        REMOVE_OUTLIERS = Boolean value, if true tries to remove outliers
        based on the median price
        DEVTIATION = Percentage variation from the median to be
        considered an outlier, only effective if REMOVE_OUTLIERS=True
        """

        df = pd.DataFrame(data)
        df.replace(0, nan, inplace=True)

        med = df['Preço'].median()

        if remove_outliers:
            for i, price in enumerate(df['Preço']):
                outlier = abs(med - price) / mean([med, price])

                if outlier > deviation:
                    df.drop(i, inplace=True)

        df.dropna(inplace=True)
        df.reset_index(inplace=True, drop=True)

        return df
