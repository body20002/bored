from tortoise import fields, models

from . import enums


class Activity(models.Model):
    id = fields.IntField(pk=True)
    accessibility = fields.CharEnumField(enums.Accessibility)
    activity = fields.CharField(max_length=200)
    duration = fields.CharEnumField(enums.Duration)
    kid_friendly = fields.BooleanField()
    link = fields.CharField(max_length=200)
    participants = fields.CharEnumField(enums.Participants)
    price = fields.CharEnumField(enums.Price)
    type = fields.CharEnumField(enums.Types)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Activity {id}"
