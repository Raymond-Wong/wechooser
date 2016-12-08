from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
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
  url(r'^upload$', views.uploadHandler),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
