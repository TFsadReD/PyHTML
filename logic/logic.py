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


    def rebuild_data(self) -> dict:
        """Перезаписывает self.re_data актуальными данными объекта"""
        self.re_data = {
            "name": self.name,
            "title": self.title,
            "lang": self.lang,
            "theme": self.theme
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