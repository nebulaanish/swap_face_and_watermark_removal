
from typing import Any
from django.db import models

class Image(models.Model):
    image_url = models.URLField(max_length=255, default="") 
    face_url = models.URLField(max_length=255, default="")
    result_url = models.URLField(null=True, blank=True)
    result_image_path = models.CharField(max_length=255, null=True, blank=True)
    mask_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Image : {self.pk}"
    
class FaceImage(models.Model):
    image_url = models.URLField(max_length=255, default="")
    face_url = models.URLField(max_length=255, default="")

    def __call__(self):
        return f"FaceImage : {self.pk}"

class WatermarkImage(models.Model):
    

    def __call__(self):
        return f"WatermarkImage : {self.pk}"