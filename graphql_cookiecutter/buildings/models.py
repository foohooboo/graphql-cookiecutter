from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=255)
    size = models.PositiveSmallIntegerField()
    owner = models.ForeignKey('users.User', related_name='buildings', blank=True, null=True)

    def __str__(self):
        return self.name

class Floor(models.Model):
    building = models.ForeignKey(Building, related_name='floors')
    size = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} - {}'.format(self.building.name, self.number)

class Room(models.Model):
    floor = models.ForeignKey(Floor, related_name='rooms')
    size = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.floor, self.name)
