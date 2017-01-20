from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django import shortcuts


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
import models

def craft_response(is_successful, data, *args, **kwargs):
    output = {'status' : 'success' if is_successful else 'failure'}
    output.update(data)
    return JsonResponse(data, *args, **kwargs)

def craft_success_response(data, *args, **kwargs):
    return craft_response(True, data, *args, **kwargs)

def craft_failure_response(data, *args, **kwargs):
    return craft_response(False, data, *args, **kwargs)



class AuthenticatedView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

class IndexView(AuthenticatedView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse({'test_get': 1, 'test_get1' : 2})

    def post(self, request):
        return JsonResponse({'test_post': 1, 'test_post1' : 2})

class AuthorView(AuthenticatedView):
    def get(self, request):
        params = request.GET
        authors = models.Author.objects

        has_filter = False
        if 'id' in params:
            result = shortcuts.get_object_or_404(models.Author, pk = params['id'])
            return craft_success_response(result.jsonize())
        elif params.get('full_name'):
            has_filter = True
            authors = authors.filter(full_name__icontains = params['full_name'])
        elif params.get('university'):
            has_filter = True
            authors = authors.filter(university__icontains = params['university'])

        if has_filter:
            return craft_success_response({'found_authors' : [author.jsonize() for author in authors]})
        else:
            return HttpResponseBadRequest('Missing filter for authors.')


class PaperView(AuthenticatedView):
    def get(self, request):
        params = request.GET
        if 'id' in params:
            result = shortcuts.get_object_or_404(models.Paper, pk = params['id'])
            return craft_success_response(result.jsonize())
        else:
            return craft_failure_response({'message' : 'Not supported yet'}, status = 501)

class SessionView(AuthenticatedView):
    def get(self, request):
        return craft_failure_response({'message' : 'Not supported yet'}, status = 501)

class CommentView(AuthenticatedView):
    def get(self, request):
        params = request.GET
        if not 'paper_id' in params:
            return HttpResponseBadRequest('Missing paper_id')

        paper_id = params['paper_id']
        paper = shortcuts.get_object_or_404(models.Paper, pk = paper_id)
        comments = models.Comment.objects.filter(paper = paper).order_by('time')
        return craft_success_response({'result' : [comment.jsonize() for comment in comments]})

    def post(self, request):
        params = request.POST

        assert request.user # Really sanity check
        if 'paper_id' not in params:
            return HttpResponseBadRequest('Missing paper_id')

        paper = shortcuts.get_object_or_404(models.Paper, pk = params['paper_id'])

        if 'text' not in params:
            return HttpResponseBadRequest('Missing text for comment')

        new_comment = models.Comment(paper = paper, user = request.user, text = params['text'])
        new_comment.save()
        return craft_success_response({'id' : new_comment.id})


    def delete(self, request):
        params = request.DELETE

        if 'id' not in params:
            return HttpResponseBadRequest('Missing comment id')

        comment = shortcuts.get_object_or_404(models.Comment, pk = params['id'])
        comment.delete()

        return craft_success_response({})

class LikeView(AuthenticatedView):
    def get(self, request):
        params = request.GET
        if not 'paper_id' in params:
            return HttpResponseBadRequest('Missing paper_id')

        paper_id = params['paper_id']
        paper = shortcuts.get_object_or_404(models.Paper, pk = paper_id)
        likes = models.Like.objects.filter(paper = paper).order_by('time')
        return craft_success_response({'result' : [like.jsonize() for like in likes]})

    def post(self, request):
        params = request.POST

        assert request.user # Really sanity check
        if 'paper_id' not in params:
            return HttpResponseBadRequest('Missing paper_id')

        paper = shortcuts.get_object_or_404(models.Paper, pk = params['paper_id'])
        new_like = models.Like(paper = paper, user = request.user)
        new_like.save()
        return craft_success_response({'id' : new_like.id})

    def delete(self, request):
        params = request.DELETE

        if 'id' not in params:
            return HttpResponseBadRequest('Missing like id')

        like = shortcuts.get_object_or_404(models.Comment, pk = params['id'])
        like.delete()

        return craft_success_response({})
