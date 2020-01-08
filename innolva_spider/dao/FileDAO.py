import shutil
from tempfile import NamedTemporaryFile


class FileDAO():


    def sync_set(self, text):
        s=set()
        try:
            urlFile = open(text, "r")
            for link in urlFile:
                s.add(link.strip("\n"))
            # self.set = self.set.union(self.set)
        except:
            text = open(text, "w+")
        return s


    def del_url(self, url, text):
        filename = text
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        with open(text, mode='r') as f:
            for line in f:
                if line.strip('\n') != url:
                    tempfile.write(line)
        shutil.move(tempfile.name, filename)

    def add_url(self, url, text):
        with open(text, 'a+') as f:
            f.write(url + '\n')


    def sync_file(self, set_sync, text):
        with open(text, "w") as f:
            for url in set_sync:
                f.write(url + "\n")


if __name__ == '__main__':

    prova = FileDAO()
    file = open("/home/sara/PycharmProjects/innolva-spider/innolva_spider/resources/url_visitati.txt", "r")
    # prova.checkFile(file)


