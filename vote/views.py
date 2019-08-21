from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from vote.forms import VoterForm,VoterinfoForm
from django.contrib.auth.decorators import login_required
from .models import VoterInfo,CandidateInfo,User
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# from .forms import DictionaryForm
import requests
import json
from adal import AuthenticationContext
from pprint import pprint

AUTHORITY = 'https://login.microsoftonline.com/chiragvmj2012gmail.onmicrosoft.com'
WORKBENCH_API_URL = 'https://safevote-3wpvhp.azurewebsites.net'
RESOURCE = '9569b296-589d-488b-a582-246d957827de'
CLIENT_APP_Id = 'b4d34ae7-b24d-4aab-87a5-a72c23d60dec'
CLIENT_SECRET = '.M-m0UajsaeD*uCc6@WlLigK5oVMPbj8'

@login_required
def index(request):  #redirection after login
    return render(request,'home.html')

def register(request):
    registered=False
    global user
    global contractid
    if request.method=="POST":
        user_form=VoterForm(data=request.POST)
        profile_form=VoterinfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save(commit=False)
            usercopy=user
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            registered=True
            context = {
                "user_form": user_form,
                "profile_form":profile_form,
                "registered": registered,
                "user":user,
            }
            auth_context = AuthenticationContext(AUTHORITY)
            token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
            post_data = {
                "workflowFunctionID": 73,
                "workflowActionParameters": [
                {
                    "name": "Description",
                    "value": str(profile_form.cleaned_data['constituency']),
                    "workflowFunctionParameterId": 249
                },
                {
                    "name": "Name",
                    "value": user_form.cleaned_data['username'],
                    "workflowFunctionParameterId": 250
                },
                {
                    "name": "DOB",
                    "value": str(profile_form.cleaned_data['dob']),
                    "workflowFunctionParameterId": 251
                },
                {
                    "name": "Aadhar",
                    "value": str(profile_form.cleaned_data['aadhar']),
                    "workflowFunctionParameterId": 252
                },
                {
                    "name": "VoterId",
                    "value": str(profile_form.cleaned_data['voterid']),
                    "workflowFunctionParameterId": 253
                },
                {
                    "name": "Pin",
                    "value": str(profile_form.cleaned_data['pin']),
                    "workflowFunctionParameterId": 254
                }
                ]
                }
            endpoint = 'https://safevote-3wpvhp-api.azurewebsites.net/api/v2/contracts'
            # endpoint = 'https://voteapp-iyby7e-api.azurewebsites.net/api/v2/applications/15'
            url = endpoint
            headers = {'Content-Type':'application/json','Authorization': 'Bearer ' + token['accessToken']}
            PARAMS = {'workflowId': 16,
                          'contractCodeId': 16,
                          'connectionId': 1
                        }
            response = requests.post(url, headers=headers,params = PARAMS,data=json.dumps(post_data))
            if response.status_code == 200:  # SUCCESS
                contractid = response.json()
                user1=VoterInfo.objects.get(user=usercopy)
                user1.contractid=contractid
                user1.save()
        else:
            context = {
                "user_form": user_form,
                "profile_form":profile_form,
                "registered": registered,
                }
            return render(request, 'register.html', context)
    else:
        user_form=VoterForm()
        profile_form=VoterinfoForm()
        context = {
            "user_form": user_form,
            "profile_form":profile_form,
            "registered": registered,
            }
    return render(request, 'register.html', context)

def user_login(request):
    if request.method=='POST':
        aadhar=request.POST.get('username')
        password=request.POST.get('password')
        voter=get_object_or_404(VoterInfo,aadhar=aadhar)
        user=authenticate(username=voter.user.username,password=password)
        haserr=False
        if user:
            if user.is_active:
                login(request,user)
                return render(request,'home.html',{'user':user})
            else:
                return HttpResponse("This account is inactive.Please contact admins for more details.")
        else:
            haserr=True
            return render(request,'login.html',{'user':user,'haserr':haserr})
    else:
        return render(request,'login.html',{})



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))




@login_required
def vote(request):
    curruser=VoterInfo.objects.get(user=request.user)
    cands = CandidateInfo.objects.all()
    haserror=False
    if curruser.hasVoted==False:
        verified=False
        auth_context = AuthenticationContext(AUTHORITY)
        token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
        endpoint = 'https://safevote-3wpvhp-api.azurewebsites.net/api/v2/'+str(curruser.contractid)+'/actions'
        url = endpoint
        headers = {'Authorization': 'Bearer ' + token['accessToken']}
        response = requests.get(url, headers=headers)
        # print(token['accessToken'])
        # print(response.text)
        # data=response.json()
        # print(data)
        if True:
            verified=True
            curruser.is_Verified=True
            if request.method=='POST':
                candidateid=request.POST.get('candidateid')
                print(candidateid)
                pin=request.POST.get('pin')
                print(pin)
                post_data= {
                    "workflowFunctionID": 77,
                    "workflowActionParameters": [
                    {
                    "name": "Candidate",
                    "value": str(candidateid),
                    "workflowFunctionParameterId": 247
                    },
                    {
                    "name": "PIN",
                    "value": str(pin),
                    "workflowFunctionParameterId": 248
                    }
                    ]
                    }
                endpoint = 'https://safevote-3wpvhp-api.azurewebsites.net/api/v2/contracts/'+str(curruser.contractid)+'/actions'
                url = endpoint
                headers = {'Content-Type':'application/json','Authorization': 'Bearer ' + token['accessToken']}
                response = requests.post(url, headers=headers,data=json.dumps(post_data))
                if response.status_code == 200:
                    curruser.hasVoted=True  # SUCCESS
                    curruser.save()
                    currcand=CandidateInfo.objects.get(name=candidateid)
                    currcand.vote_count+=1
                    currcand.save()
                    return render(request, 'about.html', {'cands': cands,'curruser':curruser})
                    #vote count display page redirection
                else:
                    print(response.status_code)
                    print(curruser.contractid)
                    haserror=True
                    return render(request,'vote.html',{'verified':verified,'haserror':haserror,'cands': cands,'curruser':curruser})
            else:
                return render(request,'vote.html',{'verified':verified,'haserror':haserror,'cands': cands,'curruser':curruser})#redirect to voting page
        else:
            verified=False
            return render(request,'vote.html',{'verified':verified,'haserror':haserror,'cands': cands,'curruser':curruser})#redirect to voting page
    else:
        return render(request, 'about.html', {'cands': cands,'curruser':curruser})#vote count display page redirection


def oxford(request):
    # search_result = {}
    # if 'applicationid' in request.POST:
    #     form = DictionaryForm(request.POST)
    #     # if form.is_valid():
    #     search_result = form.search()
    # else:
    #     form = DictionaryForm()
    result = {}
    post_data = {
                "externalID": "b039f6dc-351b-4e84-96fa-f3b1569cdca7",
                "firstName": "ABCD",
                "lastName": "EFGH",
                "emailAddress": "testuser"
                }
    # endpoint = 'https://voteapp-iyby7e-api.azurewebsites.net/api/v2/applications/{application_id}/'
    endpoint = 'https://voteapp-iyby7e-api.azurewebsites.net/api/v2/users/5/'
    url = endpoint
    headers = {'Content-Type':'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSIsImtpZCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSJ9.eyJhdWQiOiJlYTM5MzBhNy05MWRkLTRhNzUtOWY3YS0yMWRjZDNkODgzYzYiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYjI5M2I5NC00YWZkLTQxMTYtOGQzZS1iZDNmZWJiZDEyZGUvIiwiaWF0IjoxNTY0OTQ0NTY4LCJuYmYiOjE1NjQ5NDQ1NjgsImV4cCI6MTU2NDk0ODQ2OCwiYWlvIjoiQVZRQXEvOE1BQUFBblY1bUlqMHdJMVp4MnhUYlJkKzZwVE9GMGs1aUVLcCs5V0VxWVNSRGI5MG8yMlBrdTc0eUUxVWVJQ1phNGV1clV2RGs2cTJjY0VGRTRQUHBYZEc1dHQvWFAxcnNUSjNoZnlwdzA5anFmM3c9IiwiYW1yIjpbInB3ZCJdLCJlbWFpbCI6ImhpbWFuc2h1MzEwOTlAZ21haWwuY29tIiwiZmFtaWx5X25hbWUiOiJQYW5kZXkiLCJnaXZlbl9uYW1lIjoiSGltYW5zaHUiLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6IjEzNi4yMzMuMzMuODIiLCJuYW1lIjoiSGltYW5zaHUgUGFuZGV5Iiwibm9uY2UiOiJiODI5YzE1Mi1lOGUzLTRkMWEtODg1Yy05OGNjMjM3NjIzYmIiLCJvaWQiOiIwYzZiZmMzOC0xNWM4LTRiNzktYTE2MC1lZGQ4NDM5MDk1MjYiLCJyb2xlcyI6WyJBZG1pbmlzdHJhdG9yIl0sInN1YiI6IllSNUJSb1F6SWtvU3BPVmpVUUVnUWJzeklLOXZIY0d2bkxhVFd3YzZVVUUiLCJ0aWQiOiJkYjI5M2I5NC00YWZkLTQxMTYtOGQzZS1iZDNmZWJiZDEyZGUiLCJ1bmlxdWVfbmFtZSI6ImxpdmUuY29tI2hpbWFuc2h1MzEwOTlAZ21haWwuY29tIiwidXRpIjoiNXliUC1FXy1DMFc2ZWYtOFQ2bzdBQSIsInZlciI6IjEuMCJ9.nz5WvLisT-CiyI3B0tKXHJ458DFXmp2_3-aAzaaHN_982JYoIMo7PRCGxjita5E-WJz18cH6Wx5PwJznR2o8sH8DUz2-dpEPCuGBSoUeMyIc_p4lvVrdADqMaODiNYFRXcB9OdMP4MJg77oq63OpVzIMlWuPHe54ABrSE3UjSFStVURyf7xAd06pKIcZwKhN0EXifP0IJizgvkEzwqdvH0n563EMxAUwvrY51Lg0DYVax4iNkNzPHR2adI1JgACl7KGoBy3TAqhVJfHAt7IQBH2vSA7jBny--TSaTLnIBfTyfyjq_RAG7-mLkPw9IZbbs5iARseS-JbAugJFppXaFg'}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:  # SUCCESS
        result = response.json()
        print(result)
    #     # result['success'] = True
    #     # result['message'] = 'Success'
    # else:
    #     # result['success'] = False
    #     if response.status_code == 404:  # NOT FOUND
    #         # result['message'] = 'No entry found'
    #     if response.status_code == 400:
    #         # result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
        # else:
        #     result['message'] = response.status_code
    return render(request, 'oxford.html', {'search_result': result})

@login_required
def c_list(request):
     cands = CandidateInfo.objects.all()
     voter=VoterInfo.objects.get(user=request.user)
     return render(request, 'c_list.html', {'cands': cands,'voter':voter})
#
# def about(request):
#      cands = CandidateInfo.objects.all()
#      return render(request, 'about.html', {'cands': cands})
#
def home(request):
     return render(request, 'home.html', {})
