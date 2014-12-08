from collections import namedtuple
from string import rstrip
from django.db import models
from django.utils import timezone
from discuss.models import DiscussScoreMixin
from users.models import Company
from discuss.models import Comment, ChunkVote


class Document(models.Model):
    company = models.ForeignKey(Company, related_name='documents')
    title = models.CharField(max_length=500, null=False, blank=False)
    timestamp = models.DateTimeField(null=False, blank=True)

    class Meta:
        verbose_name = u'Legal Document'

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(Document, self).save(*args, **kwargs)

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
        return int(100 * votes_up_count / votes_total_count)

    def parse_input(self, text):
        self.chunks.all().delete()  # this should never actually delete anything, since we don't allow edits
        lines = "\n".join(map(rstrip, text.split("\n")))
        lines = lines.replace("\n\n\n", "\n\n")
        chunks = lines.split("\n\n")
        for i, chunk in enumerate(chunks):
            Chunk.objects.create(
                document=self,
                text=chunk,
                chunk_type=Chunk.TYPES.heading if len(chunk) < 75 else Chunk.TYPES.paragraph,
                order=i,
            )


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

    def type_full_str(self):
        if self.chunk_type == self.TYPES.heading:
            return 'heading'
        else:
            return 'paragraph'

    def short_text(self):
        length = 80
        return self.text[:length] + ('...' if len(self.text) > length else '')

    def __unicode__(self):
        return u'{}: {}'.format(self.type_str(), self.short_text())

    def comments_count(self):
        return self.comments.all().count()

    def is_scorable(self):
        return self.chunk_type == self.TYPES.paragraph

    def top_comment(self):
        try:
            return self.comments.order_by('-discuss_score')[0]
        except IndexError:
            return None

    class Meta:
        ordering = ['order', ]


class DocumentAgreement(models.Model):
    document = models.ForeignKey(Document, null=False, blank=False, related_name='agreements')
    user = models.ForeignKey('users.User', null=False, blank=False, related_name='agreements')
    timestamp = models.DateTimeField(auto_now_add=True)
