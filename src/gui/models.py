from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(null=True)
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """
        Update timestamps  
        """
        if _first_save(self):
            self.created = timezone.now()
        
        return super(Post, self).save(*args, **kwargs) 

    def __str__(self):
        return self.title
            

def _first_save(post):
    return True if not post.id else False