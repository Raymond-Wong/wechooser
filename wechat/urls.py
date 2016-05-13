from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.entrance, name='entrance'),
  url(r'update', views.updateTokenHandler, name='updateTokenHandler'),
  url(r'getMaterial', views.getMaterialHandler, name='getMaterialHandler'),
)
