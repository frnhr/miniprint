from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View
from http_status import HttpResponseCreated, HttpResponseAccepted
from fineprint.models import Chunk
from .models import ChunkVote, CommentVote


class ScoreRangeError(ValueError):
    pass


class VoteChunk(View):

    def post(self, request):
        chunk_id = None
        try:
            if not request.user.is_authenticated():
                raise PermissionDenied('Login required')
            chunk_id = int(self.request.POST['chunk_id'])
            score = int(self.request.POST['score'])
            kwargs = {
                'user': request.user,
                'target_id': chunk_id,
            }
            if score < -1 or score > 1:
                raise ScoreRangeError('Score not in range [-1, 1]')
            chunk_vote, created = ChunkVote.objects.get_or_create(**kwargs)
            chunk_vote.score = score
            chunk_vote.save()
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
                'error': 'Chunk not found: {}'.format(chunk_id)
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
                'vote_id': chunk_vote.id,
                'vote_score': chunk_vote.score,
                'target_score': chunk_vote.target.discuss_score,
            }
        return JsonResponse(response, status=status.status_code)

