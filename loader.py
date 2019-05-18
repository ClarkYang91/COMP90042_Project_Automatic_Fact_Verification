import os
import pandas as pd
import unicodedata
# TODO inicodedata used for form Latin characters
from datetime import datetime
import json
import lucene
from index_retrieval import SearchEngine


class Loader(object):

    def __init__(self, root, storedir, datadir):
        self.datadir = datadir
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.search_engine = SearchEngine(root, storedir)

    def train_dev_loader(self, max_sample=float('inf'), is_trainset=True):
        if is_trainset:
            dir = os.path.join(self.datadir, 'train.json')
        else:
            dir = os.path.join(self.datadir, 'devset.json')

        with open(dir) as f:
            data = json.loads(f.read())
            sup_examples, ref_examples, nei_examples = [], [], []
            c = 0
            for i, d in list(data.items()):
                try:
                    if d['label'] == 'SUPPORTS':
                        for e in d['evidence']:
                            if len(sup_examples) < max_sample:
                                _, content = self._retrieve(e)
                                sup_examples.append([c, i, d['claim'], content.strip(), d['label']])
                                c += 1
                                if c % 50 == 0:
                                    print('%d examples loaded' % c)
                    elif d['label'] == 'REFUTES':
                        for e in d['evidence']:
                            if len(ref_examples) < max_sample:
                                _, content = self._retrieve(e)
                                ref_examples.append([c, i, d['claim'], content.strip(), d['label']])
                                c += 1
                                if c % 50 == 0:
                                    print('%d examples loaded' % c)
                    else:
                        if len(nei_examples) < max_sample:
                            _, content = self._search(d['claim'])
                            content = content[0]
                            nei_examples.append([c, i, d['claim'], content.strip(), d['label']])
                            c += 1
                            if c % 50 == 0:
                                print('%d examples loaded' % c)
                    if len(sup_examples) == max_sample and len(ref_examples) == max_sample \
                            and len(nei_examples) == max_sample:
                        break
                except Exception:
                    continue
        samples = sup_examples + ref_examples + nei_examples
        df = pd.DataFrame(samples, columns=['index', 'id', 'claim', 'evidence', 'label'])

        return df.sample(frac=1).reset_index(drop=True)

    def test_loader(self):
        dir = os.path.join(self.datadir, 'test-unlabelled.json')
        with open(dir) as f:
            data = json.loads(f.read())
            examples = []
            c = 0
            for i, d in list(data.items())[:5]:
                claim = d['claim']
                docnames, contents = self._search(claim)
                for j in range(len(docnames)):
                    examples.append([c, i, claim, docnames[j], contents[j].strip()])
                    c += 1
        return pd.DataFrame(examples, columns=['index', 'id', 'claim', 'docname', 'evidence'])

    def _retrieve(self, e):

        term, sid = e[0], e[1]
        return self.search_engine.retrieve(term, sid)

    def _search(self, q):

        return self.search_engine.search(q, 10)

