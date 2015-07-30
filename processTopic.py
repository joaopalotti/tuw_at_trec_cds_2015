from pymetamap import MetaMap
import sys
from bs4 import BeautifulSoup # process xml with topics
import gzip
import codecs
import re

mm = MetaMap.get_instance("/data/palotti/public_mm/bin/metamap13")

filename = sys.argv[1]
outputfile = sys.argv[2]
soup = BeautifulSoup(codecs.open(filename, "r"))
text_to_use = 1
append = True
onlyOne = True

expand_metamap = True
pweight = 1
tweight = 1
defaultweight = 1
diaweight = 3

def filterConcepts(concepts):
    query = set()
    for c in concepts:
        types = c.semtypes.strip("[]").split(",")
        #print c
        #print "Preferred:", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
        for t in types:
            if t == "clna":
                #print "Remedy: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "dsyn":
                #print "Disease: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "diap":
                #print "Diagnose", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "sosy":
                #print "Symptom: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "aggp":
                #print "Age: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "fndg":
                #print "Findings: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t == "bpoc":
                #print "Body Part: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t in ["anab", "comd", "emod", "mobd", "neop", "patf"]:
                #print "Disease2: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-1-")[0].strip('"')
                query.add(c)

            elif t in ['clnd', 'phsu', 'nnon', 'lipd', 'orch', 'chvs', 'horm', 'rcpt', 'topp', 'carb', 'irda', 'bodm', 'bacs', 'enzy', 'opco', 'eico', 'vita', 'antb', 'chvf', 'nsba', 'strd']:
                #print "Remedy2: ", c.preferred_name, "<> Trigger:", c.trigger.strip("[]").split("-tx-")[0].strip('"')
                query.add(c)
    return query

def weight_concepts(concept, pweight, tweight):
    cname = re.sub("[-&*()^%:,.]", " ", concept.preferred_name.lower())
    ctrigger = concept.trigger.strip("[]").split("-tx-")[0].strip('"').lower()
    ctrigger = re.sub("[-&*()^%:,.]", " ", ctrigger)

    query_str = ""
    for f in cname.split():
        query_str = query_str + " %s^%f " % (f, pweight)
        #query_str = query_str + " %s " % (f)

    for f in ctrigger.split():
        query_str = query_str + " %s^%f " % (f, tweight)
        #query_str = query_str + "%s " % (f)
    return query_str


def process_topic(topic, topic_num, diagnosis, outputfile="topics_trec_metamap.gz"):
    query_str = ""
    if expand_metamap:
        concepts, error = mm.extract_concepts([topic.replace("(","\\(").replace(")","\\)")]) #TODO: avoid using ()
        print "Found %d concepts" % (len(concepts))
        query = filterConcepts(concepts)
        for c in query:
            found_concepts = weight_concepts(c, pweight, tweight)
            print "Concepts in query: %s" % (found_concepts)
            query_str += found_concepts
    if diagnosis:
        print "Checking diagnosis: %s" % (diagnosis)
        if expand_metamap:
            dia_concepts, error = mm.extract_concepts([diagnosis.replace("(","\\(").replace(")","\\)")])
            print "Found %d diagnosis concepts" % (len(dia_concepts))
            dia_query = filterConcepts(dia_concepts)
            for c in dia_query:
                found_concepts = weight_concepts(c, pweight + diaweight, tweight + diaweight)
                print "Concepts in diagnosis: %s" % (found_concepts)
                query_str += found_concepts

        for f in diagnosis.split():
            query_str = query_str + " %s^%f " % (f.lower(), diaweight*2)

    if append:
        topic = re.sub("[-&*()^%:,.]", " ", topic)
        for f in topic.split():
            query_str = query_str + " %s^%f " % (f.lower(), defaultweight)
            #query_str = query_str + " %s " % (f)
        query_str = " ".join(query_str.split())

    if onlyOne:
        query_str = " ".join(set(query_str.split()))

    print "Resulting query: %s" % (query_str)
    if outputfile:
        with gzip.open(outputfile, "a") as f:
            f.write("<topic>\n")
            f.write("<number> %d <number>\n" % (topic_num))
            f.write("<type> anything </type>\n")
            f.write("<query> %s </query>\n" % (query_str))
            f.write("</topic>\n")

for topic in soup.findAll("topic"):
    topic_id = int(topic.get("number"))
    qtype = topic.get("type")

    diagnosis = None
    if topic.diagnosis:
        diagnosis = topic.diagnosis.getText()
    print "Diagnosis: %s" % (diagnosis)

    if text_to_use == 1:
        query = topic.summary.get_text()
        print "Using sumarry: %s" % (query)
    elif text_to_use == 2:
        query = topic.description.get_text()
        print "Using description: %s" % (query)
    else:
        print "ERROR - Please choose either summary (1) or description (2)"
        sys.exit(0)
    print "QUERY: ", query
    print "ID: ", topic_id
    process_topic(query, topic_id, diagnosis, outputfile)

