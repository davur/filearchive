from django.db import models

class Root(models.Model):
    name = models.CharField(max_length=255)
    abspath = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def root_paths(self):
        return self.path_set.filter(parent__isnull=True)


class Path(models.Model):
    class FileType(models.TextChoices):
        DIRECTORY = 'd', 'Directory'
        FILE = 'f', 'File'
        IGNORED = 'i', 'Ignored'

    name = models.CharField(max_length=255, blank=False, null=False)
    root = models.ForeignKey('Root', on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
        related_name='children',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        )
    file_type = models.CharField(
        max_length=1,
        choices=FileType.choices,
    )
    modified_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
