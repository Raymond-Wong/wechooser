from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'getLoginUrl', views.getLoginUrl, name='getLoginUrl'),
  url(r'debuctCredit', views.debuctCredit, name='debuctCredit'),
)
