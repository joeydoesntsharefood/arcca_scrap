from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

class Brand(models.Model):
  name = models.CharField(max_length=300)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  def __str__(self):
    return self.name
  
class Interaction(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  createdAt = models.CharField(max_length=300)
  avatar = models.CharField(max_length=300)
  rating = models.CharField(max_length=300)
  name = models.CharField(max_length=300)
  comment = models.CharField(max_length=300)
  comment_imgs = ArrayField(models.CharField(max_length=200), blank=True, default=list)
  brand = models.CharField(max_length=300)

  def __str__(self):
    return self.name
  