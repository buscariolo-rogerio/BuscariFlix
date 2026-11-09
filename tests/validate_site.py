"""Validação sem dependências externas para o site estático."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.images_without_alt = 0
        self.has_refresh = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img" and not values.get("alt"):
            self.images_without_alt += 1
        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.has_refresh = True
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append(values[attribute])


def is_local(reference):
    return urlsplit(reference).scheme == "" and not reference.startswith(("#", "//", "mailto:", "tel:"))


def validate_html(path):
    parser = ReferenceParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = []
    if parser.images_without_alt:
        errors.append(f"{parser.images_without_alt} imagem(ns) sem texto alternativo")
    if parser.has_refresh:
        errors.append("recarregamento automático não permitido")
    for reference in filter(is_local, parser.references):
        clean_path = unquote(urlsplit(reference).path).lstrip("/")
        if clean_path and not (ROOT / clean_path).is_file():
            errors.append(f"arquivo local ausente: {reference}")
    return errors


def main():
    errors = []
    for html_file in HTML_FILES:
        errors.extend(f"{html_file.name}: {message}" for message in validate_html(html_file))

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for required in ('id="movie-search"', 'class="movie-card"', 'src="app.js"'):
        if required not in index:
            errors.append(f"index.html: recurso obrigatório ausente: {required}")

    if errors:
        raise SystemExit("Falha na validação:\n- " + "\n- ".join(errors))
    print(f"Validação concluída: {len(HTML_FILES)} páginas HTML e seus arquivos locais estão corretos.")


if __name__ == "__main__":
    main()
