from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.unittest import skipUnless,skipIf
from django.http import HttpResponseNotFound

from models import *

user_info = {
	'username': 'alice',
	'password': 'swordfish',
	'email': 'alice@example.com'
	}

class ModelTest(TestCase):
	def test_setup(self):
		'''
		Test if the plugin is correctly and toroughly installed
		
		'''

		self.failUnless(settings.FEEDBACK_CHOICES)
		self.failUnless(reverse('feedback'))


	def test_create_feedback(self):
		'''
		Test object creation
		(ie: as syncdb/migrate been run correctly and without errors)
		
		'''
		
		user = User.objects.create_user(**user_info)
		Feedback.objects.create(
			user=user,
			type = settings.FEEDBACK_CHOICES[0],
			message = 'Test',
			context_url = 'http://example.com/test/',
			browser ='/',		
			)
		AnonymousFeedback.objects.create(
			user=None,
			type = settings.FEEDBACK_CHOICES[0],
			message = 'Test',
			context_url = 'http://example.com/test/',
			browser ='/',		
			)

class ViewTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(**user_info)

	def tearDown(self):
		self.user.delete()

	def test_non_ajax_request(self):
		'''
		Validate a 404 error in case of direct access to the 
		feedback form

		'''

		client = Client(enforce_csrf_checks=True)
		client.login(
			username=user_info['username'], 
			password=user_info['password'],
			)
		response = client.get(
			reverse('feedback'), 
			follow=True,
			)
		self.failUnless(isinstance(response,HttpResponseNotFound))


	def test_anonymous_user(self):
		'''
		Test allowance of AnonymousUsers

		'''
		client = Client(enforce_csrf_checks=True)
		response = client.get(
			reverse('feedback'), 
			follow=True,
			)
		if settings.ALLOW_ANONYMOUS_FEEDBACK:
			self.failIf(isinstance(response,HttpResponseNotFound))
		else :
			self.failUnless(isinstance(response,HttpResponseNotFound))






