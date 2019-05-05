
# ======================== Indexer imports ========================
import sys, os, threading, time
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

# ======================= Retriever imports =======================
from org.apache.lucene.index import DirectoryReader
from org.apache.pylucene.queryparser.classic import PythonMultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher, BooleanClause
from org.apache.lucene.search.similarities import BM25Similarity


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class SearchEngine(object):

    def __init__(self, root, storedir, isindexing=False, isBM25=True):

        if not os.path.exists(storedir):
            os.mkdir(storedir)

        self.analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)

        if isindexing:
            store = SimpleFSDirectory(Paths.get(storedir))
            config = IndexWriterConfig(self.analyzer)
            # TODO BM25 parameter tuning
            if isBM25:
                config.setSimilarity(BM25Similarity())
            config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
            writer = IndexWriter(store, config)

            self.indexer(root, writer)
            ticker = Ticker()
            print('commit index')
            threading.Thread(target=ticker.run).start()
            writer.commit()
            writer.close()
            ticker.tick = False
            print('done')

        search_dir = SimpleFSDirectory(Paths.get(storedir))
        self.searcher = IndexSearcher(DirectoryReader.open(search_dir))
        if isBM25:
            self.searcher.setSimilarity(BM25Similarity())

    def indexer(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        def repalcer(text):
            chars = '\\`*_{}[]()>#+-.!$‘'
            for c in chars:
                if c in text:
                    text = text.replace(c, ' ')
            return text

        for root, dirnames, filenames in os.walk(root):
            i = 0
            for filename in filenames:
                i += 1
                with open(os.path.join(root, filename)) as f:
                    for line in f.readlines():
                        line = line.split(' ', 2)
                        docname = line[0] + ' ' + line[1]
                        name = repalcer(line[0])
                        contents = line[2]
                        doc = Document()
                        doc.add(Field('docname', docname, t1))
                        doc.add(Field('name', name, t1))
                        doc.add(Field('contents', contents, t1))
                        writer.addDocument(doc)
                print('File %d done indexing' % i)

    def search(self, query, topk):
        qp = PythonMultiFieldQueryParser(['name', 'contents'], self.analyzer)
        query = qp.parse(query, ['name', 'contents'],
                         [BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD], self.analyzer)
        print(query)
        scores = self.searcher.search(query, topk).scoreDocs
        print('%s total matching documents.' % len(scores))

        docnames = []
        doccontents = []
        for score in scores:
            doc = self.searcher.doc(score.doc)
            docnames.append(doc.get('docname'))
            doccontents.append(doc.get('contents'))

        return docnames, doccontents
