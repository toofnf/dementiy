import unittest
from scrapper.bayes import NaiveBayesClassifier
from scrapper.utils import load_data
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


class TestNaiveBayesClassifier(unittest.TestCase):
    def setUp(self):
        self.const = 1e-3
        self.X_train = [
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
        self.y_train = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]

        self.X_test = [
            "The beer was good",
            "I do not enjoy my job",
            "I ain't feeling dandy today",
            "I feel amazing",
            "Gary is a friend of mine",
            "I can't believe I'm doing this"
        ]
        self.y_test = [1, 0, 0, 1, 1, 0]

        self.naive_bayes = NaiveBayesClassifier(alpha=1)
        self.naive_bayes.fit(self.X_train, self.y_train)

    def test_prior_probability_for_labels(self):
        labels = self.naive_bayes.p_c
        equals = [
            labels[0] == 0.5,
            labels[1] == 0.5
        ]
        for test in equals:
            with self.subTest():
                self.assertTrue(test)

    def test_length_of_dictionary(self):
        self.assertEqual(self.naive_bayes.d, 36)

    def test_count_words_per_label_positive(self):
        """
        https://stackoverflow.com/questions/32899/how-do-you-generate-dynamic-parameterized-unit-tests-in-python
        """
        words = [
            'about', 'am', 'amazing', 'an', 'awesome', 'beers',
            'best', 'boss', 'cant', 'deal', 'do', 'enemy',
            'feel', 'good', 'he', 'horrible', 'i', 'is',
            'like', 'love', 'my', 'not', 'of', 'place',
            'restaurant', 'sandwich', 'stuff', 'sworn', 'these', 'this',
            'tired', 'very', 'view', 'what', 'with', 'work'
        ]
        count_positive = [
            1, 0, 1, 2, 1, 1,
            1, 0, 0, 0, 0, 0,
            1, 1, 0, 0, 2, 2,
            0, 1, 1, 0, 0, 1,
            0, 1, 0, 0, 1, 3,
            0, 1, 1, 1, 0, 1
        ]

        count_negative = [
            0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1,
            0, 0, 1, 1, 3, 2,
            1, 0, 2, 1, 1, 0,
            1, 0, 1, 1, 0, 3,
            1, 0, 0, 0, 1, 0
        ]

        count_per_label = self.naive_bayes.n_ic
        for word, count_pos, count_neg in zip(words,
                                              count_positive,
                                              count_negative):
            with self.subTest():
                self.assertEqual(count_per_label[1, word], count_pos)
                self.assertEqual(count_per_label[0, word], count_neg)

    def test_probability_of_word_per_label(self):
        probability_of_word = self.naive_bayes.prob_wi_c
        words = ['beer', 'amazing']
        prob_positive = [0, 0.032]
        prob_negative = [0, 0.016]
        for word, pos, neg in zip(words,
                                  prob_positive,
                                  prob_negative):
            with self.subTest():
                self.assertTrue(
                    abs(probability_of_word(1, word) - pos) <= self.const
                )
                self.assertTrue(
                    abs(probability_of_word(0, word) - neg) <= self.const
                )

    def test_amount_of_words_per_label(self):
        sum_per_labels = self.naive_bayes.sum_per_label
        equals = [
            sum_per_labels[0] == 26,
            sum_per_labels[1] == 25
        ]
        for test in equals:
            with self.subTest():
                self.assertTrue(test)

    def test_log_probability(self):
        log_prob = self.naive_bayes.label_log_probability
        X_test_clean = self.naive_bayes.cleaner.transform(self.X_test)
        dummy = X_test_clean[0]
        equals = [
            abs(log_prob(0, dummy) - (-4.820)) <= self.const,
            abs(log_prob(1, dummy) - (-4.110)) <= self.const,
        ]
        for test in equals:
            with self.subTest():
                self.assertTrue(test)

    def test_predict(self):
        y_pred = self.naive_bayes.predict(self.X_test)
        self.assertTrue([1, 0, 0, 1, 0, 0] == y_pred)

    def test_score(self):
        score = self.naive_bayes.score(self.X_test, self.y_test)
        self.assertEqual(score, 5 / 6)


class TestNaiveBayesClassifierOnData(unittest.TestCase):
    def setUp(self):
        self.X, self.y = load_data()

    def test_score_bayes(self):
        for alpha in [0.05, 0.1, 0.5, 1]:
            naive_bayes = NaiveBayesClassifier(alpha=alpha)

            sklearn_model = Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', MultinomialNB(alpha=alpha)),
            ])
            X_train, y_train, X_test, y_test = (
                self.X[:3900], self.y[:3900], self.X[3900:], self.y[3900:]
            )
            naive_bayes.fit(X_train, y_train)
            score_my_model = naive_bayes.score(X_test, y_test)

            sklearn_model.fit(X_train, y_train)
            score_sklearn_model = sklearn_model.score(X_test, y_test)
            equals = [
                score_my_model >= 0.982,
                score_my_model >= score_sklearn_model
            ]
            for test in equals:
                with self.subTest():
                    self.assertTrue(test)
