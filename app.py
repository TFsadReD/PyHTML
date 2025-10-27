from logic.logic import PyHTML

site = PyHTML(name="index", title="Мой сайт", lang="ru", theme=True)

site.standard_tag("h1", "PyHTML -> Лучшая библиотека")
site.standard_tag("h2", "Добро пожаловать на мой сайт")
site.standard_tag("p", "Это пример абзаца", style="color: gray;")
site.standard_tag("a", "Перейти", href="https://google.com", target="_blank")

site.build_html("logic/templates/base.html")
