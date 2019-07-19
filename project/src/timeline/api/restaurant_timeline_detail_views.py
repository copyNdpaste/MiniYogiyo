import json
from http import HTTPStatus
from json import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from accounts.mixins import LoginRequiredMixin
from restaurant.models import RestaurantTimeline
from timeline.forms import RestaurantTimelineCommentForm
from timeline.models import RestaurantTimelineComment


class RestaurantTimelineLikeAPI(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        user = request.user

        restaurant_timeline = RestaurantTimeline.objects.filter(id=restaurant_timeline_id)

        if not restaurant_timeline:
            data = {
                'error': '해당 레스토랑 타임라인이 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        user_like_restaurant_timeline = restaurant_timeline.filter(like=user)
        timeline_like = restaurant_timeline[0].like

        if user_like_restaurant_timeline.exists():

            timeline_like.remove(user)
            data = {
                'message': '좋아요 취소',
                'like': False,
                'like_count': timeline_like.count()
            }
            return JsonResponse(data, status=HTTPStatus.OK)

        timeline_like.add(user)

        data = {
            'message': '좋아요 성공',
            'like': True,
            'like_count': timeline_like.count()
        }
        return JsonResponse(data, status=HTTPStatus.OK)


class RestaurantTimelineCommentListAPI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        timeline_comments = (
            RestaurantTimelineComment.objects.select_related('writer')
            .filter(restaurant_timeline_id=restaurant_timeline_id, is_active=True)
            .order_by('-created_time'))

        if not timeline_comments:
            data = {
                'error': '댓글이 없습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        comments = [
            {'id': comment.id,
             'is_my_comment': (True if comment.writer_id==request.user.id else False),
             'username': comment.writer.username,
             'comment': comment.comment,
             'created_time': comment.created_time,
             'updated_time': comment.updated_time} for comment in timeline_comments]

        data = {
            'comments': comments
        }
        return JsonResponse(data, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):

        try:
            comment_data = json.loads(request.body)

        except JSONDecodeError:
            data = {
                'error': '잘못된 요청입니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        user = request.user

        comment_data['writer'] = user.id
        comment_data['restaurant_timeline'] = restaurant_timeline_id

        comment_form = RestaurantTimelineCommentForm(comment_data)

        if not comment_form.is_valid():
            data = {
                'message': '폼이 유효하지 않습니다.',
                'error': comment_form.errors
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        comment = comment_form.save(commit=True)
        data = {
            'comment_id': comment.id,
            'message': '댓글을 작성하였습니다.'
        }
        return JsonResponse(data, status=HTTPStatus.CREATED)


class RestaurantTimelineCommentAPI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        comment_id = kwargs['comment_id']

        user = request.user

        comment_qs = (
            RestaurantTimelineComment.objects.select_related('writer')
            .filter(id=comment_id, restaurant_timeline_id=restaurant_timeline_id, writer=user, is_active=True))

        try:
            comment = comment_qs[0]

        except IndexError:
            data = {
                'error': '해당 댓글이 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        data = {
            'comment_id': comment.id,
            'comment': comment.comment
        }
        return JsonResponse(data, status=HTTPStatus.OK)

    def put(self, request, *args, **kwargs):
        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        comment_id = kwargs['comment_id']

        try:
            comment = json.loads(request.body)['comment']

        except KeyError:
            data = {
                'error': '잘못된 요청입니다.'
            }
            return JsonResponse(data, status=HTTPStatus.BAD_REQUEST)

        user = request.user
        comment_qs = (
            RestaurantTimelineComment.objects.select_related('writer')
            .filter(id=comment_id, restaurant_timeline_id=restaurant_timeline_id, writer=user, is_active=True))

        if not comment_qs:
            data = {
                'error': '해당 댓글이 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        comment_qs.update(comment=comment)

        data = {
            'message': '수정되었습니다.',
            'comment_id': comment_id
        }
        return JsonResponse(data, status=HTTPStatus.OK)

    def delete(self, request, *args, **kwargs):
        restaurant_timeline_id = kwargs['restaurant_timeline_id']
        comment_id = kwargs['comment_id']

        user = request.user
        comment_qs = (
            RestaurantTimelineComment.objects.select_related('writer')
            .filter(id=comment_id, restaurant_timeline_id=restaurant_timeline_id, writer=user, is_active=True))

        if not comment_qs:
            data = {
                'error': '해당 댓글이 존재하지 않습니다.'
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)

        comment_qs.update(is_active=False)

        data = {
            'message': '삭제되었습니다.',
            'comment_id': comment_id
        }
        return JsonResponse(data, status=HTTPStatus.OK)
