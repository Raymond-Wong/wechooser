from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.index, name="index"),
  url(r'getNameCard', views.getNameCard, name='getNameCard'),
  url(r'getGoalMsg', views.getGoalMsg, name='getGoalMsg'),
  url(r'save', views.save, name='save'),
)
