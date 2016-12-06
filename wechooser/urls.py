from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^wechat', include('wechat.urls')),
  url(r'^duiba', include('duiba.urls')),
  url(r'^transmit', include('transmit.urls')),
  url(r'', include('customize.urls')),
  url(r'(.+).txt', views.verify),
)
