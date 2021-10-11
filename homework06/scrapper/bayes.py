import math
import collections as c
from scrapper.cleaners import Cleaner, NaiveCleaner
from scrapper.utils import load_data


class NaiveBayesClassifier:

    def __init__(self,
                 alpha: float = 0.05,
                 cleaner: Cleaner = NaiveCleaner()):
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
            return prob

    def label_log_probability(self, label, sentence):
        log_prob_labels = (
            math.log(self.p_c[label])
        )
        log_prob_words = sum(
            (
                math.log(self.prob_wi_c(label, word))
                if self.prob_wi_c(label, word)
                else 0
            )
            for word in sentence.split()
        )
        return log_prob_labels + log_prob_words

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        # for feature in X:
        #     print([self.label_log_probability(feature, label) for label in [0, 1]])
        X_clean = self.cleaner.transform(X)
        answers = []
        for sentence in X_clean:
            prob = {label: self.label_log_probability(label, sentence)
                    for label in sorted(self.p_c.keys())}
            answers.append(max(prob, key=prob.get))
        return answers

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y_pred = self.predict(X_test)
        true_answers = sum([y_pr == y_tr for y_pr, y_tr in zip(y_pred, y_test)])
        return true_answers / len(y_test)


if __name__ == '__main__':
    X, y = load_data()

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    naive = NaiveBayesClassifier(
        alpha=0.05,
        cleaner=NaiveCleaner()
    )
    naive.fit(X_train, y_train)
    print(naive.score(X_test, y_test))
