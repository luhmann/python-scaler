#!flask/bin/python
from werkzeug.contrib.profiler import ProfilerMiddleware
from image_scaler import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[100])
app.run(debug = True)