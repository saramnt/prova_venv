

from innolva_spider.business.URLinformations import LinksForMongo

class Article:

    def __init__(self, url, date, author, title, body):

        self.url = url
        self.date = date
        self.author = author
        self.title = title
        self.body = body


if __name__ == '__main__':

    prova = Article('https://www.lastampa.it/roma/2019/12/17/news/roma-militare-morta-nei-bagni-della-stazione-metro-flaminio-ora-chiusa-per-i-rilievi-si-ipotizza-un-suicidio-1.38222694')
    prova2 = Article('https://www.lastampa.it/cronaca/2019/12/15/news/litiga-con-il-marito-e-si-allontana-nel-bosco-con-i-bambini-paura-per-la-mamma-in-fuga-e-i-tre-piccoli-1.38214785')
    prova3 = Article('https://www.lastampa.it/viaggi/mondo/2019/10/23/news/l-etiopia-apre-ai-turisti-il-segretissimo-palazzo-imperiale-di-addis-abeba-1.37778661')

    database = LinksForMongo("localhost", 27017, "articles_mongodb")
    url = Article('https://www.lastampa.it/roma/2019/12/17/news/roma-militare-morta-nei-bagni-della-stazione-metro-flaminio-ora-chiusa-per-i-rilievi-si-ipotizza-un-suicidio-1.38222694')
    database.object_to_dict(url, "articles_collection")
