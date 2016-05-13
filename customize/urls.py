from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^material$', views.getMaterial, name='getMaterial'),

  url(r'^$', views.index, name="index"),
  url(r'^login$', views.login, name='login'),
  url(r'^logout$', views.logout, name='logout'),
  url(r'^reply$', views.setReply, name='setReply'),
  url(r'^reply/delete$', views.deleteReply, name='deleteReply'),
  url(r'^menu$', views.editMenuHandler, name='editMenuHandler'),
  url(r'^test$', views.test, name='test'),
)
