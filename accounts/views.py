from django.contrib import messages
from django.contrib.messages import views
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic.base import View
from requests.api import request
from .models import User
from .forms import RegisterForm
from .facebookapi import FacebookGraph
from .models import (
    UserProfile,
    FacebookApp,
    FacebookPage,

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
        # if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user = request.user) 
        except:
            profile = UserProfile.objects.create(user = request.user)
        
        page = profile.facebookpage_set.first()
        try:
            page_id = request.session['page_id']
        except:
            page_id = request.session.get('page_id', page.id)

        # if not id:
        # else: page_id = id
        # print(page_id)
        data = {'profile': profile, 'pages': profile.facebookpage_set.all(), 'page_id': page_id}
        # data = {'profile': profile,}
        return render(request, self.template_name,  data)
        # return render(request, 'accounts/login.html')

class FacebookLoginView(View):
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
        if request.user.is_authenticated:
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
                        FacebookPage.objects.get(page_id = value['id'],)
                    except:    
                        page = FacebookPage.objects.create(user_profile = profile, id = value['id'], access_token = value['access_token'], name = value['name'])
                        page.pic_url = graph.picture_url(value['id'], value['access_token'])
                        page.save()
                messages.success(request, 'You signed into facebook successfuly!')
                return HttpResponseRedirect(reverse('accounts:dashboard'))
            except:
                messages.success(request, 'Error signing to facebook, Please try again')
                return HttpResponseRedirect(reverse('accounts:dashboard'))
                    
        context = request.GET['code']
        return render(request, 'accounts/facebook-info.html', {'data': context})

class FacebookProfileView(LoginRequiredMixin,View):
    template_name = 'accounts/facebook-dashboard.html'
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
        # request.session.get('page_id', pk)
        # print(request.session())
        try:
            page_id = request.session['page_id']
        except:
            page = profile.facebookpage_set.first()
            page_id = page.id
            request.session['page_id'] = page_id


        print(page_id)
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        page = request.user.userprofile.facebookpage_set.get(id = page_id)
        graph.access_token = page.access_token
        # data = {
        #     'posts': graph.graph_api('posts')['posts']['data']
        # }
        # return render(request, self.template_name, {'profile': profile, 'pages': profile.facebookpageaccesstoken_set.all(), 'page_id': page_id, 'posts': graph.graph_api('posts')['posts']['data'], 'page': page})
        return render(request, self.template_name, {'profile': profile, 'pages': profile.facebookpage_set.all(), 'page_id': page_id, 'posts': graph.get_posts(), 'page': page})

        
    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user = request.user)
        page_id = request.POST['page_id']
        request.session['page_id'] = page_id
        graph = FacebookGraph(self.app_id, self.app_secret, self.redirect_url)
        page = request.user.userprofile.facebookpage_set.get(id = page_id)
        graph.access_token = page.access_token
        return render(request, self.template_name, {'profile': profile, 'pages': profile.facebookpage_set.all(), 'page_id': page_id, 'posts': graph.get_posts(), 'page': page})


# class RemoveProfileView(View):
#     def get(self, request, *args, **kwargs):
#         UserProfile.objects.get(user = request.user).delete()
#         return HttpResponseRedirect(reverse('accounts:profile'))

# class ReconnectFacebookView(View):
#     def get(self, request, *args, **kwargs):
#         UserProfile.objects.get(user = request.user).delete()
#         return HttpResponseRedirect('https://graph.facebook.com/oauth/authorize?client_id=482847369816069&redirect_uri=https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/&scope=email,pages_manage_metadata,pages_manage_posts,pages_read_engagement,pages_read_user_content,pages_show_list,public_profile,pages_manage_engagement,pages_messaging')
