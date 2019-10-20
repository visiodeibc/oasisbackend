from django.db import models

class Places(models.Model):

    facilityId = models.CharField(max_length=50)
    facilityType = models.CharField(max_length=60)
    lat = models.FloatField()
    lng = models.FloatField()
    phone = models.CharField(max_length=15)
    accessibility = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return str(self.facilityType) + str(self.id)

    @property
    def descriptions(self):
        return self.descriptions_set.all()
    def review(self):
        return self.review_set.all()


class Descriptions(models.Model):
    places = models.OneToOneField(Places, on_delete=models.CASCADE, primary_key=True, related_name='descriptions')

class enAddress(models.Model):
    descriptions = models.OneToOneField(Descriptions, on_delete=models.CASCADE, primary_key=True, related_name='enAddress')
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)

class hkAddress(models.Model):
    descriptions = models.OneToOneField(Descriptions, on_delete=models.CASCADE, primary_key=True, related_name='hkAddress')
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)

class Review(models.Model):
    places = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField()
    text = models.CharField(max_length=200)
    