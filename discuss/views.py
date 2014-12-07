from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View
from http_status import HttpResponseCreated, HttpResponseAccepted
from fineprint.models import Chunk
from .models import ChunkVote, CommentVote


class ScoreRangeError(ValueError):
    pass


class VoteView(View):
    model = ChunkVote

    def _target_model_name(self):
        return self.model.target.field.model.__name__

    def post(self, request):
        target_id = None
        try:
            if not request.user.is_authenticated():
                raise PermissionDenied('Login required')
            target_id = int(self.request.POST['target_id'])
            score = int(self.request.POST['score'])
            kwargs = {
                'user': request.user,
                'target_id': target_id,
            }
            if score < -1 or score > 1:
                raise ScoreRangeError('Score not in range [-1, 1]')
            vote, created = self.model.objects.get_or_create(**kwargs)
            vote.score = score
            vote.save()
        except PermissionDenied as e:
            status = HttpResponseForbidden
            response = {
                'success': False,
                'error': 'Login required',
            }
        except Chunk.DoesNotExist as e:
            status = HttpResponseNotFound
            response = {
                'success': False,
                'error': '{} not found: {}'.format(self._target_model_name(), target_id)
            }
        except Exception as e:
            status = HttpResponseBadRequest
            response = {
                'success': False,
                'error': '{}: {}'.format(type(e).__name__, e)
            }
        else:
            status = HttpResponseCreated if created else HttpResponseAccepted
            response = {
                'success': True,
                'vote_id': vote.id,
                'vote_score': vote.score,
                'target_score': vote.target.discuss_score,
            }
        return JsonResponse(response, status=status.status_code)


class VoteChunk(VoteView):
    model = ChunkVote


class VoteComment(VoteView):
    model = CommentVote
