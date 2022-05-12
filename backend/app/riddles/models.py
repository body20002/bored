from tortoise import fields, models

from . import enums


class Riddle(models.Model):
    id = fields.IntField(pk=True)
    question = fields.CharField(max_length=300)
    answer = fields.CharField(max_length=300)
    difficulty = fields.CharEnumField(enums.Difficulty)
    source = fields.CharField(max_length=200)
