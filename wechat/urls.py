from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.entrance, name='entrance'),
  url(r'menu', views.editMenu, name='editMenu'),
  url(r'getMaterial', views.getMaterial, name='getMaterial'),
)
