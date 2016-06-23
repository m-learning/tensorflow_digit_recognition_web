# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import cnn.cnn_recognition_run as recog
from src.cnn.mnist.cnn_files import training_file

@csrf_exempt
def index(request):
    if request.method == 'GET':
        template = loader.get_template('polls/index.html')
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        tr_fls = training_file()
        to_recognize_path = tr_fls.get_to_recognize_file()
        with open(to_recognize_path, 'w') as file_:
            file_.write(request.body)
        recgnizer = recog.recognizer()
        rec_answer = recgnizer.recognize_image()
        return HttpResponse(rec_answer)