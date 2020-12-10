import math
import sys
import time

import metapy
import pytoml
import csv

class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        tfn = sd.doc_term_count * math.log(( 1 + sd.avg_dl/sd.doc_size),2)
        c = 1
        score = sd.query_term_weight * (tfn/(tfn + c)) * math.log( ((sd.num_docs + 1) / (sd.corpus_term_count + 0.5)) , 2)
        #return (self.param + sd.doc_term_count) / (self.param * sd.doc_unique_terms + sd.doc_size)
        return score

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate, e.g. return InL2Ranker(some_param=1.0) 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index. You can ignore this for MP2.
    """

    return metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=500)
    #return metapy.index.PivotedLength()
    #return metapy.index.AbsoluteDiscount()
    #return metapy.index.JelinekMercer()
    #return metapy.index.DirichletPrior()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1] #system input of what the argument is
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 1000
    query_path = query_cfg.get('query-path', 'queries_simplified.txt')
    query_start = query_cfg.get('query-id-start', 0)
    print(query_start)

    idx.metadata

    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file, \
         open('predictions.txt' , mode='w', errors='ignore') as f_out:

        for query_num, line in enumerate(query_file):
            ## query_num is the number of the query, need to add 1 since
            ## it's actually 1 indexed
            ## line is the actual query
            
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            
            for num, (d_id, score) in enumerate(results):
                ## UID accesed with idx.metadata(d_id).get('uid')
                ## scores is the given score, but I think we're supposed to be giving integers
                uid = idx.metadata(d_id).get('uid')
                f_out.write(str(query_num + 1) + " " + uid + " " + str(float(score)) + '\n')

            avg_p = ev.avg_p(results, query_start + query_num + 1, top_k)

            #print("Query {} average precision: {}".format(query_num + 1, avg_p))
            #print("{}".format(avg_p))
            
    print("Mean average precision: {}".format(ev.map()))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
    ev.map()
