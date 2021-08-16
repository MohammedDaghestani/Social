from webhooks.models import Webhooks, Insights
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from accounts.models import FacebookPage
from accounts import functions
import random


verify_token = 'mhd'
@method_decorator(csrf_exempt, name='dispatch')
class TestView(View):
    def get(self, request, *args, **kwargs):
        if request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    # @csrf_exempt()
    def post(self, request):
        Webhooks.objects.create(data = json.loads(request.body), headers = request.headers, body = request.body)
        graph = functions.app() 
        data = graph.analyze_request(request)

        # If the action is comment  
        if data.ITEM.value == 'comment' and data.VERB.value == 'add':
            if data.PAGE_ID.value == data.SENDER.value:
                return HttpResponse('This comment is from page')
            comments = Insights.objects.all()
            if len(comments) == 0:
                Insights.objects.create(comments = 1, data = json.loads(request.body))
            else:
                Insights.objects.create(comments = Insights.objects.last().comments + 1, data = json.loads(request.body))
            page = FacebookPage.objects.get(id = data.PAGE_ID.value)

            # Check if there any replies to this post  
            try:
                replies = page.automatedresponses_set.filter(post = data.POST_ID.value)
            except:
                replies = None
            if replies != None:
                rep_with_words = '' # reply id for the matched reply
                reps_without_words = [] # replies that don't have a specific words
                for reply in replies:
                    if len(reply.words) != 0 and reply.words[0] !='':
                        for word in reply.words:
                            if data.MESSAGE.value.find(word) != -1:
                                rep_with_words = reply.id
                                break
                    else:
                        reps_without_words.append(reply.id)
                # Comments that don't have message it should contain stickers
                if data.MESSAGE.value != None:
                    if rep_with_words != '':
                        reply = page.automatedresponses_set.get(id = rep_with_words) 
                    elif len(reps_without_words) != 0:
                        reply = page.automatedresponses_set.get(id = reps_without_words[random.randrange(len(reps_without_words))])
                else:
                    if len(reps_without_words) != 0:
                        reply = page.automatedresponses_set.get(id = reps_without_words[random.randrange(len(reps_without_words))])
                try:    
                    graph.reply_comments(True, data.SENDER.value, data.COMMENT_ID.value, reply.response, page.access_token)
                    if reply.private_response:
                        graph.reply_comments_privetly(data.PAGE_ID.value, data.SENDER.value, data.COMMENT_ID.value, reply.private_reponse, page.access_token)
                    return HttpResponse('success')
                except:
                    return HttpResponse('error')
            else:
                return HttpResponse('noReplies')
                
        # When remove the post delete it's replies from the site
        elif data.ITEM.value == 'post' and data.VERB.value == 'remove':
            print(data.POST_ID.value)
            page = FacebookPage.objects.get(id = data.PAGE_ID.value)
            page.automatedresponses_set.filter(post = data.POST_ID.value).delete()
            return HttpResponse('Delete replies success')



