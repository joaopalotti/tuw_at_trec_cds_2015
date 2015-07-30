#!/usr/bin/env python
from scoop import futures, shared
from readNXML import get_fields
import glob
import sys
import codecs

def process_doc(filepath):
    print "filepath", filepath
    journal_title, article_subjects, article_kwds, article_title, article_abstract, article_contents = get_fields(filepath)
    doc_id = filepath.strip().split("/")[-1].split(".")[0]

    s  = "<DOC>\n"
    s += "<DOCNO> "+ doc_id  +" </DOCNO>\n "
    if journal_title:
        s += "<JTITLE> "+ journal_title  +" </JTITLE>\n "
    if article_subjects:
        for sub in article_subjects:
            if sub:
                s += "<SUB> "+ sub  +" </SUB>\n "
    if article_kwds:
        for kwd in article_kwds:
            if kwd:
                s += "<KWD> "+ kwd  +" </KWD>\n "
    if article_title:
        s += "<ATITLE> "+ article_title  +" </ATITLE>\n "
    if article_abstract:
        s += "<ABSTRACT> "+ article_abstract  +" </ABSTRACT>\n "
    s += "<TEXT> "+ article_contents  +" </TEXT>\n"
    s += "</DOC>\n"

    destination = shared.getConst('destination')
    with codecs.open(destination + "/" + doc_id, encoding="utf-8", mode="w") as f:
        f.write(s)
    return True

if __name__ == "__main__":
    datapath = sys.argv[1] + "*.nxml"
    destination = sys.argv[2]

    print "Datapath: ", datapath

    nxmls = glob.iglob(datapath)
    shared.setConst(destination=destination)

    print "processed: ", len(list(futures.map(process_doc, nxmls)))


