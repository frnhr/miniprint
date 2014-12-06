from collections import namedtuple
from django.db import models
from users.models import User


class Element(models.Model):
    previous = models.OneToOneField('self', related_name='next')

    class Meta:
        abstract = True


class Heading(Element):
    STRENGTHS = namedtuple('HeadingStrength', ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    strength = models.PositiveSmallIntegerField(choices=STRENGTHS, null=False)
    text = models.CharField(max_length=1000, null=False, blank=False)


class Chunk(Element):
    text = models.TextField()


class FinePrint(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=500, null=False, blank=False)
    first_element = models.OneToOneField(Element, related_name='fineprint')

    class Meta:
        verbose_name = u'Legal Text'

