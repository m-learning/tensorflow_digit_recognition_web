'''
Created on Jun 17, 2016

@author: Levan Tsinadze
'''

from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
