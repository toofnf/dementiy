import math
import string
import csv
import typing as tp
import collections as c
import itertools
from definitions import DATA_DIR


class Cleaner(object):

    def transform(self, sentence):
        raise NotImplementedError


class NaiveCleaner(Cleaner):

    def transform(self, X):
        def clean(s):
            translator = str.maketrans("", "", string.punctuation)
            return s.translate(translator)

        return [clean(x).lower() for x in X]


class NaiveBayesClassifier:

    def __init__(self, alpha, cleaner: NaiveCleaner):
        self.alpha = alpha
        self.cleaner = cleaner
        self.d = 0
        self.p_c = c.defaultdict(int)
        self.n_c = c.Counter()
        self.n_ic = c.defaultdict(int)
        self.sum_per_label = c.defaultdict(int)
        self.label_type = None

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        X_clean = self.cleaner.transform(X)
        for sentence, label in zip(X_clean, y):
            self.p_c[label] += 1
            words = sentence.split()
            self.n_c.update(words)
            for word in words:
                self.n_ic[label, word] += 1

        for label in self.p_c:
            self.p_c[label] /= len(X)
            self.sum_per_label[label] = sum(
                [v for k, v in self.n_ic.items() if k[0] == label]
            )

        self.d = len(self.n_c)
        self.label_type = type(y[0])

    def prob_wi_c(self, label, word):
        if word not in self.n_c:
            return 0
        else:
            prob = (
                    (self.n_ic[label, word] + self.alpha) /
                    (self.sum_per_label[label] + self.alpha * self.d)
            )
            return math.log(prob)

    def label_log_probability(self, label, sentence):
        log_prob_labels = (
            math.log(self.p_c[label])
        )
        log_prob_words = sum((self.prob_wi_c(label, word))
                             for word in sentence.split())
        return log_prob_labels + log_prob_words

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        # for feature in X:
        #     print([self.label_log_probability(feature, label) for label in [0, 1]])
        answers = []
        for sentence in X:
            prob = {label: self.label_log_probability(label, sentence)
                    for label in sorted(self.p_c.keys())}
            answers.append(max(prob, key=prob.get))
        return answers

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        X_test_clean = self.cleaner.transform(X_test)
        y_pred = self.predict(X_test_clean)
        true_answers = sum([y_pr == y_tr for y_pr, y_tr in zip(y_pred, y_test)])
        return true_answers / len(y_test)


if __name__ == '__main__':
    X_train = [
        "I love this sandwich",
        "This is an amazing place",
        "I feel very good about these beers",
        "This is my best work",
        "What an awesome view",
        "I do not like this restaurant",
        "I am tired of this stuff",
        "I can't deal with this",
        "He is my sworn enemy",
        "My boss is horrible"
    ]
    y_train = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]

    X_test = [
        "The beer was good",
        "I do not enjoy my job",
        "I ain't feeling dandy today",
        "I feel amazing",
        "Gary is a friend of mine",
        "I can't believe I'm doing this"
    ]
    y_test = [1, 0, 0, 1, 1, 0]

    naive = NaiveBayesClassifier(
        alpha=1,
        cleaner=NaiveCleaner()
    )
    naive.fit(X_train, y_train)

    print(naive.score(X_test, y_test))

    with open(str(DATA_DIR / "SMSSpamCollection"), 'r', encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter="\t"))

    X, y = [], []

    for target, msg in data:
        X.append(msg)
        y.append(target)

    X = NaiveCleaner().transform(X)

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    naive = NaiveBayesClassifier(
        alpha=0.05,
        cleaner=NaiveCleaner()
    )
    naive.fit(X_train, y_train)
    print(naive.score(X_test, y_test))
    #
    # from sklearn.naive_bayes import MultinomialNB
    # from sklearn.pipeline import Pipeline
    # from sklearn.feature_extraction.text import TfidfVectorizer
    #
    # model = Pipeline([
    #     ('vectorizer', TfidfVectorizer()),
    #     ('classifier', MultinomialNB(alpha=0.05)),
    # ])
    #
    # model.fit(X_train, y_train)
    # print(model.score(X_test, y_test))
