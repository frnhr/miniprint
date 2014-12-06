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
            self.target.adjust_score_by(base_score + self.score)
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
    user = models.ForeignKey('users.User')
    text = models.CharField(max_length=255, null=False, blank=False)
    timestamp = models.DateTimeField()
    VOTE_TYPE_CHOICES = (('chunk', 'Chunk'), ('comment', 'Comment'), )
    vote_type = models.CharField(choices=VOTE_TYPE_CHOICES, max_length=10, null=True, blank=True)
    vote_id = models.PositiveIntegerField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['discuss_score', ]

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        if self.chunk and self.parent:
            raise ValueError('Cant define both parent and chunk')
        return super(Comment, self).save(*args, **kwargs)

    def short_text(self):
        return self.text[:30] + ('...' if len(self.text) > 30 else '')

    def __unicode__(self):
        return "C{}: {}".format(self.id, self.short_text())

    @property
    def vote(self):
        if self.vote_id and self.vote_type:
            try:
                # yeah... I know :)
                model_class_name = '{}Vote'.format(self.vote_type.capitalize())
                model_class = getattr(__import__('discuss.models', globals(), locals(), [model_class_name]), model_class_name)
                return model_class.objects.get(id=self.vote_id)
            except ObjectDoesNotExist:
                pass
        return None

    def vote_score(self):
        vote = self.vote
        return 0 if not vote else vote.score
