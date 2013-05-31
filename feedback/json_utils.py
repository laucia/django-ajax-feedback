import re
import decimal
try:
	import simplejson as json
except ImportError:
	import json
import datetime

from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.functional import Promise

from django.contrib.contenttypes.models import ContentType

class LazyEncoder(json.JSONEncoder):
	'''
	Special JSON encoder for lazy translation objects
	https://docs.djangoproject.com/en/dev/topics/serialization/#id2

	`json.dumps(object, cls=LazyEncoder)``
	'''
	def default(self, obj):
		# See "Date Time String Format" in the ECMA-262 specification.
		if isinstance(obj, datetime.datetime):
			r = obj.isoformat()
			if obj.microsecond:
				r = r[:23] + r[26:]
			if r.endswith('+00:00'):
				r = r[:-6] + 'Z'
			return r
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, datetime.time):
			if is_aware(obj):
				raise ValueError("JSON can't represent timezone-aware times.")
			r = obj.isoformat()
			if obj.microsecond:
				r = r[:12]
			return r
		elif isinstance(obj, decimal.Decimal):
			return str(obj)
		#Convert Promise Lazy objects
		elif isinstance(obj, Promise):
			return force_text(obj)
		elif isinstance(obj, ContentType):
			return obj.model
		else:
			return super(LazyEncoder, self).default(obj)


class JSONResponse(HttpResponse):
	'''
	XHR Object utility
	'''
	def __init__(self, request, data):
		indent = 2 if settings.DEBUG else None
		mime = 'text/javascript' if settings.DEBUG else 'application/json'
		content = json.dumps(data, indent=indent, sort_keys= settings.DEBUG, cls=LazyEncoder)
		callback = request.GET.get('callback')
		if callback:
			# Verify that the callback is secure
			if re.compile(r'^[a-zA-Z][\w.]*$').match(callback):
				content = '%s(%s);' % (callback, content)
		super(JSONResponse, self).__init__(content=content, mimetype=mime)