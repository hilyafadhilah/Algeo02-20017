from flask import Flask, request, send_from_directory, send_file, make_response
from flask_cors import CORS
from time import perf_counter

from compress.lib import compressImage

app = Flask(__name__,
            static_folder=None)

cors = CORS(app,
            resources={
                r'/api/*' : {
                    'origins' : '*',
                    'expose_headers': ['Compress-Time']
            }})

@app.route('/api/compress', methods=['POST'])
def compress_route():
    try:
        file = request.files['file']
        ratio = int(request.form['rate'])

        startTime = perf_counter()
        result = compressImage(file, ratio)
        endTime = perf_counter()

        response = make_response(send_file(result, mimetype=file.mimetype))
        response.headers['Compress-Time'] = endTime - startTime
        return response
    except:
        return '', 501

@app.route('/', defaults={ 'path': 'index.html' })
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./client/dist', path)
