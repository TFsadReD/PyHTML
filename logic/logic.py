from string import Template


class PyHTML:
    """In Progress..."""
    def __init__(self, name: str = "PyHTML", title: str = "PyHTML", lang: str = "ru", theme: bool = True, tabs: bool = True):
        self.name = name
        self.title = title
        self.lang = lang
        self.theme = theme

        self.html = ""
        self.css = ""
        self.tabs = tabs
        self.diversity_tabs = "\t" if tabs else "    "

        self.containers = {}

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


    def container_tag(self, tag: str = "div", *, id: str, parent: str | None = None, **attributes) -> None:
        """Функция создающая теги-контейнеры, в которые можно класть другие теги, внутри -> body"""
        if id in self.containers:
            raise ValueError(f"Контейнер с id='{id}' уже существует.")

        f_attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
        open_tag = f"<{tag} id=\"{id}\" {f_attributes}>".strip()
        self.containers[id] = {"open": open_tag, "content": "", "close": f"</{tag}>", "parent": parent}


    def standard_tag(self, tag: str = "h1", content: str = "PyHTML -> Лучшая библиотека", parent: str | None = None, **attributes) -> None:
        """Функция создающая теги внутри -> body или внутри контейнера"""
        f_attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
        element = f"<{tag} {f_attributes}>{content}</{tag}>" if f_attributes else f"<{tag}>{content}</{tag}>"

        if parent:
            if parent not in self.containers:
                raise ValueError(f"Контейнер с id='{parent}' не найден.")
            self.containers[parent]["content"] += element + "\n"

        else:
            self.re_data["body"] += f"{self.diversity_tabs}{element}\n"


    def head_tag(self, tag: str, content: str = "", self_closed: bool = True, **attributes) -> None:
        """Создаёт тег внутри -> head"""
        f_attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])

        if self_closed:
            element = f"    <{tag} {f_attributes}>" if f_attributes else f"    <{tag}>"
        else:
            element = f"    <{tag} {f_attributes}>{content}</{tag}>" if f_attributes else f"    <{tag}>{content}</{tag}>"

        self.re_data["head"] += element + "\n"


    def rebuild_data(self) -> dict:
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


    def format_html(self, html: str, level: int = 1) -> str:
        """Форматирует HTML с отступами"""
        indent = self.diversity_tabs * level
        lines = [line.strip() for line in html.strip().splitlines() if line.strip()]
        return "\n".join(f"{indent}{line}" for line in lines)


    def build_container(self, container_id: str, level: int = 1) -> str:
        """Рекурсивно строит контейнер с учётом вложенности"""
        container = self.containers[container_id]
        indent = self.diversity_tabs * level

        inner_html = container["content"].strip()

        nested_html = "\n".join(
            self.build_container(child_id, level + 1)
            for child_id, c in self.containers.items()
            if c["parent"] == container_id
        )

        full_inner = ""
        if inner_html:
            full_inner += self.format_html(inner_html, level + 1)
        if nested_html:
            if full_inner:
                full_inner += "\n"
            full_inner += nested_html

        return f"{indent}{container['open']}\n{full_inner}\n{indent}{container['close']}"


    def build_html(self, template_path: str = "base.html"):
        """Создаёт HTML-файл на основе шаблона"""
        try:
            for container_id, container in self.containers.items():
                if container["parent"] is None:
                    container_html = self.build_container(container_id, level=1)
                    self.re_data["body"] += container_html + "\n"

            lines = [ln for ln in self.re_data["body"].splitlines()]

            prefixed = []
            for ln in lines:
                if not ln.strip():
                    continue
                if ln.startswith(self.diversity_tabs):
                    prefixed.append(ln)
                else:
                    prefixed.append(f"{self.diversity_tabs}{ln.lstrip()}")

            self.re_data["body"] = "\n".join(prefixed) + "\n"


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