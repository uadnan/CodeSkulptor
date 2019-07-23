import os
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO

import multipart

from codeskulptor import __version__, storage


class CodeSkulptorRequestHandler(SimpleHTTPRequestHandler):
    server_version = "CodeSkulptor/%s" % __version__

    def read_form_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf8")

        parser = multipart.MultipartParser(BytesIO(multipart.to_bytes(post_data)), post_data.split("\r")[0][2:])
        parts = parser.parts()

        return {
            part.name: part.value
            for part in parts
        }

    def do_HEAD(self):
        if self.path.startswith("/save/"):
            self.handle_storage_HEAD(self.path.replace("/save/", ""))
        else:
            super().do_HEAD()

    def do_POST(self):
        if self.path.startswith("/save/"):
            self.handle_storage_POST()
        else:
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method Not Allowed")

    def do_GET(self):
        if self.path.startswith("/save/"):
            self.handle_storage_GET(self.path.replace("/save/", ""))
        else:
            super().do_GET()

    def handle_storage_HEAD(self, path):
        if storage.file_exists(path):
            self.send_error(HTTPStatus.OK, "Found")
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def handle_storage_GET(self, path):
        path = storage.abs_path(path)

        if not os.path.exists(path):
            return self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/x-python")

        with open(path, "rb") as f:
            fs = os.fstat(f.fileno())

            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()

            self.copyfile(f, self.wfile)

    def handle_storage_POST(self):
        form_data = self.read_form_data()
        storage.save_file(form_data["key"], form_data["file"])
        self.send_response(HTTPStatus.NO_CONTENT, "No Content")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()


class CodeSkulptorHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.open_browser = kwargs.pop("open_browser", False)
        super().__init__(*args, **kwargs)

    def server_activate(self):
        if self.open_browser:
            webbrowser.open("http://%s:%s/" % self.server_address)

        super().server_activate()


def serve(address, directory, open_browser):
    current_dir = os.curdir
    os.chdir(directory)

    try:
        server = CodeSkulptorHTTPServer(address, CodeSkulptorRequestHandler, open_browser=open_browser)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        os.chdir(current_dir)
