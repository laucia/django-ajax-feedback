====================
django-ajax-feedback
====================

Django Ajax Feedback is a simple Django application that makes it trivial to start accepting user feedback from authenticated users within your Django project.

It also include a feedback button to display the ajax submission form in an overlay.

The application can be internationalized (also no local is given).

Installation
============

Put ``feedback`` in your ``INSTALLED_APPS``, and set ``FEEDBACK_CHOICES`` to a 2-tuple of feedback types
in your settings file. For example::

	FEEDBACK_CHOICES = (
		('bug', _('Bug')),
		('feature_request', _('Feature Request')),
	)

Synchronize this application to your database with ``syncdb`` or ``migrate`` if you are a South user.

Also, be sure to include ``feedback.urls`` somewhere in your urls.py file.

If you want to use the lateral feedback button on your pages, 
load the tags ``{% load feedback_tags%}``
put this in your <header> ``{% feedback_header %}`` and ``{% feedback_widget %}`` in your <body>


Configuration
=============

To support anonymous feedback, set ``ALLOW_ANONYMOUS_FEEDBACK`` to true in your settings file.

This plugin uses ``jquery`` and its plugin ``jquery.forms``. If you already include them you can set ``FEEDBACK_INSERT_REQUIREMENT = False`` in your setting file.

Additionnaly, you can add ``feedback.context_processors.feedback_form`` to ``TEMPLATE_CONTEXT_PROCESSORS``, and
``feedback_form`` will be in the context for all authenticated users.
(usefull when NOT using the feedback widget)


Admin Screenshots
=================

.. image:: http://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-1.PNG

Overview in your admin index. Allows you to see all feedback current in the system.

.. image:: http://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-2.PNG

Viewing a piece of feedback from a user.
