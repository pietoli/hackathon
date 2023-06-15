import json
import re
import urllib.request
from typing import Dict

from bs4 import BeautifulSoup, Tag
from pydantic import BaseSettings
from serpapi import GoogleSearch


class SerpapiSettings(BaseSettings):
    api_key: str

    class Config:
        env_prefix: str = "serpapi_"

def only_letters(s: str):
    return re.sub(r'[\W_]', '', s.lower())

def only_letters_and_spaces(s: str):
    return re.sub(r'[^a-zA-Z\s,:]', ' ', s.lower())

config = SerpapiSettings()

def get_context(query: str)-> Dict[str,str]:

    params = {
        "api_key": config.api_key, # https://serpapi.com/manage-api-key
        "engine": "google_scholar",  # profile results search engine
        "q":f"{query} site:ncbi.nlm.nih.gov",  # search query
        "num": 5,
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    ncbi_urls = {}

    for result in results['organic_results']:
        url = result.get("link")
        if url is not None and "ncbi" in url:
           ncbi_urls[url] = result.get("title")

    abstract_results = {}
    for title in list(ncbi_urls.values()):
        title = only_letters_and_spaces(title)
        search_term = "+".join([el for el in title.split()])
        search_url = f'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/' + \
                     f'?db=pubmed' + \
                     f'&retmode=json' + \
                     f'&retmax=1000' + \
                     f'&term={search_term}' + \
                     f'&field=title'
        link_list = urllib.request.urlopen(search_url).read().decode('utf-8')
        result = json.loads(link_list)
        id_list = result['esearchresult']['idlist']
        if len(id_list)==0:
            print('no articles for title')
        else:
            id_list = ",".join(id_list[:20])

            summary_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/esummary.fcgi?db=pubmed&id={id_list}&retmode=json'
            summary_list = urllib.request.urlopen(summary_url).read().decode('utf-8')
            summary = json.loads(summary_list)

            try:
                uid = [x for x in summary['result'] if x != 'uids']
                titles = [summary['result'][x]['title'] for x in summary['result'] if x != 'uids']

                real_pmid = [pmid for real_title, pmid in zip(titles, uid) if only_letters(real_title) == only_letters(title)][
                0]

                abstract_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/efetch.fcgi?db=pubmed&id={real_pmid}'
                abstract_ = urllib.request.urlopen(abstract_url).read().decode('utf-8')
                abstract_bs = BeautifulSoup(abstract_, features="xml")
                articles_iterable = abstract_bs.find_all('PubmedArticle')
                abstract_texts = [x.find('AbstractText').text if isinstance(x.find('AbstractText'), Tag) else '' for x in
                                  articles_iterable]

                abstract_results[title] = abstract_texts[0]
            except:
                print("Pmid not found")


    print(abstract_results)
    return abstract_results


