
# I am using BM25 from Aldo's paper K1=2.5; B=0.55
#./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015A_summary_noexpansion_1_1_1.gz -q -Dtrec.model=BM25;
#./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015A_summary_expanded_1_1_1.gz -q -Dtrec.model=BM25; 
#./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015A_summary_expanded_2_1_3.gz -q -Dtrec.model=BM25;

./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015B_summary_noexpansion_1_1_1.gz -q -Dtrec.model=BM25;
./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015B_summary_expanded_1_1_1.gz -q -Dtrec.model=BM25; 
./bin/trec_terrier.sh -r -Dtrec.topics=/data/palotti/trec/metamap/2015B_summary_expanded_2_1_3.gz -q -Dtrec.model=BM25;

