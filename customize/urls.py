from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.index, name="index"),
  url(r'^login$', views.login, name='login'),
  url(r'^logout$', views.logout, name='logout'),
  url(r'^reply$', views.setReplyHandler, name='setReplyHandler'),
  url(r'^reply/delete$', views.deleteReply, name='deleteReply'),
  url(r'^menu$', views.editMenuHandler, name='editMenuHandler'),
  url(r'^task/add$', views.addTaskHandler, name='addTaskHandler'),
  url(r'^task/list$', views.taskHandler, name='taskHandler'),
  url(r'^test$', views.test, name='test'),
  url(r'^statisic/list$', views.list_statistic, name='list_statistic'),
)
