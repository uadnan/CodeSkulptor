import string

DISALLOWED_HOSTS = [
    "maps.googleapis.com"
]

LEGAL_FILENAME_CHAR = "-_.() %s%s" % (string.ascii_letters, string.digits)
EXTENSION_BY_MIME_TYPE = {
    "text/css": ".css"
}
