# server.py
import commands
from flask import Flask, request, render_template
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import time
from jinja2 import Template, Environment, FileSystemLoader
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pipe')
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        ws.send(commands.getoutput("cat /home/pi/raspberrypi-wifi-config-script/previous-ip"))

        while True:
            message = ws.receive()
            logger.debug('receive message: type=%s, message=%s', type(message), message)
            data = message.split(",")
            btnData = data[0]

            if btnData == "save-reboot":
                logger.debug("save-reboot")
                env = Environment(loader=FileSystemLoader('/home/pi/raspberrypi-wifi-config-script/wifi-config-site/templates'))
                template = env.get_template('wpa_supplicant.conf.j2')

                data = {
                    "ssid": data[1],
                    "pass": data[2],
                }

                rendered = template.render(data)

                with open("/etc/wpa_supplicant/wpa_supplicant.conf", mode='w') as f:
                    f.write(str(rendered))

            commands.getoutput("/home/pi/raspberrypi-wifi-config-script/wifi-reconfig.sh")

def main():
    app.debug = True
    server = pywsgi.WSGIServer(("", 80), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
