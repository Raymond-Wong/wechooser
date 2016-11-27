from sae.storage import Connection, Bucket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def verify(request, fname):
  con = Connection()
  bucket = con.get_bucket("data")
  content = bucket.get_object_contents("%s.txt" % fname)
  return HttpResponse(content)