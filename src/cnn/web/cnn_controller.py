'''
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
'''

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
    if request.method == 'POST':
        dig_fl = request.files['this_file']
        print dig_fl
    elif request.method == 'GET':
        print 'GET'


if __name__ == "__main__":
    app.run()