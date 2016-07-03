'''
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
'''

from flask import Flask, request, render_template, json
from sys import argv
from cnn_files import training_file
from retrain_run import image_recognizer


app = Flask(__name__)

# Controller for image recognition
class cnn_server:
    
    # Runs recognizer
    def cnn_run(self, request):
        
        img_url = request.data
        print img_url
        tr_fl = training_file()
        tr_fl.get_file_to_recognize(img_url)
        img_recognizer = image_recognizer()
        answer = img_recognizer.run_inference_on_image()
        anwer_txt = {}
        for key, value in answer.iteritems():
            anwer_txt[key] = str(value)
        print anwer_txt
        resp = json.dumps(anwer_txt)
        
        return resp

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
    
    if request.method == 'POST':
        srv = cnn_server()
        resp = srv.cnn_run(request)
        resp = resp
    elif request.method == 'GET':
        resp = render_template("index.html")
    
    return resp
        
# Retrieves host name from arguments
def get_host_info():
    
    if len(argv) > 1:
        host_nm = argv[1]
    else:
        host_nm = '0.0.0.0'
    
    return host_nm

# Retrieves port number from arguments
def get_port_info():
    
    if len(argv) > 2:
        port_nm = argv[1]
    else:
        port_nm = 8080
        
    return port_nm

# Initializes host address and port number    
def get_host_and_port():
    
    # Retrieves host and port from arguments
    host_nm = get_host_info()
    port_nm = get_port_info()
    
    return (host_nm, port_nm)

if __name__ == "__main__":
    
    # Retrieves host and port from arguments
    (host_nm, port_nm) = get_host_and_port()
    # Binds server on host and port
    app.run(host=host_nm, port=port_nm, threaded=True)
