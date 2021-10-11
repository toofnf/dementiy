<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th colspan="3">Label</th>
                <form action="/update" method="post">
                    Amount of Pages: <input name="page" type="text" value=1 />
                    <input class="ui right floated small primary button" value="I Wanna more Hacker News!" type="submit" />
                </form>
                <form action="/classify" method="post">
                    <input class="ui green right floated small button" value="Generate recommendations" type="submit" />
                </form>
            </thead>
            <tbody>
                % if use_color==False:
                    %for row in rows:
                    <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}">Не интересно</a></td>
                    </tr>
                    % end
                % else:
                    %for row in rows:
                    <tr style="background-color:{{ row[1] }}">
                    <td><a href="{{ row[0].url }}">{{ row[0].title }}</a></td>
                    <td>{{ row[0].author }}</td>
                    <td>{{ row[0].points }}</td>
                    <td>{{ row[0].comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row[0].id }}&cl=yes">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row[0].id }}&cl=yes">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row[0].id }}&cl=yes">Не интересно</a></td>
                    </tr>
                    % end
                % end
            </tbody>

        </table>
        </div>
    </body>
</html>
