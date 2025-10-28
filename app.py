from logic.logic import PyHTML

site = PyHTML(name="index", title="Мой сайт", lang="ru", theme=True)

site.container_tag("div", id="main", class_="container")

site.standard_tag("h1", "Добро пожаловать!", parent="main")
site.standard_tag("p", "Это пример вложенности", parent="main")

site.standard_tag("p", "Это пример ytdkj;tyyjcnb")
site.standard_tag("p", "Это пример вложенности", parent="main")

site.standard_tag("footer", "© 2025 PyHTML")

site.build_html("logic/templates/base.html")
