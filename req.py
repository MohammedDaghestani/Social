import requests
from accounts.facebookapi import FacebookGraph
app_id = '482847369816069'
app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'

graph = FacebookGraph(app_id, app_secret, redirect_url)
graph.access_token = 'EAAG3Jan1aAUBAOjZBTPxCnoQzyOt6WZB8FBEY0HZA2gsGZChQemGmIQdsbOmlo5gD9wnVfrDJSalu1ryozzwZA6yKoCF4MrSWAZCWxYJnnFHwxodxfLqjOFcFcW2ZBKtbQP6hKpFzWUzU3KcNKXfuLezGIyEUyOPFzssHbtSwZBoLKAY6KJOvYQv'
# print(graph.get_user_profile_picture())
    # data={
    #     'access_token': 'EAAG3Jan1aAUBACbVhqDysctrD2vL71Ne6URvSkz0ai9TVdKEH0ASC57azt70KKEFA0ZCROfTtv92hJ5baywu0an6UEZAXEhT0jWaZADoxZA1DL1BDHHDYINMBXEEWvaRFrdeKFljjqQph8dBnybJF5ThZC2HjkuAmMkg3QWTXr41k7pmqZAjGH',
    # }
# print(graph.get_post_details('109139470485036_672280950837549'))
print(graph.check_reply_if_exist('134150406795176', '1732150443661823_1732172883659579'))