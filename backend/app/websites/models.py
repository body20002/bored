from tortoise import models, fields


class Website(models.Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=200)
    description = fields.CharField(max_length=240)
