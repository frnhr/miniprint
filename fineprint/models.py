from collections import namedtuple
from django.db import models
from users.models import User


class Company(models.Model):
    user = models.OneToOneField(User, related_name='company')
    name = models.CharField(max_length=500)


class Element(models.Model):
    previous = models.OneToOneField('self', related_name='next', null=True, blank=True)


class Heading(Element):
    STRENGTHS = namedtuple('STRENGTHS', ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))._make(range(6))
    STRENGTH_CHOICES = [(STRENGTHS.h1, 'h1'), (STRENGTHS.h2, 'h2'), (STRENGTHS.h3, 'h3'),
                        (STRENGTHS.h4, 'h4'), (STRENGTHS.h5, 'h5'), (STRENGTHS.h6, 'h6')]

    strength = models.PositiveSmallIntegerField(choices=STRENGTH_CHOICES, null=False)
    text = models.CharField(max_length=1000, null=False, blank=False)

    def strength_str(self):
        return self.STRENGTHS._fields[self.strength]

    def __unicode__(self):
        return u'{}: {}'.format(self.strength_str(), self.text)


class Chunk(Element):
    text = models.TextField()

    def __unicode__(self):
        return u'{}{}'.format(self.text[:80], '...' if len(self.text) > 80 else '')


class FinePrint(models.Model):
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=500, null=False, blank=False)
    first_element = models.OneToOneField(Element, related_name='fineprint')

    class Meta:
        verbose_name = u'Legal Text'

    def __unicode__(self):
        return self.title