from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig 
import polyglotdb.io as pgio
import sys
import os


graph_db = {'host':'localhost', 'port': 7474}

path_to_switchboard = os.path.join("/Volumes","data","corpora","Switchboard_for_MFA")

if __name__ == '__main__':
    config = CorpusConfig("switchboard", **graph_db)
    print("loading corpus...")
    with CorpusContext(config) as g:
        g.reset()
        parser = pgio.inspect_fave(path_to_switchboard)
        g.load(parser, path_to_switchboard)

        q = g.query_graph(g.word).filter(g.word.label=="think")

        results = q.all()

        assert(len(results) > 0)


        q = g.query_graph(g.phone).filter(g.phone.label=="ow")
        results_phone = q.all()
        assert(len(results_phone) > 0 )