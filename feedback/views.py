from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from feedback.json_utils import JSONResponse
from feedback.forms import AnonymousFeedbackForm, FeedbackForm


def leave_feedback(request, template_name='feedback/feedback_form.html'):
	'''
	Generate and manage the form for feedback, and ulterior AJAX exchanges
    Only respond to Ajax call.
    Will return Http404 in case of non-xhr request
    
	Parameters
	----------
	request : HttpRequest
		user request sent by browser
	template_url : string
		Url of the template to use for rendering 

	'''
	if request.is_ajax():

		# Create Form
		if request.user.is_authenticated():
			form = FeedbackForm(request.POST or None)
		elif getattr(settings, 'ALLOW_ANONYMOUS_FEEDBACK', False):
			form = AnonymousFeedbackForm(request.POST or None)
		else:
			raise Http404

		# POST
		if request.method == 'POST':
			if form.is_valid():
				feedback = form.save(commit=False)
				if request.user.is_anonymous():
					feedback.user = None
				else:
					feedback.user = request.user
				feedback.save()
				data = {'success': _('Your feedback has been sent to us! Thanks a lot.')}
			else:
				data = {
                'success': False,
                'errors': dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()])}
			return JSONResponse(request, data)
		else :
			context = {
				'feedback_form':form,
			}
			return render(request, template_name, context)
	else :
		raise Http404

