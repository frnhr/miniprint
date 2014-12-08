from django.conf import settings
from django.template.loader import get_template
from django.template import Context


def get_code(document_id):
    """
    :raises Document.DoesNotExist
    :param document_id:
    :return:
    """
    template_name = 'remote/include.html'
    template = get_template(template_name)
    context = Context({
        'MAIN_HOST': settings.MAIN_HOST,
        'document_id': document_id,
    })
    return template.render(context)
