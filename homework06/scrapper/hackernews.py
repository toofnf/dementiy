import bottle
import numpy as np
from bottle import (
    route,
    run,
    template,
    redirect,
    request
)
from scrapper.settings import CLASS_MAPPER, COLORS_MAPPER
from scrapper.scraputils import get_news
from scrapper.db import News, session
from scrapper.bayes import NaiveBayesClassifier
from sklearn.model_selection import train_test_split

bottle.TEMPLATE_PATH.insert(0, '../templates')

seed = np.random.RandomState(239)


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows, use_color=False)


@route("/add_label/")
def add_label():
    s = session()
    # 1. Получить значения параметров label и id из GET-запроса
    id, label = request.query["id"], request.query["label"]

    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    item = s.query(News).get(id)

    # 3. Изменить значение метки записи на значение label
    item.label = label

    # 4. Сохранить результат в БД
    s.commit()
    d = request.query.get("cl")
    if d is not None:
        redirect('/classify')
    else:
        redirect('/news')


@route("/update", method=["POST"])
def update_news():
    n_pages = request.forms.get('page')
    n_pages = int(n_pages) if n_pages else 1

    s = session()

    # 1. Получить данные с новостного сайта

    parse_news = get_news(n_pages=n_pages)

    for news in parse_news:
        title, author = news['title'], news['author']

        # 2. Проверить, каких новостей еще нет в БД. Будем считать,
        #    что каждая новость может быть уникально идентифицирована
        #    по совокупности двух значений: заголовка и автора

        result = s.query(News).filter(
            News.title == title,
            News.author == author
        )

        if not list(result):
            new = News(
                title=title,
                author=author,
                url=news['url'],
                comments=news['comments'],
                points=news['points']
            )
            s.add(new)

    # 3. Сохранить в БД те новости, которых там нет
    s.commit()

    redirect("/news")


@route("/classify", method=["GET", "POST"])
def classify_news():
    s = session()
    train_data = s.query(News).filter(News.label != None).all()
    X = [news.title for news in train_data]
    y = [CLASS_MAPPER[news.label] for news in train_data]
    print(len(X), len(y))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )

    results = {}
    for alpha in [0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1]:
        naive_bayes = NaiveBayesClassifier(alpha=alpha)
        naive_bayes.fit(X_train, y_train)
        results[alpha] = naive_bayes.score(X_test, y_test)

    best_alpha = max(results, key=results.get)
    print(best_alpha, results[best_alpha])

    best_model = NaiveBayesClassifier(alpha=best_alpha)

    best_model.fit(X, y)

    test_data = s.query(News).filter(News.label == None).all()
    X_predict = [news.title for news in test_data]

    y_pred = best_model.predict(X_predict)

    ids = [i.id for i in test_data]
    classes = {2: [], 1: [], 0: []}

    for id, label in zip(ids, y_pred):
        classes[label].append(
            (
                s.query(News).filter(News.id == id).all()[0],
                COLORS_MAPPER[label]
            )
        )
    print(len(classes[2]))
    classified_news = classes[2] + classes[1] + classes[0]
    return template(
        'news_template',
        rows=classified_news,
        use_color=True
    )


if __name__ == "__main__":
    run(host="localhost", port=8080)
