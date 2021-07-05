# from django.shortcuts import render
from webhooks.models import Webhooks
from django.views import View
from django.http import HttpResponse
#Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from accounts.facebookapi import FacebookGraph
from accounts.models import FacebookPage



verify_token = 'mhd'
@method_decorator(csrf_exempt, name='dispatch')
class TestView(View):
    app_id = '482847369816069'
    app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
    redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, *args, **kwargs):
        # return HttpResponse("test")
        print(request.GET['hub.challenge'])
        if request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    # @csrf_exempt()
    def post(self, request):
        Webhooks.objects.create(data = json.loads(request.body))
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        data = graph.analyze_request(request)
        # page_id = json.loads(request.body)['entry'][0]['id']
        # sender = json.loads(request.body)['entry'][0]['changes'][0]['value']['from']['id']
        if data.ITEM.value == 'comment':
            if data.PAGE_ID.value == data.SENDER.value:
                return HttpResponse('This comment is from page')
            # comment_id = json.loads(request.body)['entry'][0]['changes'][0]['value']['comment_id']
            # post_id = json.loads(request.body)['entry'][0]['changes'][0]['value']['comment_id'].split('_')[0]
            page = FacebookPageAccessToken.objects.get(page_id = data.PAGE_ID.value)
            try:
                automation = page.automatepostcommentsresponse_set.get(post = data.POST_ID.value)
                graph.reply_comments(True, data.SENDER.value, data.COMMENT_ID.value, automation.response, page.page_access_token)
                if automation.response_privetly != '':
                    graph.reply_comments_privetly(data.PAGE_ID.value, data.SENDER.value, data.COMMENT_ID.value, automation.response_privetly, page.page_access_token)
                return HttpResponse('Reply success')
            except:
                return HttpResponse('Reply error')
        return HttpResponse('Not comment')



