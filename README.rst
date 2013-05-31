====================
django-ajax-feedback
====================

Django Ajax Feedback is a simple Django application that makes it trivial to start accepting user feedback 
from authenticated users within your Django project.
It also include a feedback button to display the ajax submission form in an overlay

Installation
============

Put ``feedback`` in your ``INSTALLED_APPS``, and set ``FEEDBACK_CHOICES`` to a 2-tuple of feedback types
in your settings file. For example::

	FEEDBACK_CHOICES = (
		('bug', _('Bug')),
		('feature_request', _('Feature Request')),
	)


Also, be sure to include ``feedback.urls`` somewhere in your urls.py file.

Additionnaly, you can add ``feedback.context_processors.feedback_form`` to ``TEMPLATE_CONTEXT_PROCESSORS``, and
``feedback_form`` will be in the context for all authenticated users.

To support anonymous feedback, set ``ALLOW_ANONYMOUS_FEEDBACK`` to true in your settings file.

Admin Screenshots
=================
.. image:: http://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-1.PNG

Overview in your admin index. Allows you to see all feedback current in the system.

.. image:: http://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-2.PNG

Viewing a piece of feedback from a user.
