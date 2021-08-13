import datetime, time
from calendar import monthrange

from requests.sessions import session
from .facebookapi import FacebookGraph
from .models import FacebookApp
def return_unix_date_last(filter, date = datetime.datetime.now()):
    this_year = date.year
    this_month = date.month
    this_day = date.day
    past_year = this_year if this_month != 1 else this_year - 1
    past_month = this_month - 1 if this_month != 1 else 12
    if filter == 'today':
        return int(time.mktime(datetime.datetime(this_year, this_month, this_day).timetuple()))
    elif filter == 'thisMonth':
        return int(time.mktime(datetime.datetime(this_year, this_month, 1).timetuple()))
    elif filter == 'thisYear':
        return int(time.mktime(datetime.datetime(this_year, 1, 1).timetuple()))
    else:
        if this_day > filter:
            return int(time.mktime(datetime.datetime(this_year, this_month, this_day - filter).timetuple()))   
        else:
            return int(time.mktime(datetime.datetime(past_year, past_month, (this_day + monthrange(this_year, past_month)[1]) - filter).timetuple()))   


def posts_filter(since):
    if since == 'last7':
        return return_unix_date_last(7)
    elif since == 'last14':
        return return_unix_date_last(14)
    elif since == 'last28':
        return return_unix_date_last(28)
    elif since == 'yesterday':
        return return_unix_date_last(1)
    elif since == 'lifetime':
        return None
    else:
        return return_unix_date_last(since)


def get_page_id(request, profile):
    try:
        page_id = request.COOKIES['page_id']
    except:
        try:
            page = profile.facebookpage_set.first()
            page_id = page.id
        except:
            page_id = ''
    return page_id


def app():
    try:
        app = FacebookApp.objects.first()
        app_id = app.app_id
        app_secret = app.app_secret
        redirect_url = app.redirect_url
    except:
        app_id = '482847369816069'
        app_secret = '11b994aa0b08dabbcb04c3b2ade775e7'
        redirect_url = 'https://mhddaghestani.pythonanywhere.com/accounts/facebook-login/'
    return FacebookGraph(app_id, app_secret, redirect_url) 
