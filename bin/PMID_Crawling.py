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
            title = title_pro(title)
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

    # abs_file = '../data/reference.table.tail.txt'
    # out = '../data/reference_PMID.table.tail.txt'
    main(args.abs_file, args.out)


"""
- -
, %2C
( %28
) %29
. .
; %3B
' %27
/ %2F
Isolation and characterization of cDNA clones encoding cdc2 homologues from Oryza sativa: a functional homologue and cognate variants
Chalk5 encodes a vacuolar H+-translocating pyrophosphatase influencing grain chalkiness in rice
Cytochrome P450 family member CYP704B2 catalyzes the {omega}-hydroxylation of fatty acids and is required for anther cutin biosynthesis and pollen exine formation in rice
Cytochrome P450 family member CYP704B2 catalyzes the {omega}-hydroxylation of fatty acids and is required for anther cutin biosynthesis and pollen exine formation in rice
The same nuclear proteins bind to the 5?-flanking regions of genes for the rice seed storage protein: 16 kDa albumin, 13 kDa prolamin and type II glutelin
Morphological and molecular characterization of a new frizzy panicle mutant, "fzp-9(t)", in rice (Oryza sativa L.)
Structural and enzymatic characterization of Os3BGlu6, a rice beta-glucosidase hydrolyzing hydrophobic glycosides and (1->3)- and (1->2)-linked disaccharides
Heterologous expression of a rice syntaxin-related protein KNOLLE gene (<I>OsKNOLLE</I>) in yeast and its functional analysis in the role of abiotic stress
Two types of replication protein A 70 kDa subunit in rice, Oryza sativa: molecular cloning, characterization, and cellular & tissue distribution
A Rice HAL2-like Gene Encodes a Ca[IMAGE]-sensitive 3`(2`),5`-Diphosphonucleoside 3`(2`)-Phosphohydrolase and Complements Yeast met22 and Escherichia coli cysQ Mutations
A Rice HAL2-like Gene Encodes a Ca[IMAGE]-sensitive 3`(2`),5`-Diphosphonucleoside 3`(2`)-Phosphohydrolase and Complements Yeast met22 and Escherichia coli cysQ Mutations
A Rice HAL2-like Gene Encodes a Ca[IMAGE]-sensitive 3`(2`),5`-Diphosphonucleoside 3`(2`)-Phosphohydrolase and Complements Yeast met22 and Escherichia coli cysQ Mutations
Rice_Phospho 1.0: a new rice-specific SVM predictor for protein phosphorylation sites.
\Rice calcium-dependent protein kinase OsCPK17 targets plasma membrane intrinsic protein and sucrose phosphate synthase and is required for a proper cold stress response.
Chromatin states responsible for the regulation of differentially expressed genes under (60)Co~ ray radiation in rice.
"""

