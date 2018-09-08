import re
from bs4 import BeautifulSoup

from . import actions
from .urls import normalise_url, is_absolute_url


def get_file_handler(extension):
    if extension == ".html":
        return HtmlFileContent

    if extension == ".css":
        return CssFileContent


class FileContent:
    def __init__(self, url, path, content, grabber):
        self.url = url
        self.path = path
        self.grabber = grabber
        self.content = content

        self._unresolved_dependencies = {}
        self._actions = []

    def has_pending_dependencies(self):
        if not self._unresolved_dependencies:
            return False

        resolved = []
        for url, replace_action in self._unresolved_dependencies.items():
            try:
                self._resolve_dependency(url, replace_action)
                resolved.append(url)
            except KeyError:
                pass

        for x in resolved:
            self._unresolved_dependencies.pop(x)

        return bool(self._unresolved_dependencies)

    def _resolve_dependency(self, url, replace_action):
        replace_with = self.grabber.urls.get_local_path(url)
        relative_path = self.generate_relative_path(replace_with)

        replace_action.set_replace_with(relative_path)
        self._actions.append(replace_action)

    def generate_relative_path(self, target):
        source_url = self.url
        target_url = self.grabber.urls.get_url_from_local_path(target)

        relative_target = target[len(self.grabber.base_target):].lstrip("/")

        if source_url.netloc != target_url.netloc:
            parts = [".."] * (source_url.path.count("/") - 1)
        else:
            parts = [".."] * (source_url.path.count("/") - 1)

        parts.append(relative_target)
        return "/".join(parts)

    def crawl(self):
        for url, replace_action in self.find_links():
            url = normalise_url(url.strip(), self.url)

            try:
                self._resolve_dependency(url, replace_action)
            except KeyError:
                self._unresolved_dependencies[url] = replace_action

            yield url

    def find_links(self):
        raise NotImplementedError()

    def write(self):
        content = self.content
        for action in self._actions:
            content = action(content)

        with open(self.path, "w") as handler:
            handler.write(content)


class HtmlFileContent(FileContent):
    def write(self):
        self._actions.append(actions.ReplaceGATagAction())
        super().write()

    def find_links(self):
        soup = BeautifulSoup(self.content, "html.parser")

        # img
        for img_tag in soup.find_all("img"):
            yield img_tag["src"], actions.ReplaceHtmlValueAction("img", "src", img_tag["src"])

        # script
        for script_tag in soup.find_all("script"):
            if script_tag.get("type") == "text/javascript" and script_tag.get("src"):
                yield script_tag["src"], actions.ReplaceHtmlValueAction("script", "src", script_tag["src"])

        # link
        for link_tag in soup.find_all("link"):
            if link_tag.get("rel") == ["stylesheet"] and link_tag.get("href"):
                yield link_tag["href"], actions.ReplaceHtmlValueAction("link", "href", link_tag["href"])

        # a
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href")
            if not href or (is_absolute_url(href) and not href.startswith(self.grabber.base_url)):
                continue

            parts = href.split(":")
            if len(parts) == 2 and parts[-1] not in ("http", "https"):
                continue

            yield href, actions.ReplaceHtmlValueAction("a", "href", href)


class CssFileContent(FileContent):
    URL_RE = re.compile(r"url\(([^)]+)\)", re.IGNORECASE)

    def find_links(self):
        for match in self.URL_RE.findall(self.content):
            value = match
            if not value or value.startswith("data:"):
                continue

            yield value.strip("\""), actions.ReplaceCssUrlAction(value)
