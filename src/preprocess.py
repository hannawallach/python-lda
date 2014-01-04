import argparse, csv, re
from corpus import *
from numpy import *

def create_stopword_list(f):

    if not f:
        return set()

    if isinstance(f, basestring):
        f = file(f)

    return set(word.strip() for word in f)

def tokenize(data, stopwords=set()):

    tokens = re.findall('[a-z]+', data.lower())

    return [x for x in tokens if x not in stopwords]

def main():

    # parse command-line arguments

    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', metavar='input-file', help='CSV file to be preprocessed')
    parser.add_argument('--remove-stopwords', metavar='stopword-file', help='remove stopwords provided in the specified file')
    parser.add_argument('--output-file', metavar='output-file', help='save preprocessed data to the specified file')

    args = parser.parse_args()

    # create stopword list

    stopwords = create_stopword_list(args.remove_stopwords)

    # preprocess data

    corpus = Corpus()

    for name, label, data in csv.reader(open(args.input_file), delimiter='\t'):
        corpus.add(name, tokenize(data, stopwords))

    print '# documents =', len(corpus)
    print '# tokens =', sum(len(doc) for doc in corpus)
    print '# unique types =', len(corpus.alphabet)

    if args.output_file:
        corpus.save(args.output_file)

if __name__ == '__main__':
    main()
