import sys
import django 
from django.utils import timezone
from django.core.validators import int_list_validator
from django.core import validators
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

django.setup()

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


time_signature_validator = [
    validators.RegexValidator(
        regex='^[0-9]+/[0-9]+$',
        message='Time signature must be in the form of "X/Y".',
        code='invalid_time_signature'
    )
]

class Warning(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    reason = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Warning: {self.user} - {self.reason}"

class User(models.Model):
    discord_user_id = models.BigIntegerField(unique=True)
    experience = models.IntegerField(default=0)
    register_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.discord_user_id}"
    
class LevelPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    trials = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    last_tried = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Performance: {self.successes}/{self.trials}"

class IntervalRecognitionLevel(models.Model):
    level_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=1000)
    interval = models.IntegerField(default=0)
    direction = models.CharField(max_length=100)
    performance = models.ForeignKey(LevelPerformance, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return f"Interval Recognition Level {self.level_number}"
    
class ChordRecognitionLevel(models.Model):
    level_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=1000)
    chord_type = models.CharField(max_length=100)
    shape = models.CharField(validators=[int_list_validator])
    inversion = models.CharField(max_length=100)
    performance = models.ForeignKey(LevelPerformance, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return f"Chord Recognition Level {self.level_number}"


class ModeRecognitionLevel(models.Model):
    level_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=1000)
    performance = models.ForeignKey(LevelPerformance, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100)
    shape = models.CharField(validators=[int_list_validator])
    characteristic_notes = models.CharField(validators=[int_list_validator])
    presentation = models.CharField(max_length=100)
    def __str__(self):
        return f"Mode Recognition Level {self.level_number}"

class MelodicDictationLevel(models.Model):
    level_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=1000)
    length = models.IntegerField(default=0)
    time_signature = models.CharField(max_length=100, default="4/4", validators=time_signature_validator)
    performance = models.ForeignKey(LevelPerformance, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return f"Melodic Dictation Level {self.level_number}"
    
class FrequencyRecognitionLevel(models.Model):
    level_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=1000)
    frequency_thresholds = models.CharField(validators=[int_list_validator])
    performance = models.ForeignKey(LevelPerformance, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return f"Frequency Recognition Level {self.level_number}"

class Excercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    difficulty = models.IntegerField(default=0)
    def __str__(self):
        return f"Excercise: {self.name}"

class Tune(models.Model):
    excercise = models.ForeignKey(Excercise, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)    
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Tune: {self.author} - {self.title}"
    class Meta:
        unique_together = ('author', 'title',)

class Phrase(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reviewer')
    content = models.CharField(max_length=300)
    context = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

