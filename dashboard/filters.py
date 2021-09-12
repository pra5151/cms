import django_filters

from django_filters import filters


from .models import Server

class ServerFilter(django_filters.FilterSet):

    class Meta:
        model = Server
        fields = {
            'name': ['icontains'],
            'server_type': ['exact'],
            'public_ip': ['icontains'],
            'username': ['icontains'],

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name__icontains'].field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by Name'})
        self.filters['name__icontains'].field.label = ''
        self.filters['server_type'].field.widget.attrs.update({'class': 'form-control select2'})
        self.filters['server_type'].field.label = ''
        self.filters['server_type'].field.empty_label = 'Select Server Type'
        self.filters['public_ip__icontains'].field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by IP Address'})
        self.filters['public_ip__icontains'].field.label = ''
        self.filters['username__icontains'].field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by Username'})
        self.filters['username__icontains'].field.label = ''

