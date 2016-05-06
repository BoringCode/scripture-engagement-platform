from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect
from flask.ext.wtf import Form
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import Length, required


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.url:
        if not target:
            continue
        if is_safe_url(target):
            return target


class NewPost(Form):
    comment = TextAreaField("Comment", [required(), Length(max=1000)])
    submit = SubmitField('Post Comment')
    next = HiddenField()
    originator_type = HiddenField([required()])
    originator_id = HiddenField([required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        # Set hidden data
        if not self.originator_type.data and originator_type is not None:
            self.originator_type.data = originator_type
        if not self.originator_id.data and originator_id is not None:
            self.originator_id.data = originator_id
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))