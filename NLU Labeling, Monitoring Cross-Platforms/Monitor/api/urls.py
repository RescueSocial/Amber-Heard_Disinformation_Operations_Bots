from django.urls import path
from django.conf.urls import url 

from api import views

urlpatterns = [
    url(r'^api/nlptext$', views.nlptext),
    url(r'^api/nlutext$', views.nlutext),
    url(r'^api/nlgtext$', views.nlgtext),
    url(r'^api/tweet$', views.tweets),
    url(r'^api/action$', views.action),
    url(r'^api/fileupload$', views.fileupload),
    url(r'^api/dashboard$', views.dashboard),
    # path('nlptext', views.nlptext, name='nlptext'),
]