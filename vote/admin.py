from django.contrib import admin
from vote.models import VoterInfo,CandidateInfo
# Register your models here.
admin.site.register(VoterInfo)
admin.site.register(CandidateInfo)
