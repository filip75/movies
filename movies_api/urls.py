from django.conf.urls import url

from movies_api import views

urlpatterns = []

urlpatterns += [url(r'^movies/$', views.MoviesView.as_view())]
urlpatterns += [url(r'^movies/(?P<title>[a-zA-Z]+)', views.MoviesView.as_view())]