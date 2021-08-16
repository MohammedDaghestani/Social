from datetime import datetime
import requests
# from requests.api import post
import json
import enum
class FacebookGraph:
    graph_url           = 'https://graph.facebook.com/'
    facebook_auth_url = 'https://graph.facebook.com/oauth/authorize'
    facebook_get_access_token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_url = None
    app_id = None
    app_secret = None
    access_token = None
    error = None
    user_id = None
    next_paging= None
    def __init__(self, app_id, app_secret, redirect_url):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_url = redirect_url


    def get_user_access_token(self, code):
        data = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'redirect_uri': self.redirect_url,
            'code' : code
        }
        req = requests.get(self.facebook_get_access_token_url, data)
        response = req.json()
        # items = response['data']
        try:
            self.access_token = response['access_token']
            self.user_id = self.get_user_id()
        except:
            self.error = response['error']
        return {'access_token':self.access_token, 'id': self.user_id} if self.access_token != None else self.error


    def get_user_id(self):
        data = {
            'access_token': self.access_token
        }
        req = requests.get(self.graph_url + 'me', data)
        return req.json()['id']

    def get_user_name(self):
        data = {
            'fields': 'name',
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + 'me', data)
        return req.json()['name']

    def get_user_profile_picture(self):
        data = {
            'height': 150,
            'width': 150,
            'redirect': 0,
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + 'me/picture', data)
        return req.json()['data']['url']

        
    def graph_api(self, fields = 'id,name'):
        data = {
            'fields': fields,
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + 'me', data)
        return req.json()

    def get_pages(self):
        data = {
            'fields': 'accounts',
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + 'me', data)
        data_out = {}
        for page in req.json()['accounts']['data']:
            data_out[page['name']] = {
                'name': page['name'],
                'id': page['id'],
                'access_token': page['access_token'],
            }

        return data_out

    def add_post(self, page_id, message, page_access_token):
        data = {
            'message': message,
            'access_token': page_access_token,
        }
        req = requests.post(self.graph_url + 'me/feed', data)
        return req.json()

        
    def reply_comments(self,add_like, sender, comment_id, message, access_token):
        data = {
            'message': '@[{0}] {1}'.format(sender, message),#'@[%s] ' % sender + message,
            'access_token': access_token,
        }
        req = requests.post(self.graph_url + comment_id + '/comments', data)
        if add_like:
            requests.post(self.graph_url + comment_id + '/likes', {'access_token': access_token})
        return req.json()
    
    def reply_comments_privetly(self, page_id, sender, comment_id, message, page_access_token):
        data = {
            'recipient': {'comment_id': comment_id},
            'message': {'text': message},
            'message_type': 'RESPONSE',
            'access_token': page_access_token,
        }
        req = requests.post(self.graph_url + page_id + '/messages', json=data)
        return req.json()

    def analyze_request(self, request):
        req = json.loads(request.body)
        class RequestData(enum.Enum):
            PAGE_ID     = req['entry'][0]['id']
            ITEM        = req['entry'][0]['changes'][0]['value']['item']
            VERB        = req['entry'][0]['changes'][0]['value']['verb']
            if ITEM == 'comment':
                SENDER      = req['entry'][0]['changes'][0]['value']['from']['id']
                POST_ID     = req['entry'][0]['changes'][0]['value']['post_id'].split('_')[1]
                COMMENT_ID  = req['entry'][0]['changes'][0]['value']['comment_id']
                PARENT_ID   = req['entry'][0]['changes'][0]['value']['parent_id']
                try:
                    MESSAGE = req['entry'][0]['changes'][0]['value']['message']
                except:
                    MESSAGE = None
            if ITEM == 'post':
                POST_ID     = req['entry'][0]['changes'][0]['value']['post_id'].split('_')[1]

        return RequestData

    def picture_url(self, page_id, page_access_token):
        data = {
            'height': 150,
            'width': 150,
            'redirect': 0,
            'access_token': page_access_token,
        }
        req = requests.get(self.graph_url + page_id + '/picture', data)
        return req.json()['data']['url']


    def get_posts(self, limit=10, since=0):
        if since == 0:
            data = {
                'fields': 'id,message,created_time,full_picture,permalink_url',
                'limit': limit,
                'access_token': self.access_token,
            }
            req = requests.get(self.graph_url + 'me/posts', data)
            try:
                self.next_paging = req.json()['paging']['next']
            except:
                self.next_paging = None
            res = req.json()['data']
        else:
            data = {
                'fields': 'id,message,created_time,full_picture,permalink_url',
                'since': since,
                'access_token': self.access_token,
            }
            # res = {}
            req = requests.get(self.graph_url + 'me/posts', data)
            res = req.json()['data']
            try:
                nxt = req.json()['paging']['next']
            except:
                nxt = None
            while(nxt != None):
                r = requests.get(nxt)
                res.extend(r.json()['data'])
                try: 
                    nxt = r.json()['paging']['next']
                except:
                    break
        for post in res:
            # print(post, end='\n')
            post['created_time'] = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z")
        return res


    def get_scheduled_posts(self):
        data = {
            'fields': 'id,message,created_time,full_picture,permalink_url',
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + 'me/scheduled_posts', data)
        res = req.json()['data']
        for post in res:
            post['created_time'] = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z")
        return res


    def get_post_details(self, post_id):
        data = {
            'fields': 'id,message,created_time,full_picture,permalink_url,admin_creator',
            'access_token': self.access_token,
        }
        req = requests.get(self.graph_url + post_id, data)
        res = req.json() 
        res['created_time'] = datetime.strptime(req.json()['created_time'], "%Y-%m-%dT%H:%M:%S%z") 
        return res
        
    def check_reply_if_exist(self, page_id, post_id):
        req = requests.get(self.graph_url + page_id + '_' +  post_id + '/comments')
        for reply in req.json():
            if reply['from']['id'] == page_id:
                return True
        return False