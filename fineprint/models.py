from collections import namedtuple
from django.db import models
from discuss.models import DiscussScoreMixin
from users.models import Company



class Document(models.Model):
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = u'Legal Document'

    def __unicode__(self):
        return self.title


class Chunk(DiscussScoreMixin, models.Model):
    TYPES = namedtuple('TYPES', ('heading', 'paragraph', ))._make(range(2))
    TYPE_CHOICES = [(TYPES.heading, 'Heading'), (TYPES.paragraph, 'Paragraph'), ]
    HEADING_STRENGTHS = namedtuple('STRENGTHS', ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))._make(range(6))
    HEADING_STRENGTH_CHOICES = [(getattr(HEADING_STRENGTHS, 'h{}'.format(i)), 'H{}'.format(i)) for i in range(1, len(HEADING_STRENGTHS) + 1)]

    document = models.ForeignKey(Document)

    order = models.PositiveIntegerField(default=0)
    chunk_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    text = models.TextField()
    heading_strength = models.PositiveSmallIntegerField(choices=HEADING_STRENGTH_CHOICES, null=True, blank=True)

    def type_str(self):
        if self.chunk_type == self.TYPES.heading:
            return self.HEADING_STRENGTHS._fields[self.heading_strength or 2]
        else:
            return 'p'

    def __unicode__(self):
        return u'{}: {}'.format(self.type_str(), self.text)

    class Meta:
        ordering = ['order', ]

