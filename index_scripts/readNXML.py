from bs4 import BeautifulSoup
import codecs
#filename = "../raw-files/00/2649282.nxml"

def get_fields(filename, utf8=True):
#Info extracted:
#   journal_title
#   article_name
#   article_subjects
#   article_abstract
#   article_contents
    if utf8:
        soup = BeautifulSoup(codecs.open(filename, encoding="utf-8", mode="r"))
    else:
        soup = BeautifulSoup(open(filename))

    journal_title = None
    article_subjects = None
    article_title = None
    article_abstract = None
    article_contents = ""
    article_kwds = None

    if soup.front:
        front = soup.front.extract()
        if front.find("journal-title"):
            journal_title = front.find("journal-title").get_text()
        if front.find("subject"):
            article_subjects = [sub.string for sub in front.find_all("subject")]
        if front.find("article-title"):
            article_title = front.find("article-title").get_text()
        if front.find('abstract'):
            article_abstract = front.find('abstract').get_text(" ")
        if front.find("kwd"):
            article_kwds = [sub.string for sub in front.find_all("kwd")]

    #ignored by now...it contains references
    #if soup.back:
    #    back = soup.back.extract()

    if soup.body:
        body = soup.body.extract()
        article_contents = body.get_text(" ")

    return [journal_title, article_subjects, article_kwds, article_title, article_abstract, article_contents]

