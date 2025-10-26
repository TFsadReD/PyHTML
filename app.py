from logic.logic import PyHTML

site = PyHTML(name="index", title="Мой сайт", lang="ru", theme=True)
site.build_html("logic/templates/base.html")
