./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2014_summary_noexpansion_1_1_1.gz -q -Dtrec.model=BM25 ;
./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2014_summary_expanded_1_1_1.gz -q -Dtrec.model=BM25 ;  
./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2014_summary_expanded_2_1_3.gz -q -Dtrec.model=BM25 ;

./bin/trec_terrier.sh -e

