from django.contrib import messages
from django.http import response
from django.utils.html import escape
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic.base import View
import requests
from . import functions
from calendar import monthrange
from datetime import date, datetime, time
from requests.api import delete, post, request
from requests.sessions import Request
from .models import User
from .forms import RegisterForm
from .facebookapi import FacebookGraph
from .models import (
    UserProfile,
    FacebookApp,
    FacebookPage,
    AutomatePostCommentsResponse,
)


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    success_url = '/accounts/login'
    template_name = 'accounts/register.html'
    context_object_name = 'form'
    success_message = 'Your account created successfully!'


class DashboardView(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'
    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user = request.user) 
        except:
            profile = UserProfile.objects.create(user = request.user)
        
        # page = profile.facebookpage_set.first()
        # try:
        #     page_id = request.session['page_id']
        # except:
            # page_id = request.session.get('page_id', page.id)

        data = {'profile': profile, 'pages': profile.facebookpage_set.all()}
        return render(request, self.template_name,  data)

class FacebookLoginView(LoginRequiredMixin, View):
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user = request.user) 
        except:
            profile = UserProfile.objects.create(user = request.user)
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        
        try:
            profile.facebook_user_code = request.GET['code']
            info = graph.get_user_access_token(request.GET['code'])
            profile.facebook_user_access_token = info['access_token']
            profile.facebook_user_id = info['id']
            profile.facebook_user_name = graph.get_user_name()
            profile.pic_url = graph.get_user_profile_picture()
            profile.save()
            for key, value in graph.get_pages().items():
                try:
                    FacebookPage.objects.get(id = value['id'],)
                except:    
                    page = FacebookPage.objects.create(user_profile = profile, id = value['id'], access_token = value['access_token'], name = value['name'])
                    page.pic_url = graph.picture_url(value['id'], value['access_token'])
                    page.save()
            messages.success(request, 'You signed into facebook successfuly!')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        except:
            messages.success(request, 'Error signing to facebook, Please try again')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
                    
        # context = request.GET['code']
        # return render(request, 'accounts/facebook-info.html', {'data': context})

class FacebookProfileView(LoginRequiredMixin,View):
    template_name   = 'accounts/facebook-dashboard.html'
    no_pages        = 'accounts/no-pages.html'
    no_account      = 'accounts/no-account.html'
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user = request.user) 
        except:
            profile = UserProfile.objects.create(user = request.user)

        if profile.facebookpage_set.all().count() == 0: 
            if  not profile.facebook_user_id == None:
                return render(request, self.no_pages)
            else:
                return render(request, self.no_account)
        
        # try:
        #     print(request.GET['posts'])
        # except:
        #     print(None)
        page_id = functions.get_page_id(request, profile)
        if not page_id == '':
            graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
            page = request.user.userprofile.facebookpage_set.get(id = page_id)
            graph.access_token = page.access_token
            pic_url = graph.picture_url(page.id, page.access_token)
            posts = graph.get_posts()
            request.session['next_paging'] = ''
            request.session['next_paging'] = graph.next_paging
            # print(request.session['next_paging'])
            return render(request, self.template_name, {'profile': profile, 'pages': profile.facebookpage_set.all(), 'page_id': page_id, 'posts': posts, 'page': page, 'pic_url': pic_url, 'next': request.session['next_paging'] if request.session['next_paging'] != None else False})
        return render(request, self.template_name, {'profile': profile})

class FacebookMorePosts(View):
    template_name = 'accounts/posts.html'
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, *args, **kwargs):
        url = request.session['next_paging']
        if url == '':
            profile = UserProfile.objects.get(user = request.user) 
            page_id = functions.get_page_id(request, profile)
            page = request.user.userprofile.facebookpage_set.get(id = page_id)
            graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
            graph.access_token = page.access_token
            posts = graph.get_posts()
            request.session['next_paging'] = graph.next_paging
            return render(request, self.template_name, {'posts': posts})

        if url != None:
            req = requests.get(url)
            data = req.json()['data']
            for post in data:
                post['created_time'] = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z") 
            try:
                request.session['next_paging'] = req.json()['paging']['next']
            except:
                request.session['next_paging'] = None
            return render(request, self.template_name, {'posts': data})
        else:
            return HttpResponse('None')

class FacebookSearchPostsView(View):
    template_name = 'accounts/post.html'
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, post_id, *args, **kwargs):
        request.session['next_paging'] = ''
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        profile = UserProfile.objects.get(user = request.user) 
        page_id = functions.get_page_id(request, profile)
        if not page_id == '':
            page = request.user.userprofile.facebookpage_set.get(id = page_id)
            graph.access_token = page.access_token
            post_id = page_id + '_' + post_id
            try:
                post = graph.get_post_details(post_id)
                scheduled = str(datetime.now()) < str(post['created_time'])
                # print(str(datetime(2021, 8, 28, 1, 56, 0)) > str(post['created_time']))
                return render(request, self.template_name, {'post': post, 'scheduled': scheduled})
            except:
                return HttpResponse("noResults")
        return HttpResponse("pageError")


class FacebookScheduledPostsView(View):
    posts_template_name = 'accounts/posts.html'
    post_template_name = 'accounts/post.html'
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    def get(self, request, *args, **kwargs):
        request.session['next_paging'] = ''
        profile = UserProfile.objects.get(user = request.user) 
        page_id = functions.get_page_id(request, profile)
        page = request.user.userprofile.facebookpage_set.get(id = page_id)
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        graph.access_token = page.access_token
        posts = graph.get_scheduled_posts()
        if len(posts) == 0: 
            return HttpResponse('None')
        return render(request, self.posts_template_name if len(posts) > 1 else self.post_template_name, {'posts': posts} if len(posts) > 1 else {'post': posts})


class FacebookLifeTimePostsView(View):
    posts_template_name = 'accounts/posts.html'
    post_template_name = 'accounts/post.html'
    def get(self, request, lifetime, *args, **kwargs):
        request.session['next_paging'] = ''
        profile = UserProfile.objects.get(user = request.user)
        page_id = functions.get_page_id(request, profile)
        page = request.user.userprofile.facebookpage_set.get(id = page_id)
        graph = functions.app()
        graph.access_token = page.access_token        
        date = functions.posts_filter(lifetime)
        if date != None:
            posts = graph.get_posts(since=date)
            if len(posts) > 0:
                return render(request, self.posts_template_name if len(posts) > 1 else self.post_template_name, {"posts": posts} if len(posts) > 1 else {'post': posts})
            else:
                return HttpResponse('noPosts')
        else:
            return HttpResponseRedirect(reverse('accounts:facebook-more-posts'))

class FacebookPublishedPostsView(View):
    def get(self, request, *args, **kwargs):
        request.session['next_paging'] = ''
        return HttpResponseRedirect(reverse('accounts:facebook-more-posts'))


class AddPost(View):
    template_name = 'accounts/add_post.html'
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'pages': request.user.userprofile.facebookpage_set.all()})

    def post(self, request, *args, **kwargs):
        page = FacebookPage.objects.get(id = request.POST['page_id'])
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        post_id = graph.add_post(page.id ,request.POST['message'], page.access_token)['id']
        messages.success(request, 'Post add successfuly with id %s' % post_id)
        return HttpResponseRedirect(reverse('accounts:facebook-profile'))


class AutomatePostCommentsResponseView(View):
    template_name = 'accounts/automate_post_comments_response.html'
    def get(self, request, post_id, *args, **kwargs):
        page = request.user.userprofile.facebookpage_set.get(id = post_id.split('_')[0])
        p_id = post_id.split('_')[1]
        graph = functions.app()
        graph.access_token = page.access_token
        post = graph.get_post_details(post_id)
        pic_url = graph.picture_url(page.id, page.access_token)
        replies = page.automatepostcommentsresponse_set.filter(post = p_id)
        return render(request, self.template_name, {'post': post, 'page': page, 'pic_url':pic_url, 'replies': replies})
    # def post(self, request, *args, **kwargs):
    #     page = request.user.userprofile.facebookpage_set.get(id = request.POST['post_id'].split('_')[0])
    #     post_id = request.POST['post_id'].split('_')[1]
    #     try:
    #         post = AutomatePostCommentsResponse.objects.get(post = post_id)
    #         messages.success(request, 'An automation for this post is already exist')
    #         return HttpResponseRedirect(reverse('accounts:facebook-profile'))
    #     except:
    #         post = AutomatePostCommentsResponse.objects.create(page = page, post = post_id, response = request.POST['response'],response_privetly = request.POST['response_privetly'], name = request.POST['automation'])
    #         messages.success(request, 'Automation added successfully')
    #         return HttpResponseRedirect(reverse('accounts:facebook-profile'))


class ReplyView(View):
    template_name = 'accounts/add_reply.html'
    def get(self, request, *args, **kwargs):
        reply_id = request.GET['reply_id']
        AutomatePostCommentsResponse.objects.get(id = reply_id).delete()
        return HttpResponse('done')
    def post(self, request, *args, **kwargs):
        page = request.user.userprofile.facebookpage_set.get(id = request.POST['post_id'].split('_')[0])
        post = request.POST['post_id'].split('_')[1]
        words = request.POST['words'].split(' ')
        reply = request.POST['reply']
        private_reply = request.POST['private_reply']
        res = AutomatePostCommentsResponse.objects.create(page = page, post = post, words = words, response = reply, private_response = private_reply)
        return render(request, self.template_name, {'id':res.id, 'words': words, 'reply': reply, 'private_reply': private_reply})