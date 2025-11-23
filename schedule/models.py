from django.db import models

class Conference(models.Model):
    FORMAT_CHOICES = [
        ('bca', 'Từ Bộ Công an'),
        ('xuong_co_so', 'Xuống cơ sở'),
        ('tinh_uy', 'Từ Tỉnh ủy'),
    ]

    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='bca')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='participants', null=True, blank=True)

    def __str__(self):
        if self.location:
            return f"{self.name} - {self.location.name}"
        return f"{self.name} (Unassigned)"
