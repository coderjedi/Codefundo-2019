from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class VoterInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voterid=models.IntegerField(blank=False)
    aadhar=models.IntegerField(blank=False)
    dob=models.DateField(blank=False)
    hasVoted=models.BooleanField(default=False)
    pin=models.IntegerField(blank=False,null=True)
    contractid=models.IntegerField(default=0)
    is_Verified=models.BooleanField(default=False)
    constituency=models.CharField(blank=False,max_length=256)
    def __str__(self):
        return str(self.aadhar)

class CandidateInfo(models.Model):
    candidateid=models.AutoField(primary_key=True)
    name=models.CharField(blank=False,max_length=256)
    party=models.CharField(blank=False,max_length=256)
    assets=models.IntegerField(blank=False)
    criminal_cases=models.IntegerField(blank=False)
    vote_count=models.IntegerField(default=0)


    def __str__(self):
        return str(self.candidateid)
