from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'autoLogin', views.autoLogin, name='autoLogin'),
  url(r'debuctCredit', views.debuctCredit, name='debuctCredit'),
  url(r'notify', views.notify, name='notify'),
)
