from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.


class IndexView(GenericAPIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		return JsonResponse({'test': 1, 'test1' : 2})