import json
from os import path
from django.db import models


# ======================= USERS ==========================

class PlayerCard(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=120)

    icon = models.URLField(max_length=200, blank=True, null=True)
    small_art = models.URLField(max_length=200, blank=True, null=True)
    wide_art = models.URLField(max_length=200, blank=True, null=True)
    large_art = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class PlayerTitle(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class User(models.Model):
    puuid = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=5)
    card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE, null=True)
    title = models.ForeignKey(PlayerTitle, on_delete=models.CASCADE, null=True)
    recent_matches = models.JSONField()

    def __str__(self):
        return f"{self.name}#{self.tag}"