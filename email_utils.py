# Part of code from https://github.com/pennersr/django-allauth/
# The MIT License (MIT)
# Copyright (c) 2010-2017 Raymond Penners and contributors

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_text


def format_email_subject(subject, prefix=None):
    if prefix is None:
        site = get_current_site()
        prefix = "[{name}] ".format(name=site.name)
    return prefix + force_text(subject)


def render_mail(template_prefix, email, context):
    """
    Renders an e-mail to `email`.  `template_prefix` identifies the
    e-mail that is to be sent, e.g. "account/email/email_confirmation"
    """
    subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                               context)
    # remove superfluous line breaks
    subject = " ".join(subject.splitlines()).strip()
    subject = format_email_subject(subject, settings.EMAIL_SUBJECT_PREFIX)

    bodies = {}
    for ext in ['html', 'txt']:
        try:
            template_name = '{0}_message.{1}'.format(template_prefix, ext)
            bodies[ext] = render_to_string(template_name,
                                           context).strip()
        except TemplateDoesNotExist:
            if ext == 'txt' and not bodies:
                # We need at least one body
                raise
    if 'txt' in bodies:
        msg = EmailMultiAlternatives(subject,
                                     bodies['txt'],
                                     settings.DEFAULT_FROM_EMAIL,
                                     [email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(subject,
                           bodies['html'],
                           settings.DEFAULT_FROM_EMAIL,
                           [email])
        msg.content_subtype = 'html'  # Main content is now text/html
    return msg


def send_templated_mail(template_prefix, email, context):
    msg = render_mail(template_prefix, email, context)
    msg.send()
