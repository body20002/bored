from tortoise import models, fields


class Fact(models.Model):
    id = fields.IntField(pk=True)
    fact = fields.CharField(max_length=300)
    source = fields.CharField(max_length=200)
