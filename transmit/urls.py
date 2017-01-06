from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'activity/set$', views.activity_set, name="activity_set"),
  url(r'showNameCard', views.showNameCard, name='showNameCard'),
  url(r'getNameCard', views.getNameCard, name='getNameCard'),
  url(r'getGoalMsg', views.getGoalMsg, name='getGoalMsg'),
  url(r'activity/save', views.save, name='save'),
  url(r'activity/release', views.release, name='release'),
  url(r'activity/delete', views.delete, name='delete'),
  url(r'activity/list', views.activity_list, name='activity_list'),
)
