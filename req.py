import requests
from accounts.facebookapi import FacebookGraph
app_id = '482847369816069'
app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'

graph = FacebookGraph(app_id, app_secret, redirect_url)
graph.access_token = 'EAAG3Jan1aAUBAKD6IpmkEtZBktG6ZCCZAI3VTZBkMtIXqZAH1e4ZA3ZC9hJHJXQuZC8tWkZBZA4F62JGacTluJTH2hhehVNYm13IZAYrcPpV8yRg8pAv4tQBjO5qgOLXRG4qn0Gt14yZBigPy1TVImAKrzjZCpewJ8BE7wZAZCG3UyLV7fGU7erUH58z2LV'
# print(graph.get_user_profile_picture())
data={
    'access_token': 'EAAG3Jan1aAUBACbVhqDysctrD2vL71Ne6URvSkz0ai9TVdKEH0ASC57azt70KKEFA0ZCROfTtv92hJ5baywu0an6UEZAXEhT0jWaZADoxZA1DL1BDHHDYINMBXEEWvaRFrdeKFljjqQph8dBnybJF5ThZC2HjkuAmMkg3QWTXr41k7pmqZAjGH',
}
# print(graph.get_post_details('109139470485036_672280950837549'))
print(graph.get_scheduled_posts())