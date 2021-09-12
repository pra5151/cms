from django.conf import settings as conf_settings
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView, 
    TemplateView, 
    FormView, 
    UpdateView,
    View
)


from .models import Server, ServerType, DiskType, ServerOwner, ServerLocation
from.filters import ServerFilter
from .forms import (
    LoginForm, 
    ServerForm, 
    EmailForm, 
    ServerTypeForm, 
    DiskTypeForm, 
    ServerOwnerForm, 
    ServerLocationForm, 
    UserForm
    )
from .mixins import (
    NonDeletedListMixin,
    NonLoginRequiredMixin,
    CustomLoginRequiredMixin,
    GetDeleteMixin,
    GroupRequiredMixin,
    AjaxFormMixin
)

from .utils import pdf_report_create


# Create your views here.
class DashboardView(CustomLoginRequiredMixin, TemplateView):
    template_name = "dashboard/layouts/home.html"

# Login Logout Views
class LoginPageView(NonLoginRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "dashboard/auth/login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        # Remember me
        if self.request.POST.get('remember', None) == None:
            self.request.session.set_expiry(0)

        login(self.request, user)

        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('dashboard:home')

class LogoutView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard:login')


# Server Type Crud
class ServerTypeListView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, ListView):
    model = ServerType
    template_name = 'dashboard/server_type/list.html'
    paginate_by = 10
    group_required = ['Admin']


class ServerTypeCreateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, CreateView):
    form_class = ServerTypeForm
    template_name = 'dashboard/server_type/form.html'
    success_message = "Server Type Has Been Created Successfully"
    success_url = reverse_lazy('dashboard:server-type-list')
    group_required = ['Admin']
    
    
class ServerTypeUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, UpdateView):
    model = ServerType
    form_class = ServerTypeForm
    template_name = 'dashboard/server_type/form.html'
    success_message = "Server Type Has Been Updated Successfully"
    success_url = reverse_lazy('dashboard:server-type-list')
    group_required = ['Admin']

class ServerTypeDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, GroupRequiredMixin, GetDeleteMixin, DeleteView):
    model = ServerType
    success_message = "Server Type Has Been Deleted Successfully"
    success_url = reverse_lazy('dashboard:server-type-list')
    group_required = ['Admin']

# Disk Type Crud
class DiskTypeListView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, ListView):
    model = DiskType
    template_name = 'dashboard/disk_type/list.html'
    paginate_by = 10
    group_required = ['Admin']

class DiskTypeCreateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, CreateView):
    form_class = DiskTypeForm
    template_name = 'dashboard/disk_type/form.html'
    success_message = "Disk Type Has Been Created Successfully"
    success_url = reverse_lazy('dashboard:disk-type-list')
    group_required = ['Admin']

class DiskTypeUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, SuccessMessageMixin, AjaxFormMixin, UpdateView):
    model = DiskType
    form_class = DiskTypeForm
    template_name = 'dashboard/disk_type/form.html'
    success_message = "Disk Type Has Been Updated Successfully"
    success_url = reverse_lazy('dashboard:disk-type-list')
    group_required = ['Admin']

class DiskTypeDeleteView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, SuccessMessageMixin, GetDeleteMixin, DeleteView):
    model = DiskType
    success_message = "Disk Type Has Been Deleted Successfully"
    success_url = reverse_lazy('dashboard:disk-type-list')
    group_required = ['Admin']

# Server Owner Crud
class ServerOwnerListView(CustomLoginRequiredMixin, GroupRequiredMixin, NonDeletedListMixin, ListView):
    model = ServerOwner
    template_name = 'dashboard/server_owner/list.html'
    paginate_by = 10
    group_required = ['Admin']

class ServerOwnerCreateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, CreateView):
    form_class = ServerOwnerForm
    template_name = 'dashboard/server_owner/form.html'
    success_message = "Server Owner Has Been Created Successfully"
    success_url = reverse_lazy('dashboard:server-owner-list')
    group_required = ['Admin']
    

class ServerOwnerUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, UpdateView):
    model = ServerOwner
    form_class = ServerOwnerForm
    template_name = 'dashboard/server_owner/form.html'
    success_message = "Server Owner Has Been Updated Successfully"
    success_url = reverse_lazy('dashboard:server-owner-list')
    group_required = ['Admin']

class ServerOwnerDeleteView(CustomLoginRequiredMixin,NonDeletedListMixin,  SuccessMessageMixin, GroupRequiredMixin, GetDeleteMixin, DeleteView):
    model = ServerOwner
    success_message = "Server Owner Has Been Deleted Successfully"
    success_url = reverse_lazy('dashboard:server-owner-list')
    group_required = ['Admin']

# Server Location Crud
class ServerLocationListView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, ListView):
    model = ServerLocation
    template_name = 'dashboard/server_location/list.html'
    paginate_by = 10
    group_required = ['Admin']

class ServerLocationCreateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, CreateView):
    form_class = ServerLocationForm
    template_name = 'dashboard/server_location/form.html'
    success_message = "Server Location Has Been Created Successfully"
    success_url = reverse_lazy('dashboard:server-location-list')
    group_required = ['Admin']

class ServerLocationUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, AjaxFormMixin, SuccessMessageMixin, UpdateView):
    model = ServerLocation
    form_class = ServerLocationForm
    template_name = 'dashboard/server_location/form.html'
    success_message = "Server Location Has Been Updated Successfully"
    success_url = reverse_lazy('dashboard:server-location-list')
    group_required = ['Admin']

class ServerLocationDeleteView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, SuccessMessageMixin, GetDeleteMixin, DeleteView):
    model = ServerLocation
    success_message = "Server Location Has Been Deleted Successfully"
    success_url = reverse_lazy('dashboard:server-location-list')
    group_required = ['Admin']

# Server  Crud
class ServerListView(CustomLoginRequiredMixin, NonDeletedListMixin, ListView):
    model = Server
    template_name = 'dashboard/server/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = ServerFilter(data=self.request.GET, queryset=queryset)
        return filters.qs.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ServerFilter(self.request.GET)
        return context

class ServerCreateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ServerForm
    template_name = 'dashboard/server/form.html'
    success_message = "Server Has Been Created Successfully"
    success_url = reverse_lazy('dashboard:server-list')
    group_required = ['Admin']

class ServerUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'dashboard/server/form.html'
    success_message = "Server Has Been Updated Successfully"
    success_url = reverse_lazy('dashboard:server-list')
    group_required = ['Admin']

class ServerDetailView(CustomLoginRequiredMixin, NonDeletedListMixin, DetailView):
    model = Server
    template_name = 'dashboard/server/detail.html'
    object_list = "server"

class ServerDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, GroupRequiredMixin, GetDeleteMixin, DeleteView):
    model = Server
    success_message = "Server Has Been Deleted Successfully"
    success_url = reverse_lazy('dashboard:server-list')
    group_required = ['Admin']

# Server List PDF
class ServerPDFGeneratorView(CustomLoginRequiredMixin, GroupRequiredMixin, View):
    group_required = ['Admin']

    def get_pdf(self):
        context = {'servers': Server.objects.filter(deleted_at__isnull=True), 'current_date':timezone.now()}
        pdf = pdf_report_create('dashboard/pdf/report.html', 'Report.pdf', context)
        return pdf

    def get(self, *args, **kwargs):
        return HttpResponse(self.get_pdf(), content_type='application/pdf')

class ServerPDFMailView(CustomLoginRequiredMixin, GroupRequiredMixin, FormView):
    form_class = EmailForm
    template_name = 'dashboard/pdf/email_form.html'
    group_required = ['Admin']
    
    def get_success_url(self):
        return reverse_lazy('dashboard:server-list')
    
    def get_pdf(self):
        context = {'servers': Server.objects.filter(deleted_at__isnull=True), 'current_date':timezone.now()}
        pdf = pdf_report_create('dashboard/pdf/report.html', 'Report.pdf', context)
        return pdf

    def form_valid(self, form):
        email_id = form.cleaned_data.get('email_id')
        email = EmailMessage("Server Report", 'Please find the attached pdf', conf_settings.EMAIL_HOST_USER, [email_id])
        email.attach('Report.pdf', self.get_pdf().getvalue())
        email.send(fail_silently=False)
        messages.success(self.request, "PDF has been send to the given Email Address")
        return redirect(self.get_success_url())


# User Crud
class UserListView(CustomLoginRequiredMixin, GroupRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users/list.html"
    paginate_by = 100
    group_required = ['Admin']

    def get_queryset(self):
        return super().get_queryset().exclude(username=self.request.user)

class UserCreateView(CustomLoginRequiredMixin, GroupRequiredMixin, SuccessMessageMixin, CreateView):
    form_class= UserForm
    success_message = "User Created Successfully"
    success_url = reverse_lazy('dashboard:user-list')
    template_name = "dashboard/users/form.html"
    group_required = ['Admin']

    def get_success_url(self):
        return reverse('dashboard:user-password-reset', kwargs={'pk': self.object.pk })

class UserUpdateView(CustomLoginRequiredMixin, GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserForm
    model = User
    success_message = "User Updated Successfully"
    success_url = reverse_lazy('dashboard:user-list')
    template_name = "dashboard/users/form.html"
    group_required = ['Admin']

class UserStatusView(CustomLoginRequiredMixin, GroupRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_message = "User's Status Has Been Changed"
    success_url = reverse_lazy('dashboard:user-list')

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        if user_id:
            account = User.objects.filter(pk=user_id).first()
            if account.is_active == True:
                account.is_active = False
            else:
                account.is_active = True
            account.save(update_fields=['is_active'])
        return redirect(self.success_url)


# Password Reset
class UserPasswordResetView(CustomLoginRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_url = reverse_lazy("dashboard:user-list")
    success_message = "Password has been sent to the user's email."

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        account = User.objects.filter(pk=user_pk).first()
        password = get_random_string(length=6)
        account.set_password(password)
        msg = (
            "You can login into the Credential Management System Dashboard with the following credentials.\n\n" + "Username: " + account.username + " \n" + "Password: " + password
        )
        send_mail("Dashboard Credentials", msg, conf_settings.EMAIL_HOST_USER, [account.email], fail_silently=True)
        account.save(update_fields=["password"])

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
