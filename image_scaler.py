from flask import Flask, send_file
import settings
from ImageGetter import ImageGetter
import StringIO
from targets import *

app = Flask(__name__)
app.config.from_pyfile('config/default.cfg')

@app.route("/<target>/<width>/<path:key>")
def scale(target, width, key):
    img_getter = ImageGetter(key)
    target = Target.factory(target, width, img_getter.get())
    image = target.convert()

    output = StringIO.StringIO()
    image.save(output, settings.OUTPUT_FORMAT, quality=settings.JPEG_QUALITY)
    output.seek(0)

    return send_file(output, 'image/jpeg')

if __name__ == "__main__":
    app.run()