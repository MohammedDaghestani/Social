from accounts.facebookapi import FacebookGraph
app_id = '482847369816069'
app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'

graph = FacebookGraph(app_id, app_secret, redirect_url)
graph.access_token = 'EAAG3Jan1aAUBAHYc2HZCMHXzh8yvR0PQ1GvQlIoHi2u9ZA5Y1TOYBuEwt80NBZA9EEfp1ZBFGSWDzwC7bLF2TzOfEPyTZAA0Lf2MLZCS6DHwZAFcNxg1uHqsYgZBpZA9303Ui8vfqKyvbwug6iubf3oYycoGzaJ0ofCQtHRfsPN6IyVpRX3v5ZBF0x'
print(graph.get_user_profile_picture())