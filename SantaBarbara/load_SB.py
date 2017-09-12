from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig 
import polyglotdb.io as pgio
import sys
import os


graph_db = {'host':'localhost', 'port': 7474}

path_to_SB = os.path.join("/Volumes","data","corpora","SantaBarbara_aligned", "Part2_aligned")

if __name__ == '__main__':
    config = CorpusConfig("santabarbara_part2", **graph_db)
    print("loading corpus...")
    with CorpusContext(config) as g:
        g.reset()
        parser = pgio.inspect_fave(path_to_SB)
        g.load(parser, path_to_SB)

        q = g.query_graph(g.word).filter(g.word.label=="think")

        results = q.all()

        assert(len(results) > 0)


        q = g.query_graph(g.phone).filter(g.phone.label=="ow")
        results_phone = q.all()
        assert(len(results_phone) > 0 )