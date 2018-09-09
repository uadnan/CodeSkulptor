import re


class ReplaceAction:
    replace_with = None
    fragment = None

    def __call__(self, content):
        return self.replace(content, self.replace_with)

    def replace(self, content, replace_with):
        raise NotImplementedError()


class ReplaceHtmlValueAction(ReplaceAction):
    def __init__(self, tag, attribute, value):
        self.tag = tag
        self.attribute = attribute
        self.value = value

    def replace(self, content, replace_with):
        pattern = r"(<{tag}\s[^>]*{attr}=\"){value}(\"[^>]*>)".format(
            tag=self.tag,
            attr=self.attribute,
            value=re.escape(self.value)
        )

        return re.sub(pattern, lambda m: "%s%s%s" % (m.group(1), replace_with, m.group(2)), content)


class ReplaceCssUrlAction(ReplaceAction):
    def __init__(self, value):
        self.value = value

    def replace(self, content, replace_with):
        pattern = r"url\(\"?{value}\"?\)".format(value=re.escape(self.value))
        return re.sub(pattern, lambda m: "url(%s)" % replace_with, content)


class ReplaceGATagAction:
    RE = re.compile(r"<script\s[^>]*>[^<]*google-analytics\.com/ga.js[^<]*</script>", re.I | re.M)

    def __call__(self, content):
        return self.RE.sub("", content)


class ReplaceSaveURLAction:
    LOOKUP_URL = "\"//codeskulptor-{0}.commondatastorage.googleapis.com/\""
    TAGS_TO_REPLACE = [
        "googleid",
        "policy",
        "signature"
    ]

    def __call__(self, content):
        if self.LOOKUP_URL not in content:
            return content

        content = content.replace(self.LOOKUP_URL, "\"/save/\"")
        for tag in self.TAGS_TO_REPLACE:
            content = re.sub(r"%s\s*:\s*\"[^\"]*\"" % tag, "%s:\"\"" % tag, content)

        return content
