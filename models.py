from tortoise.models import Model
from tortoise import fields, validators

time_signature_validator = [
    validators.RegexValidator(pattern='^[0-9]+/[0-9]+$', flags=0),
]


class User(Model):
    discord_user_id = fields.BigIntField(unique=True)
    user_name = fields.CharField(max_length=100)
    experience = fields.IntField(default=0)
    register_date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name}. Discord ID: {self.discord_user_id}"

class Warning(Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT)
    reason = fields.CharField(max_length=200)
    message = fields.CharField(max_length=1000)
    date = fields.DatetimeField(auto_now_add=True)
    def __str__(self):
        return f"Warning: {self.user} - {self.reason}"
    
class Suggestion(Model):
    suggester = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT, related_name='suggester') #null true?
    reviewer = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT, related_name='suggestion_reviewer', null=True)
    title = fields.CharField(max_length=200)
    content = fields.CharField(max_length=2000)
    resolution = fields.CharField(max_length=2000, null=True)
    date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.suggester} suggested:\n{self.title}\n{self.content}"
        
class LevelPerformance(Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT)
    trials = fields.IntField(default=0)
    successes = fields.IntField(default=0)
    last_tried = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Performance: {self.successes}/{self.trials}"

class IntervalRecognitionLevel(Model):
    level_number = fields.IntField(unique=True, pk=True)
    description = fields.CharField(max_length=1000)
    interval = fields.IntField(default=0)
    direction = fields.CharField(max_length=100)
    performance = fields.ForeignKeyField('models.LevelPerformance', on_delete=fields.RESTRICT, null=True)
    def __str__(self):
        return f"Interval Recognition Level {self.level_number}"
    
class ChordRecognitionLevel(Model):
    level_number = fields.IntField(unique=True, pk=True)
    description = fields.CharField(max_length=1000)
    chord_type = fields.CharField(max_length=100)
    shape = fields.CharField(max_length=100,validators=[validators.CommaSeparatedIntegerListValidator(allow_negative=False)])
    inversion = fields.CharField(max_length=100)
    performance = fields.ForeignKeyField('models.LevelPerformance', on_delete=fields.RESTRICT, null=True)
    def __str__(self):
        return f"Chord Recognition Level {self.level_number}"


class ModeRecognitionLevel(Model):
    level_number = fields.IntField(unique=True, pk=True)
    description = fields.CharField(max_length=1000)
    performance = fields.ForeignKeyField('models.LevelPerformance', on_delete=fields.RESTRICT, null=True)
    name = fields.CharField(max_length=100)
    shape = fields.CharField(max_length=100, validators=[validators.CommaSeparatedIntegerListValidator(allow_negative=False)])
    characteristic_notes = fields.CharField(max_length=100, validators=[validators.CommaSeparatedIntegerListValidator(allow_negative=False)])
    presentation = fields.CharField(max_length=100)
    def __str__(self):
        return f"Mode Recognition Level {self.level_number}"

class MelodicDictationLevel(Model):
    level_number = fields.IntField(unique=True, pk=True)
    description = fields.CharField(max_length=1000)
    length = fields.IntField(default=0)
    time_signature = fields.CharField(max_length=100, default="4/4", validators=time_signature_validator)
    performance = fields.ForeignKeyField('models.LevelPerformance', on_delete=fields.RESTRICT, null=True)
    def __str__(self):
        return f"Melodic Dictation Level {self.level_number}"
    
class FrequencyRecognitionLevel(Model):
    level_number = fields.IntField(unique=True, pk=True)
    description = fields.CharField(max_length=1000)
    frequency_thresholds = fields.CharField(max_length=100, validators=[validators.CommaSeparatedIntegerListValidator(allow_negative=False)])
    performance = fields.ForeignKeyField('models.LevelPerformance', on_delete=fields.RESTRICT, null=True)
    def __str__(self):
        return f"Frequency Recognition Level {self.level_number}"

class Excercise(Model):
    title = fields.CharField(max_length=100, unique=True)
    description = fields.CharField(max_length=1000)
    difficulty = fields.IntField(default=0)
    def __str__(self):
        return f"Excercise: {self.title}"

class Tune(Model):
    excercise = fields.ForeignKeyField('models.Excercise', on_delete=fields.RESTRICT)
    author = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT)
    title = fields.CharField(max_length=200)    
    description = fields.CharField(max_length=1000)
    date = fields.DatetimeField(auto_now_add=True)
    def __str__(self):
        return f"Tune: {self.author} - {self.title}"
    class Meta:
        unique_together = ('author', 'title',)

class Phrase(Model):
    author = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT, related_name='author')
    reviewer = fields.ForeignKeyField('models.User', on_delete=fields.RESTRICT, related_name='phrase_reviewer', default=None, null=True)
    content = fields.CharField(max_length=400)
    context = fields.CharField(max_length=1000)
    approved = fields.BooleanField(default=None, null=True)
    date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.content

