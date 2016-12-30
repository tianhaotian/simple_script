import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=9002, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        verify_code = self.get_argument('verify_code', '')
        if verify_code:
            print 'hahahahahaha'
        print self.request.path
        real_ip = self.request.headers.get('X-Forwarded-For',self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        token_cookie = self.get_cookie('token', '')
        real_token = token_cookie if token_cookie else self.get_argument('access_token', '')
        print "Token: ", real_token
        print real_ip
        self.write(greeting + ', friendly user!')

    def post(self, *args, **kwargs):
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
