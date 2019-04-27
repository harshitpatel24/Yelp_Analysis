from django.shortcuts import render

# Create your views here.
from MySQL_procedures_conncetion_python.Connection import get_columns, get_data
from login_register.models import users


def homepage(request):
    db_name = 'project2'
    business_columns = get_columns(db_name, 'business')
    user_columns = get_columns(db_name, 'user')
    review_columns = get_columns(db_name, 'review')
    check_in_columns = get_columns(db_name, 'checkin')
    tip_columns = get_columns(db_name, 'tip')

    business_data = get_data('business')
    user_data = get_data('user')
    review_data = get_data('review')
    check_in_data = get_data('checkin')
    tip_data = get_data('tip')

    if 'userid' in request.session:
        user_object = users.objects.get(pk=request.session['userid'])

        args = {'user_object': user_object,
                'logged_in': 1,
                'business_columns': business_columns,
                'user_columns': user_columns,
                'review_columns': review_columns,
                'check_in_columns': check_in_columns,
                'tip_columns': tip_columns,
                'business_data': business_data,
                'user_data' : user_data,
                'review_data' : review_data,
                'check_in_data' : check_in_data,
                'tip_data' : tip_data
                }
    else:
        args = {'logged_in': 0,
                'business_columns': business_columns,
                'user_columns': user_columns,
                'review_columns': review_columns,
                'check_in_columns': check_in_columns,
                'tip_columns': tip_columns,
                'business_data': business_data,
                'user_data' : user_data,
                'review_data' : review_data,
                'check_in_data' : check_in_data,
                'tip_data' : tip_data
                }
    return render(request, 'home/homepage.html', args)
