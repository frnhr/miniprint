from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class DiscussScoreMixin(models.Model):
    discuss_score = models.BigIntegerField(null=False, blank=True, default=0)

    def adjust_score_by(self, score_delta, use_manager=False):
        if use_manager:
            type(self).objects.filter(id=self.id).update(score=self.discuss_score + score_delta)
        else:
            self.discuss_score = self.discuss_score + score_delta
            self.save()

    class Meta:
        abstract = True


class VoteModel(models.Model):
    score = models.SmallIntegerField(choices=((1, '+'), (0, '0'), (-1, '-')), default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            base_score = 0
        else:
            base_score = self.__class__.objects.get(id=self.id).score
        if self.target_id:
            self.target.adjust_score_by(self.score - base_score)
        return super(VoteModel, self).save(*args, **kwargs)


class CommentVote(VoteModel):
    user = models.ForeignKey('users.User', related_name='comment_votes')
    target = models.ForeignKey('Comment', related_name='votes')


class ChunkVote(VoteModel, models.Model):
    user = models.ForeignKey('users.User', related_name='chunk_votes')
    target = models.ForeignKey('fineprint.Chunk', related_name='votes')


class Comment(MPTTModel, DiscussScoreMixin):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    chunk = models.ForeignKey('fineprint.Chunk', null=True, blank=True, related_name='comments')
    user = models.ForeignKey('users.User', related_name='comments')
    text = models.CharField(max_length=255, null=False, blank=False)
    timestamp = models.DateTimeField()

    class MPTTMeta:
        order_insertion_by = ['-discuss_score', '-timestamp', ]

    class Meta:
        ordering = ['-discuss_score', '-timestamp', ]

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def short_text(self):
        return self.text[:30] + ('...' if len(self.text) > 30 else '')

    def __unicode__(self):
        return "C{}: {}".format(self.id, self.short_text())

    def render(self):
        return self.text

    @classmethod
    def get_trending(cls):
        past_limit = timezone.now() - timedelta(days=10)
        limit = 3
        min_score = 2
        trending = (Comment.objects
                    .filter(timestamp__gte=past_limit, parent=None)
                    .values('chunk__document')
                    .annotate(max_score=models.Max('discuss_score'))
                    .filter(max_score__gte=min_score)
                    .order_by('-max_score')[:limit])
        document_ids = [result['chunk__document'] for result in trending]
        for document_id in document_ids:
            yield Comment.objects.filter(chunk__document_id=document_id).order_by('-discuss_score')[0]


