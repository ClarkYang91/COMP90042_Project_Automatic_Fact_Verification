import os, sys, lucene
from Project.idx_retrl import SearchEngine

INDEX_DIR = 'IndexFiles.index'

# wiki pages folder must be put under root path
WIKI_FLDR_NAME = 'wiki-pages-text'

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
wiki_dir = os.path.join(base_dir, WIKI_FLDR_NAME)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
search_engine = SearchEngine(wiki_dir, os.path.join(base_dir, INDEX_DIR), isindexing=True)

q = 'Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.'
docnames, doccontents = search_engine.search(q, 10)

for i in range(len(docnames)):
    print(docnames[i])
    print(doccontents[i])

