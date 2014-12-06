from collections import namedtuple
from django.db import models
from users.models import Company


class Chunk(models.Model):
    TYPES = namedtuple('TYPES', ('heading', 'paragraph', ))._make(range(2))
    TYPE_CHOICES = [(TYPES.heading, 'Heading'), (TYPES.paragraph, 'Paragraph'), ]
    HEADING_STRENGTHS = namedtuple('STRENGTHS', ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))._make(range(6))
    HEADING_STRENGTH_CHOICES = [(getattr(HEADING_STRENGTHS, 'h{}'.format(i)), 'H{}'.format(i)) for i in range(1, len(HEADING_STRENGTHS) + 1)]

    previous = models.OneToOneField('self', related_name='next', null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    text = models.TextField()
    heading_strength = models.PositiveSmallIntegerField(choices=HEADING_STRENGTH_CHOICES, null=True, blank=True)

    def type_str(self):
        if self.type == self.TYPES.heading:
            return self.HEADING_STRENGTHS._fields[self.heading_strength]
        else:
            return 'p'

    def __unicode__(self):
        return u'{}: {}'.format(self.strength_str(), self.text)


class FinePrint(models.Model):
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=500, null=False, blank=False)
    first_chunk = models.OneToOneField(Chunk, related_name='fineprint')

    class Meta:
        verbose_name = u'Legal Text'

    def __unicode__(self):
        return self.title