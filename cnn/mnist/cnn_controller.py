'''
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
'''

from flask import Flask, request, render_template, json
from cnn_fs import parameters_file
from cnn_recognizer import image_recognizer


app = Flask(__name__)

# Controller for image recognition
class cnn_server:
    
    # Runs recognizer
    def cnn_run(self, request):
        
        fls = request.data
        tr_fls = parameters_file()
        to_recognize_path = tr_fls.get_to_recognize_file()
        with open(to_recognize_path, 'w') as file_:
            file_.write(fls)
        recgnizer = image_recognizer()
        rec_numb = recgnizer.recognize_image()
        resp = json.dumps(rec_numb)
        
        return resp

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
    if request.method == 'POST':
        
        srv = cnn_server()
        resp = srv.cnn_run(request)
        
        return resp
    elif request.method == 'GET':
        return render_template("index.html")
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded = True)
