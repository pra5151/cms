from django import forms
from django.contrib.auth.models import User

from .mixins import FormControlMixin
from .models import Server, ServerType, DiskType, ServerOwner, ServerLocation


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':  'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username, is_active=True).first()
        if user == None or not user.check_password(password):
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control error-input'
                })
            raise forms.ValidationError(
                {"username":"Incorrect username or password"}
            )
        return self.cleaned_data


class ServerTypeForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = ServerType
        exclude = ['deleted_at']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if ServerType.objects.filter(name=name, deleted_at__isnull=True).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Server Type with this name already exists")

        return name



class DiskTypeForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = DiskType
        exclude = ['deleted_at']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if DiskType.objects.filter(name=name, deleted_at__isnull=True).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Disk Type with this name already exists")

        return name

class ServerOwnerForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = ServerOwner
        exclude = ['deleted_at']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if ServerOwner.objects.filter(name=name, deleted_at__isnull=True).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Server Owner with this name already exists")

        return name
    

class ServerLocationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = ServerLocation
        exclude = ['deleted_at']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if ServerLocation.objects.filter(name=name, deleted_at__isnull=True).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Server Location with this name already exists")

        return name
    

class ServerForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Server
        exclude = ['deleted_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['server_type'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['disk_type'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['server_owner'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['server_location'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['memory_size'].label=''

        self.fields['server_type'].queryset = self.fields['server_type'].queryset.filter(deleted_at__isnull=True)
        self.fields['disk_type'].queryset = self.fields['disk_type'].queryset.filter(deleted_at__isnull=True)
        self.fields['server_owner'].queryset = self.fields['server_owner'].queryset.filter(deleted_at__isnull=True)
        self.fields['server_location'].queryset = self.fields['server_location'].queryset.filter(deleted_at__isnull=True)

class EmailForm(FormControlMixin, forms.Form):
    email_id = forms.EmailField()
    

class UserForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("User with this email address already exists")
        
        return email
