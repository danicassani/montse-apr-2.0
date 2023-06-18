from db.PostgresDB import PgDB
from discord import User as DiscordUser
from datetime import datetime

from django.db import models
from manage import init_django

init_django()

class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
# class AuditionPathProfile(Model):
#     def __init__(self, skillpath: str):
#         self.skillpath = skillpath
#         self.trials = 0
#         self.successes = 0
#         self.last_trial = None
#         super().__init__()

#     def save(self):
#         query = f"""INSERT INTO audition_path_profiles (id, name, path, profile)
#         VALUES ({self.id}, '{self.name}', '{self.path}', '{self.profile}');"""
#         # self.pgdb.save(query)
    


class User(Model):
    discord_user_id = models.BigIntegerField(unique=True)
    experience = models.IntegerField(default=0)
    register_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.discord_user_id}"