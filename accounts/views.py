from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic.base import View
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


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user = request.user) 
        except:
            profile = UserProfile.objects.create(user = request.user)
        
        # page = profile.facebookpageaccesstoken_set.first()
        # try:
        #     page_id = request.session['page_id']
        # except:
        #     page_id = request.session.get('page_id', page.page_id)

        # if not id:
        # else: page_id = id
        # print(page_id)
        # data = {'profile': profile, 'pages': profile.facebookpageaccesstoken_set.all(), 'page_id': page_id}
        data = {'profile': profile,}
        return render(request, self.template_name,  data)
        # return render(request, 'accounts/login.html')

class FacebookLoginView(View):
    app = FacebookApp.objects.first()
    app_id = app.app_id
    app_secret = app.app_secret
    redirect_url = app.redirect_url
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
                return HttpResponseRedirect(reverse('accounts:profile'))
            except:
                messages.success(request, 'Error signing to facebook, Please try again')
                return HttpResponseRedirect(reverse('accounts:profile'))
                    
        context = request.GET['code']
        return render(request, 'accounts/facebook-info.html', {'data': context})
