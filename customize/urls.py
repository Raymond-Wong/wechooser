from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^menu$', views.editMenu, name='editMenu'),
  url(r'^material$', views.getMaterial, name='getMaterial'),

  url(r'^login$', views.login, name='login'),
  url(r'^reply$', views.setReply, name='setReply'),
  url(r'^reply/delete$', views.deleteReply, name='deleteReply'),
)
