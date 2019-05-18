import os
import pickle
import csv
import json
from loader import Loader


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.
        Args:
          guid: Unique id for the example.
          text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
          text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
          label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label


class InputFormatting(object):
    def __init__(self):
        self.wikidir = './wiki-pages-text'
        self.indexdir = './IndexFiles.index'
        self.datadir = './data'
        self.pickledir = './pickles'
        self.loader = Loader(self.wikidir, self.indexdir, self.datadir)

    def convert_traindev_to_input_example(self, max_sample, is_trainset=True):
        if is_trainset:
            pickle_file_dir = os.path.join(self.pickledir, 'train%s.txt' % max_sample)
            if not os.path.exists(pickle_file_dir):
                df = self.loader.train_dev_loader(max_sample=max_sample)
                with open(pickle_file_dir, 'wb') as f:
                    pickle.dump(df, f)

            else:
                with open(pickle_file_dir, 'rb') as f:
                    df = pickle.load(f)
            print(df)
            print(df.columns)
            input_examples = df.apply(lambda x: InputExample(guid=x['index'],
                                                             text_a=x['claim'],
                                                             text_b=x['evidence'],
                                                             label=x['label']), axis=1)
            return input_examples
        else:
            pickle_file_dir = os.path.join(self.pickledir, 'dev%s.txt' % max_sample)
            if not os.path.exists(pickle_file_dir):
                df = self.loader.train_dev_loader(max_sample=max_sample, is_trainset=False)
                with open(pickle_file_dir, 'wb') as f:
                    pickle.dump(df, f)

            else:
                with open(pickle_file_dir, 'rb') as f:
                    df = pickle.load(f)
            input_examples = df.apply(lambda x: InputExample(guid=x['index'],
                                                             text_a=x['claim'],
                                                             text_b=x['evidence'],
                                                             label=x['label']), axis=1)
            return input_examples

    def convert_test_to_input_example(self):
        pickle_file_dir = os.path.join(self.pickledir, 'test.txt')
        if not os.path.exists(pickle_file_dir):
            df = self.loader.test_loader()
            with open(pickle_file_dir, 'wb') as f:
                pickle.dump(df, f)
        else:
            with open(pickle_file_dir, 'rb') as f:
                df = pickle.load(f)
            input_examples = df.apply(lambda x: InputExample(guid=x['index'],
                                                             text_a=x['claim'],
                                                             text_b=x['evidence'],
                                                             label='NOT ENOUGH INFO'), axis=1)
            return input_examples


class OutputFormatting(object):
    def __init__(self):
        self.outputdir = './output'
        self.pickledir = './pickles'
        self.labels = ['SUPPORTS', 'REFUTES', 'NOT ENOUGH INFO']

    def convert_output_to_json(self):
        labels = []
        with open(os.path.join(self.outputdir, 'test_results.tsv')) as f:
            output = csv.reader(f, delimiter='\t')
            for line in output:
                label = self.labels[line.index(max(line))]
                labels.append(label)

        #labels = [labels[i: i + 10] for i in range(0, len(labels) - 9, 3)]
        pickle_file_dir = os.path.join(self.pickledir, 'test.txt')
        with open(pickle_file_dir, 'rb') as f:
            df = pickle.load(f)

        output = {}
        for i in range(0, len(labels) - 9, 10):
            sub = labels[i: i + 10]
            f = list(filter(lambda x: x[1] == 'SUPPORTS', enumerate(sub)))
            if len(f) > 0:
                evidences = [df.loc[[i + j[0]], 'docname'].values[0] for j in f]

                output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                 'label': 'SUPPORTS',
                                                                 'evidence': evidences}
            else:
                f = list(filter(lambda x: x[1] == 'REFUTES', enumerate(sub)))
                if len(f) > 0:
                    evidences = [df.loc[[i + j[0]], 'docname'].values[0] for j in f]
                    output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                     'label': 'REFUTES',
                                                                     'evidence': evidences}
                else:
                    output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                     'label': 'NOT ENOUGH INFO',
                                                                     'evidence': []}

        with open(os.path.join(self.outputdir, 'test_results.json'), 'w') as f:
            json.dump(output, f)









#outputformatting = OutputFormatting()
#outputformatting.convert_output_to_json()
inputformatting = InputFormatting()
inputformatting.convert_traindev_to_input_example(500)



