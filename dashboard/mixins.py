from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.template.loader import get_template

from io import BytesIO, StringIO

from xhtml2pdf import pisa

from .models import Server

class NonLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('dashboard:login')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_superuser or self.request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class GetDeleteMixin:
    def get(self, request, *args, **kwargs):
        if hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class NonDeletedListMixin:
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class GroupRequiredMixin(object):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or self.request.user.groups.filter(name__in=self.group_required).exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
    
class AjaxFormMixin:
    def form_valid(self,form):
        super().form_valid(form)
        return JsonResponse({'url': self.success_url}, status=200)
        
        
    def form_invalid(self,form):
        if self.request.is_ajax():
            return JsonResponse({'errors':form.errors}, status=400)
        return super().form_invalid(form)