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


# ======================= AGENTS ==========================

class AgentRole(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class AgentAbility(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    description = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    developerName = models.CharField(max_length=120, null=True, blank=True)

    icon = models.URLField(max_length=200, blank=True, null=True)
    icon_small = models.URLField(max_length=200, blank=True, null=True)
    bust_image = models.URLField(max_length=200, blank=True, null=True)
    full_image = models.URLField(max_length=200, blank=True, null=True)
    full_image_v2 = models.URLField(max_length=200, blank=True, null=True)
    background_image = models.URLField(max_length=200, blank=True, null=True)

    role = models.ForeignKey(AgentRole, on_delete=models.CASCADE, blank=True, null=True)

    ability1 = models.ForeignKey(AgentAbility, on_delete=models.CASCADE, related_name='ability1', null=True)
    ability2 = models.ForeignKey(AgentAbility, on_delete=models.CASCADE, related_name='ability2', null=True)
    grenade = models.ForeignKey(AgentAbility, on_delete=models.CASCADE, related_name='grenade', null=True)
    ultimate = models.ForeignKey(AgentAbility, on_delete=models.CASCADE, related_name='ultimate', null=True)
    passive = models.ForeignKey(AgentAbility, on_delete=models.CASCADE, related_name='passive', null=True)

    def __str__(self):
        return self.name