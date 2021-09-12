from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        else:
            return super().delete()

class ServerType(DateTimeModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DiskType(DateTimeModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ServerOwner(DateTimeModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ServerLocation(DateTimeModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

MEMORY_CHOICES = [
    ('MB', 'MB'),
    ('GB', 'GB'),
    ('TB', 'TB'),
    ('PB', 'PB'),
    ('EB', 'EB'),
    ('ZB', 'ZB'),
]

class Server(DateTimeModel):
    name = models.CharField(max_length=255)
    server_type = models.ForeignKey(ServerType, verbose_name="Server Type", on_delete=models.CASCADE)
    disk_type = models.ForeignKey(DiskType, verbose_name="Disk Type", on_delete=models.CASCADE)
    server_owner = models.ForeignKey(ServerOwner, verbose_name="Server Owner", on_delete=models.CASCADE)
    server_location =  models.ForeignKey(ServerLocation, verbose_name="Server Location", on_delete=models.CASCADE)
    cpu = models.TextField()
    ram = models.CharField(max_length=255)
    memory_size = models.CharField(max_length=255, choices=MEMORY_CHOICES)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    public_ip = models.GenericIPAddressField()
    private_ip = models.GenericIPAddressField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def ram_size(self):
        return self.ram + ' ' + self.memory_size


