import tornado.ioloop
import tornado.web
import tornado.concurrent

import os
import uuid
import connector_predict


MAX_PROCESS = 1
MAX_WORKERS = 4
PORT = 8080

IMAGE_DIR = "image_temp/"
HTML_PATH = "templates/"
REDIRECT_URL = "https://www.google.co.kr/search?tbm=isch&q="
REDIRECT_HOME = "http://localhost:8080"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        print('client !')
        self.render(HTML_PATH + "index.html")


class ImageHandler(tornado.web.RequestHandler):

    executor = tornado.concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @tornado.concurrent.run_on_executor
    def run_tensorflow(self, image_path):
        connector_inst = connector_predict.Connector(image_path)
        label = connector_inst.get_result()
        return label

    @tornado.gen.coroutine
    def upload_file(self, file, f_name):
        with open(os.path.join(IMAGE_DIR + f_name), 'wb') as save_file:
            save_file.write(file['body'])

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        request_file = self.request.files['uploadFile'][0]

        if request_file:
            extension = os.path.splitext(request_file.filename)[1]
            file_name = str(uuid.uuid4()) + extension

            yield self.upload_file(request_file, file_name)

            print("upload !")
            image_path = IMAGE_DIR + file_name
            label = yield self.run_tensorflow(image_path)
            return self.redirect(REDIRECT_URL + label)

        else:
            return self.redirect(REDIRECT_HOME)


def make_app():
    return tornado.web.Application([
        ("/", MainHandler),
        ("/upload", ImageHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(PORT)
    server.start(MAX_PROCESS)  # forks one process per cpu 0
    print('Tornado Server Start !')
    tornado.ioloop.IOLoop.current().start()
