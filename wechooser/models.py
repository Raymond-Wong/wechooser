# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, FieldFile, ImageFile
import sae.storage
from os import environ

# from http://www.pythonfan.org/thread-7614-1-1.html
class SAEFieldFile(FieldFile):
  def getUploadTo(self):
    return self.upload_to

  def save(self, name, content, save=True):
    name = self.field.generate_filename(self.instance, name)
    #for SAE
    s = sae.storage.Client()
    ob = sae.storage.Object(content._get_file().read())
    url = s.put('images', name, ob)
    self.name = name
    setattr(self.instance, self.field.name, self.name)

    # Update the filesize cache
    self._size = content.size
    self._committed = True

    # Save the object because it has changed, unless save is False
    #if save:
    #    self.instance.save()

class SAEImageFieldFile(ImageFile, SAEFieldFile):
  def delete(self, save=True):
    # Clear the image dimensions cache
    if hasattr(self, '_dimensions_cache'):
      del self._dimensions_cache
    super(ImageFieldFile, self).delete(save)

class ZGImageFieldFile(SAEImageFieldFile):
  def save(self, name, content, save=True):
    super(SAEImageFieldFile, self).save(name, content, save=True)

class ZGImageField(ImageField):
  attr_class = ZGImageFieldFile
  def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
    super(ZGImageField, self).__init__(verbose_name, name, **kwargs)

############################
remote = not environ.get("APP_NAME", "")
if not remote:
  ImageField = ZGImageField
############################

class Image(models.Model):
  url = ImageField(upload_to = 'images/')