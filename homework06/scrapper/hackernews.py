import bottle
from bottle import (
    route,
    run,
    template,
    redirect,
    request
)
from scrapper.scraputils import get_news
from scrapper.db import (
    News,
    session,
)

bottle.TEMPLATE_PATH.insert(0, '../templates')


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


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

    redirect("/news")


@route("/update")
def update_news():
    s = session()

    # 1. Получить данные с новостного сайта

    parse_news = get_news()

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


@route("/classify")
def classify_news():
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
