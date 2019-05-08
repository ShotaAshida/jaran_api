from django.conf import settings
from django.db import models

class jaranOnsenPost(models.Model):
    #reg = models.IntegerField()
    #pref = models.IntegerField()
    l_area = models.IntegerField()
    #s_area = models.IntegerField()
    #onsen_q = models.IntegerField()
    #start = models.IntegerField()
    count = models.IntegerField()
    xml_ptn = models.IntegerField()

class jaranOnsen(models.Model):
    onsen_name = models.TextField()
    onsen_name_kana = models.TextField()
    onsen_id = models.IntegerField()
    onsen_address = models.TextField()
    region = models.TextField()
    prefecture = models.TextField()
    large_area = models.TextField()
    small_area = models.TextField()
    nature_of_onsen = models.TextField()
    onsen_area_name = models.TextField()
    onsen_area_name_kana = models.TextField()
    onsen_area_id = models.TextField()
    onsen_area_url = models.TextField()
    onsen_area_caption = models.TextField()

    def __str__(self):
        return self.onsen_name

