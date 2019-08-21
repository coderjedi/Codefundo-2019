from django import forms
from django.conf import settings
import requests
from django.contrib.auth.models import User
from vote.models import VoterInfo,CandidateInfo

class VoterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields={'username','email','password'}

class VoterinfoForm(forms.ModelForm):
    class Meta():
        model=VoterInfo
        fields={'voterid','aadhar','dob','pin','constituency'}

class DictionaryForm(forms.Form):
    applicationid = forms.IntegerField()

    def search(self):
        result = {}
        post_data = {
                    "externalID": "b039f6dc-351b-4e84-96fa-f3b1569cdca7",
                    "firstName": "ABCD",
                    "lastName": "EFGH",
                    "emailAddress": "testuser"
                    }
        applicationid = self.cleaned_data['applicationid']
        # endpoint = 'https://voteapp-iyby7e-api.azurewebsites.net/api/v2/applications/{application_id}/'
        endpoint = 'https://voteapp-iyby7e-api.azurewebsites.net/api/v2/users/'
        url = endpoint
        headers = {'Content-Type':'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSIsImtpZCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSJ9.eyJhdWQiOiJlYTM5MzBhNy05MWRkLTRhNzUtOWY3YS0yMWRjZDNkODgzYzYiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYjI5M2I5NC00YWZkLTQxMTYtOGQzZS1iZDNmZWJiZDEyZGUvIiwiaWF0IjoxNTY0OTQxMjYyLCJuYmYiOjE1NjQ5NDEyNjIsImV4cCI6MTU2NDk0NTE2MiwiYWlvIjoiQVZRQXEvOE1BQUFBN20vNnhjeFhudEgvdkJBR0JKOFFxWWdvRUlPcERrUWFTRWlCVkF1TlNkTXZudEl5Nk9wOE5ENVpETGhwa2R5VUxmUEZZZFI3QUEyeXVHTXBMRVJNZVhqRVlnQlROenBDVW14WEEzQ0JIZzA9IiwiYW1yIjpbInB3ZCJdLCJjX2hhc2giOiI2allPeERVUk5TdXFhWHJDLUxUWEpnIiwiZW1haWwiOiJoaW1hbnNodTMxMDk5QGdtYWlsLmNvbSIsImZhbWlseV9uYW1lIjoiUGFuZGV5IiwiZ2l2ZW5fbmFtZSI6IkhpbWFuc2h1IiwiaWRwIjoibGl2ZS5jb20iLCJpcGFkZHIiOiIxMzYuMjMzLjMzLjgyIiwibmFtZSI6IkhpbWFuc2h1IFBhbmRleSIsIm5vbmNlIjoiNDY1NWVkMzAtZTQyMS00M2NkLWI2ZWItN2YyN2E3OGQzNDZmIiwib2lkIjoiMGM2YmZjMzgtMTVjOC00Yjc5LWExNjAtZWRkODQzOTA5NTI2Iiwicm9sZXMiOlsiQWRtaW5pc3RyYXRvciJdLCJzdWIiOiJZUjVCUm9Reklrb1NwT1ZqVVFFZ1Fic3pJSzl2SGNHdm5MYVRXd2M2VVVFIiwidGlkIjoiZGIyOTNiOTQtNGFmZC00MTE2LThkM2UtYmQzZmViYmQxMmRlIiwidW5pcXVlX25hbWUiOiJsaXZlLmNvbSNoaW1hbnNodTMxMDk5QGdtYWlsLmNvbSIsInV0aSI6Inh3OUJzVmpNZWtlOHItemR0VXRCQUEiLCJ2ZXIiOiIxLjAifQ.K3asdi1eHXOEqQkB7xlUW6JXSNRwVwopMmh1YBKp4wLnKbzL5xwkWM5xKBF_aL_NTaniUf-T3Zh0kxbE5uC8H00y6bbBUm85KhL_ldwX3yGompJT1s0eTkuF4XFHucoFNSLNYCYlRXzaBeaiy_CCb6-imjSbAaGlTRkEJCCJUmuAREb6pwTqr-stB-1v1ktTysccf-iJcFoWcxDK6rOGD4FT0iQ_s7hpaES8TpeGf4fkrh9E-j4OrWb-efedE35EDatcf2bG7no-wBAHmR78ww7TRWf2fZfLIUp8cKKZKLZIDbV44EZQU9v_3I3oNilZWjcVjU0MUvfu1hkYrk7YQg'}
        response = requests.post(url, headers=headers,json=post_data)
        if response.status_code == 200:  # SUCCESS
            result = response.json()
            print(result)
            result['success'] = True
            result['message'] = 'Success'
        else:
            result['success'] = False
            if response.status_code == 404:  # NOT FOUND
                result['message'] = 'No entry found'
            if response.status_code == 400:
                result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
            else:
                result['message'] =' response.status_code'
        return result
