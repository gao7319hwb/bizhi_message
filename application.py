# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2020-04-16 14:38:22
@LastEditTime: 2020-08-06 15:07:21
@LastEditors: HuangWenBin
@Description: 
"""

# 框架引用
from seven_framework.web_tornado.base_tornado import *
from handlers.monitor import MonitorHandler
#from handlers import Index
from handlers.server import sdk_message



class Application(tornado.web.Application):
    def __init__(self):
        application_settings = dict(
            # 如需使用cookie 请解除注释此句,并在handler中继承含有cookie的 base_handler
            # cookie_secret=config.get_value("cookie_secret"),
            # pycket=config.get_value("pycket"),
            # 键为template_path固定的，值为要存放HTML的文件夹名称
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape=None,
            xsrf_cookies=True)

        handlers = []

        # 模块的路由可以独立开
        handlers.extend(self.route_handlers())

        super().__init__(handlers, **application_settings)

    def route_handlers(self):
        return [
            (r"/monitor", MonitorHandler),
            (r"/message/get", sdk_message.MessageListHandler),
            (r"/message/getmessagecount", sdk_message.MessageCountHandler),
            (r"/message/actionreport", sdk_message.MessageReportHandler),
            (r"/message/operate", sdk_message.MessageOperateHandler),
            (r"/message/add", sdk_message.AddMessageHandler),
            (r"/message/record", sdk_message.GetRecordHandler),
        ]


def main():
    logger_info.info('application begin')
    try:
        if platform.system() == "Windows":
            import asyncio
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

        http_server = tornado.httpserver.HTTPServer(Application(),
                                                    xheaders=True)
        # 从配置中获取启动监听端口
        http_server.listen(config.get_value("run_port"))
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print("服务已停止运行")


if __name__ == "__main__":
    main()
