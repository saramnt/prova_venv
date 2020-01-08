
from innolva_spider.dao.UrlDAO import UrlDAO
from innolva_spider.dao.FileDAO import FileDAO

import time
import re
import requests
from urllib.parse import urlparse

from innolva_spider.business.ArticleBusiness import ArticleBusiness


class UrlBusiness():
    def __init__(self):
        self.url_dao = UrlDAO()
        self.file_dao = FileDAO()
        self.fileVisitati = "/home/sara/PycharmProjects/innolva-spider/innolva_spider/resources/url_visitati.txt"
        self.fileNonVisitati = "/home/sara/PycharmProjects/innolva-spider/innolva_spider/resources/url_nonVisitati.txt"
        self.fileScaricati = "/home/sara/PycharmProjects/innolva-spider/innolva_spider/resources/url_scaricati.txt"
        self.setArticles = set()


    def takeUrls(self, set_non_vis:set) -> set:
        setVis = self.file_dao.sync_set(self.fileVisitati)
        setUrls = set_non_vis.difference(setVis)
        for url in setUrls:
            self.file_dao.del_url(url, self.fileNonVisitati)
            try:
                setNonVis = set_non_vis.union(self.url_dao.getUrls(url))
            except:
                continue
            self.file_dao.add_url(url, self.fileVisitati)
            if ArticleBusiness(url).getBody():
                url_article = ArticleBusiness(url).article
                self.setArticles.add(url_article)
                ArticleBusiness(url).url_to_mongodb()
                self.file_dao.add_url(url, self.fileScaricati)

        print('lunghezza set articoli: ', len(self.setArticles))
        print(self.setArticles)
        print(len(set_non_vis))
        set_non_vis.difference_update(setUrls)
        print(len(set_non_vis))
        self.file_dao.sync_file(set_non_vis, self.fileNonVisitati)
        return set_non_vis






    def goDeep(self, livello:int, url:str = ""):
        if url:
            set_non_vis = self.url_dao.getUrls(url)
            self.file_dao.sync_file(set_non_vis, self.fileNonVisitati)
        else:
            set_non_vis = self.file_dao.sync_set(self.fileNonVisitati)
        print(len(set_non_vis))
        print(set_non_vis)
        while livello>0:
            setNonVis = self.takeUrls(set_non_vis)
            livello -= 1

        return self.setArticles




if __name__ == '__main__':


    prova = UrlBusiness()
    p = prova.goDeep(2, "https://www.lastampa.it/")

    # count = 0
    # for article in p:
    #     count += 1
    #     if count == 10:
    #         break
    #     print(article.url, article.date, article.author, article.title, article.body)

