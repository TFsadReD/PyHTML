from logic.logic import PyHTML

site = PyHTML(name="index", title="Мой сайт", lang="ru", theme=True)

site.head_tag("meta", charset="UTF-8")
site.head_tag("link", rel="stylesheet", href="style.css")
site.head_tag("script", "console.log('Привет, PyHTML!');", self_closed=False)

site.standard_tag("h1", "PyHTML -> Лучшая библиотека")
site.standard_tag("p", "Создавай HTML без HTML!", style="color: gray;")

site.build_html("logic/templates/base.html")
