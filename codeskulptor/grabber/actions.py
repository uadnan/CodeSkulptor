import re


class ReplaceAction:
    replace_with = None

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
