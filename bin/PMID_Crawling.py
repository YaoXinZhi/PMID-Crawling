# -*- coding:utf-8 -*-
#! usr/bin/env python3
"""
Created on 04/04/2020 下午9:29 
@Author: xinzhi yao 
"""

import os
import bs4
import time
import string
import requests
import argparse
from bs4 import BeautifulSoup

def get_HTMLText(url):
    headers = {'User-Agent':'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36', 'Cookie':'ncbi_sid=47EF8993E4BE3193_0587SID; _ga=GA1.2.780797648.1582031800; pmc.article.report=; books.article.report=; _gid=GA1.2.288894097.1585885708; QSI_HistorySession=https%3A%2F%2Fwww.ncbi.nlm.nih.gov%2F~1585922167314; WebEnv=1zmWDqnmAX_v2YHx4rlkrq3Yhg3ZCIGss-UrAFg-SZPikri1ywXU5zjN2MwUgcrtonBWnvUs1EJyzzVzB2wC14pFkl6eh-708Vl%4047EF8993E4BE3193_0587SID; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgCIAYBC2ArAMIDMRAHGdmQCwCcAbEbm7mbgwOxEBiDWvzoA6AIwiAtnEogANCACuAOwA2AewCGqZVAAeAF0ygATJhABzAI6KoEAJ7yQZc5tWqndcwGcomiADGiE5E5hCKqlAAvIj2qBCaAD6oAEZRYIopklCoid7qioHRJMgGmgbI6soAylDK+RB5galRAAqZALI5iQb2YNH+FQGRiU5iXli+/kFOJrjmeISkFNS0jCzsHFy8AkJ8ohLSsgomYubWtg4YbqoYU4GIGOGRMXEJyWkZWd35hQHFpXKlRqdQaTQCLXaKS6uV6/Sig2QwygoxOZiwAHcsSJlAEUsgcapJDjkIgRBZ1DBZgxzGIGHMnJxabhKPMFGQzlg6Qz2eiQGJcEQXOyXFgDOEoIyJiBxbZGbIsIyaVgiELBTSFHR5lgmDwGJRQprRSBcCITJQRMKQHRpSoNNpdIZPKEsGyQELaawQtKGFqQkxaUwOCFuLSvAomJz+dxuLIAL5xoA'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def page_parser(url):
    html = get_HTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def title_pro(title: str):
    puncs = string.punctuation
    for punc in puncs:
        title = title.replace(punc, '')
    title = title.lower()
    return title

def title_punc_pro(title: str):
    # punc_rep = {'-': '-', '(': '%28', ',': '%2C', ')': '%29', '.': '.',
    #             ';': '%3B', "'": '%27', '/': '%2F', ':': '%3A', '+': '%2B',
    #             '{': '%7B', '}': '%7D', '?': '%3F', '"': ':', '>': '>',
    #             '&': '%26', '[': '%5B', ']': '%5D', '`': '%60', '_': '_',
    #             '\\': '%5C', '~': '~', '!': '%21', '#': '%23', '$': '%24',
    #             '%': '%25', "*": '*', '<': '<', '=': '%3D', '@': '%40',
    #             '^': '%5E', '|': '%7C'}
    # '%': '%25',
    punc_rep = {'(': '%28', ',': '%2C', ')': '%29', '+': '%2B',
                ';': '%3B', "'": '%27', '/': '%2F', ':': '%3A',
                '{': '%7B', '}': '%7D', '?': '%3F', '|': '%7C',
                '&': '%26', '[': '%5B', ']': '%5D', '`': '%60',
                '\\': '%5C', '!': '%21', '#': '%23', '$': '%24',
                '=': '%3D', '@': '%40', '^': '%5E'}
    puncs = list(punc_rep.keys())
    title = title.replace('%', '%25')
    for pun in puncs:
        if pun in title:
            title = title.replace(pun, punc_rep[pun])
    title = title.replace(' ', '+')
    return title


def extract_PMID(soup):
    try:
        for li in soup.find(attrs={'class':'ncbi-inline-list'}).children:
            if isinstance(li, bs4.element.Tag):
                if li.a['id'] == 'article_suppl_pmid':
                    PMID = li.a.string
        return PMID
    except:
        return 'None'

def main(abs_file: str, out: str):
    base_url = 'https://www.ncbi.nlm.nih.gov/search/all/?term='
    wf = open(out, 'w')
    wf.write('PMID\tTitle\tYear\tJournal\tAffiliation\tAbstract\tGene')
    count = 0
    match_count = 0
    start_time = time.time()
    with open(abs_file) as f:
        l = f.readline()
        for line in f:
            count += 1
            if count % 20 == 0:
                print('sleeping')
                time.sleep(5.8)
                end_time = time.time()
                print('已经爬取{0}篇PMID, 用时{1:.2f}s'.format(count, end_time-start_time))
            l = line.strip()
            title = l.split('\t')[0]
            # title = title_pro(title)
            title = title_punc_pro(title)
            url = base_url + title.replace(' ', '+')
            soup = page_parser(url)
            PMID = extract_PMID(soup)
            print(PMID)
            if PMID != 'None':
                match_count += 1
            wf.write('{0}\t{1}\n'.format(PMID, l))
    print('共找到{0}\{1}篇PMID, 用时{2:.2f}s.'.format(match_count, count, end_time-start_time))
    wf.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='PMID_Crawling')
    parser.add_argument('-ab', dest='abs_file', type=str, required=True)
    parser.add_argument('-o', dest='out', type=str, required=True)
    args = parser.parse_args()

    main(args.abs_file, args.out)



