from collections import namedtuple
from django.db import models
from discuss.models import DiscussScoreMixin
from users.models import Company
from discuss.models import Comment, ChunkVote


class Document(models.Model):
    company = models.ForeignKey(Company, related_name='documents')
    title = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = u'Legal Document'

    def __unicode__(self):
        return self.title

    def comments_count(self):
        return Comment.objects.filter(chunk__document=self, parent=None).count()

    def percentage(self):
        votes_total = ChunkVote.objects.filter(target__in=self.chunks.all())
        votes_up = votes_total.filter(score=1)
        votes_total_count = votes_total.count()
        votes_up_count = votes_up.count()
        if votes_up_count == 0 or votes_total_count == 0:
            return 0
        return int(100 * votes_up_count / votes_total_count )


class Chunk(DiscussScoreMixin, models.Model):
    TYPES = namedtuple('TYPES', ('heading', 'paragraph', ))._make(range(2))
    TYPE_CHOICES = [(TYPES.heading, 'Heading'), (TYPES.paragraph, 'Paragraph'), ]
    HEADING_STRENGTHS = namedtuple('STRENGTHS', ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))._make(range(6))
    HEADING_STRENGTH_CHOICES = [(getattr(HEADING_STRENGTHS, 'h{}'.format(i)), 'H{}'.format(i)) for i in range(1, len(HEADING_STRENGTHS) + 1)]

    document = models.ForeignKey(Document, related_name='chunks')

    order = models.PositiveIntegerField(default=0)
    chunk_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    text = models.TextField()
    heading_strength = models.PositiveSmallIntegerField(choices=HEADING_STRENGTH_CHOICES, null=True, blank=True)

    def type_str(self):
        if self.chunk_type == self.TYPES.heading:
            return self.HEADING_STRENGTHS._fields[self.heading_strength or 2]
        else:
            return 'p'

    def short_text(self):
        length = 80
        return self.text[:length] + ('...' if len(self.text) > length else '')

    def __unicode__(self):
        return u'{}: {}'.format(self.type_str(), self.short_text())

    def comments_count(self):
        return self.comments.all().count()

    class Meta:
        ordering = ['order', ]

