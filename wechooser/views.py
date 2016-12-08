from sae.storage import Connection, Bucket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils import appendImageUrl, Response
import time
from models import Image

def verify(request, fname):
  con = Connection()
  bucket = con.get_bucket("data")
  content = bucket.get_object_contents("%s.txt" % fname)
  return HttpResponse(content)

@csrf_exempt
def uploadHandler(request):
  image = request.FILES['image']
  image._name = '%s_%s' % (str(int(time.time())), image._name)
  image = Image(url=image)
  image.save()
  url = appendImageUrl(image.__dict__.get('url'))
  return HttpResponse(Response(m=url).toJson(), content_type='application/json')