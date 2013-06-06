from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib import admin
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import AnonymousFeedback, Feedback

class BaseFeedbackAdmin(admin.ModelAdmin):
    '''
    Base Class with the general informations and mecanisms relative to Feedback admin
    
    '''
    list_display = ['type','user', 'message', 'time','context_url' ,'browser', 'view']
    search_fields = ['user', 'message']
    list_filter = ['type', 'time']

    def view(self, obj):
        return "<a href='%s'>View</a>" % obj.get_absolute_url()

    view.allow_tags = True

    def view_feedback(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        context = {'feedback': feedback}
        return render_to_response('feedback/view_feedback.html', context,
                                  context_instance=RequestContext(request))

class FeedbackAdmin(BaseFeedbackAdmin):
    '''
    ``Feedback`` admin class

    '''
    def get_urls(self):
        urls = super(FeedbackAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^view/(?P<feedback_id>\d+)/$',
                self.admin_site.admin_view(self.view_feedback),
                name='view-feedback'),
        )
        return my_urls + urls

admin.site.register(Feedback, FeedbackAdmin)


class AnonymousFeedbackAdmin(BaseFeedbackAdmin):
    '''
     ``AnonymousFeedback`` admin class

    '''
    def get_urls(self):
        urls = super(AnonymousFeedbackAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^view/(?P<feedback_id>\d+)/$',
                self.admin_site.admin_view(self.view_feedback),
                name='view-anon-feedback'),
        )
        return my_urls + urls


if getattr(settings, 'ALLOW_ANONYMOUS_FEEDBACK', False):
    admin.site.register(AnonymousFeedback, AnonymousFeedbackAdmin)


# Change the admin index with the custom version with the display of the latest feedbacks
admin.site.index_template = 'feedback/index.html'

