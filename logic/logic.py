from string import Template


class PyHTML:
    """In Progress..."""
    def __init__(self, name: str = "PyHTML", title: str = "PyHTML", lang: str = "ru", theme: bool = True):
        self.name = name
        self.title = title
        self.lang = lang
        self.theme = theme
        self.html = ""
        self.css = ""
        self.rebuild_data()


    @staticmethod
    def rw_files(name: str, mode: str, data: str | list[str] | None = None) -> str | None:
        """Функция для чтения или записи файлов"""
        match mode:
            case "r":
                with open(name, "r", encoding="utf-8") as f:
                    return f.read()

            case "w":
                if data is None:
                    raise ValueError("Write-Mode Error")
                if isinstance(data, list):
                    data = "".join(data)
                with open(name, "w", encoding="utf-8") as f:
                    f.write(data)
                return "Successful"

            case _:
                raise ValueError(f"Mode Error: {mode}")


    def standard_tag(self, tag: str = "h1", content: str = "PyHTML -> Лучшая библиотека", **attributes) -> None:
        """Функция создающая теги внутри -> body"""
        f_attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])

        if f_attributes:
            element = f"<{tag} {f_attributes}>{content}</{tag}>"
        else:
            element = f"<{tag}>{content}</{tag}>"

        self.re_data["body"] += element + "\n"


    def head_tag(self, tag: str, content: str = "", self_closed: bool = True, **attributes) -> None:
        """Создаёт тег внутри <head>"""
        f_attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])

        if self_closed:
            element = f"    <{tag} {f_attributes}>" if f_attributes else f"    <{tag}>"
        else:
            element = f"    <{tag} {f_attributes}>{content}</{tag}>" if f_attributes else f"    <{tag}>{content}</{tag}>"

        self.re_data["head"] += element + "\n"


    def rebuild_data(self) -> dict:
        """Перезаписывает self.re_data актуальными данными объекта"""
        old_body = getattr(self, "re_data", {}).get("body", "")
        old_head = getattr(self, "re_data", {}).get("head", "")

        self.re_data = {
            "name": self.name,
            "title": self.title,
            "lang": self.lang,
            "theme": self.theme,
            "head": old_head,
            "body": old_body
        }
        return self.re_data


    def build_html(self, template_path: str = "base.html"):
        """Создаёт HTML-файл на основе шаблона и данных из self.re_data"""
        try:
            template_content = self.rw_files(template_path, "r")

            template = Template(template_content)
            rendered_html = template.safe_substitute(self.re_data)
            output_name = f"{self.name}.html"

            self.rw_files(output_name, "w", rendered_html)
            self.html = rendered_html

            print(f"[OK] HTML-файл успешно создан: {output_name}")
            return output_name

        except FileNotFoundError:
            print(f"[Ошибка] Не найден шаблон: {template_path}")
        except Exception as e:
            print(f"[Ошибка] {e}")