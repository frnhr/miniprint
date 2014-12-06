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


class Comment(MPTTModel, DiscussScoreMixin):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    user = models.ForeignKey('users.User')
    text = models.CharField(max_length=255, null=False, blank=False)
    timestamp = models.DateTimeField()

    class MPTTMeta:
        order_insertion_by = ['score']

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)


class VoteModel(models.Model):
    score = models.SmallIntegerField(choices=((1, '+'), (0, '0'), (-1, '-')), default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            base_score = 0
        else:
            base_score = self.__class__.objects.get(id=self.id).score
        self.target.adjust_score_by(base_score + self.score)
        return super(VoteModel, self).save(*args, **kwargs)


class CommentVote(VoteModel):
    user = models.ForeignKey('users.User', related_name='comment_votes')
    target = models.ForeignKey(Comment, related_name='votes')


class ChunkVote(VoteModel, models.Model):
    user = models.ForeignKey('users.User', related_name='chunk_votes')
    target = models.ForeignKey('fineprint.Chunk', related_name='votes')

