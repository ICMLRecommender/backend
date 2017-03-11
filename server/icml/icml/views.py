import uuid

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django import shortcuts

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index2.html', {})