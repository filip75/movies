from django.conf.urls import url

from movies_api import views

date_regex = r'\d{4}-\d{2}-\d{2}'

urlpatterns = []

urlpatterns += [url(r'^movies/$', views.MoviesView.as_view())]
urlpatterns += [url(r'^movies/(?P<movie>[0-9]+$)', views.MoviesView.as_view())]

urlpatterns += [url(r'^comments/$', views.CommentsView.as_view())]
urlpatterns += [url(r'^comments/movies/(?P<movie>[\d]+)$', views.CommentsView.as_view())]

urlpatterns += [url(r'^top/$', views.TopView.as_view())]
