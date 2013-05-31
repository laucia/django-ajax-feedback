from django.conf import settings
from django.template import Library, Node
from feedback.models import AnonymousFeedback, Feedback
from itertools import chain
from feedback.context_processors import feedback_form as feedback_context_processor

register = Library()

@register.tag
def get_feedback(parser, token):
    '''
    {% get_feedback %}
    '''
    return FeedbackNode()


class FeedbackNode(Node):
    def render(self, context):
        feedback = [Feedback.objects.all()]
        if getattr(settings, 'ALLOW_ANONYMOUS_FEEDBACK', False):
            feedback.append(AnonymousFeedback.objects.all())
        # Flatten list of querysets and sort feedback by date.
        feedback = sorted(list(chain.from_iterable(feedback)),
                          key=lambda instance: instance.time, reverse=True)
        context['feedback'] = feedback
        return ''


@register.inclusion_tag('feedback/feedback_widget.html', takes_context = True)
def feedback_widget(context):
    '''
    Create the feedback widget
    {% feedback_widget %}
    '''
    request = context['request']
    try:
        feedback_form = context['feedback_form']
    except KeyError :
        feedback_form = feedback_context_processor(request)['feedback_form']
    return {'feedback_form': feedback_form}


@register.inclusion_tag('feedback/feedback_header.html',takes_context = True)
def feedback_header(context):
    '''
    Include the header elements relative to the feedback
    {% feedback_header %}
    '''
    forwarded_context = {'STATIC_URL':context['STATIC_URL']}
    if getattr(settings, 'FEEDBACK_INSERT_REQUIREMENT', False):
        forwarded_context.update({'FEEDBACK_INSERT_REQUIREMENT': True})
    else:
        forwarded_context.update({'FEEDBACK_INSERT_REQUIREMENT': False})

    return forwarded_context