from django.views.decorators.csrf import csrf_exempt
from efficient_apriori import apriori
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
# Create your views here.
from MySQL_procedures_conncetion_python.Connection import get_all_business_count, get_all_category_count, get_top_10_categories, \
    get_filtered_users, get_filtered_reviews, get_filtered_businesses, get_review_distribution, \
    get_businesses_with_highest_ratings, get_business_categories_with_highest_ratings, get_businesses_five_stars, \
    get_business_name_from_ids
from login_register.models import users
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
import random
import string

def step1(request):
    if 'userid' in request.session:
        user_object = users.objects.get(pk=request.session['userid'])
        args = {'user_object': user_object, 'logged_in': 1}
        return render(request,'analysis/step-1.html',args)
    else:
        return HttpResponseRedirect('/login_register/login_page')


def step2(request):
    if 'userid' in request.session:
        user_object = users.objects.get(pk=request.session['userid'])
        args = {'user_object': user_object, 'logged_in': 1,
                'no_of_businesses': get_all_business_count(),
                'no_of_categories': get_all_category_count(),
                'business_category': get_top_10_categories(),
                'min_ratings_range' : ['1000', '1250', '1500', '1750', '2000', '2500',
                                       '3000', '3500'],
                'business_ratings_range' : [1, 2, 3, 4, 5]
                }
        return render(request, 'analysis/step-2.html', args)
    else:
        return HttpResponseRedirect('/login_register/login_page')


def visualization(request):
    return None


def generate_dataframe(filtered_businesses, filtered_users, filtered_reviews):
    final_categories = []
    user_ids = set(filtered_users)
    print(len(filtered_reviews))
    for review_data in filtered_reviews:
        if review_data[0] in user_ids:
            category = [x.strip() for x in filtered_businesses[review_data[1]].split(',')]
            final_categories.append(category)
    #df = pd.DataFrame(final_categories)
    #df.fillna(value=pd.np.nan, inplace=True)
    te = TransactionEncoder()
    te_ary = te.fit(final_categories).transform(final_categories)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df


def perform_apriori(final_df):
    records = []
    for i in range(final_df.shape[0]):
        records.append([str(final_df.values[i, j]) for j in range(final_df.shape[1])])
    association_rules = apriori(records, min_support=0.005, min_confidence=0.2, min_length=2)
    association_results = list(association_rules)
    return association_results


def filter_data(request):
    if 'userid' in request.session:
        if request.method == 'POST':
            business = request.POST.get('category')
            stars = request.POST.get('business_ratings')
            startdate = request.POST.get('startdate')
            enddate = request.POST.get('enddate')
            minratings = request.POST.get('min_ratings')

        filtered_users = get_filtered_users(minratings)
        filtered_reviews = get_filtered_reviews(stars,business)
        filtered_businesses = get_filtered_businesses(business)
        final_df = generate_dataframe(filtered_businesses,filtered_users,filtered_reviews)
        frequent_itemsets = apriori(final_df, min_support=0.1, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets = frequent_itemsets.sort_values(['length','support'], ascending=False)

        #frequent_itemsets
        #print(final_df.shape)
        #itemsets, rules = apriori(final_df, min_support=0.1,  min_confidence=0.9)
        #print(rules)

        most_frequent_itemset = list(frequent_itemsets['itemsets'].iloc[0])
        supp = frequent_itemsets['support'].iloc[0]
        for i in range(len(frequent_itemsets)):
            frequent_itemsets['itemsets'].iloc[i] = list(frequent_itemsets['itemsets'].iloc[i])
        print(frequent_itemsets)
        user_object = users.objects.get(pk=request.session['userid'])
        args = {'user_object': user_object, 'logged_in': 1, 'category': business,
                'stars': stars, 'startdate': startdate,'enddate': enddate,
                'minratings':minratings ,
                'associations' : frequent_itemsets,
                'most_frequent_itemset' : most_frequent_itemset,
                'supp' :supp
                }

        return render(request, 'analysis/apriori.html', args)
    else:
        return HttpResponseRedirect('/login_register/login_page')

@csrf_exempt
def rating_dist(request):
    args = {'data': 'hello', 'post' : 0,'image':''}
    if request.method == 'POST':
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        stars, count = get_review_distribution()
        plt.figure(figsize=(8, 5))
        plt.bar(stars, count)
        plt.xlabel('Stars')
        plt.ylabel('Count')
        plt.title('Stars Distribution in Review Table')
        plt.savefig('/home/harshit/Yelp_Analysis/yelp_analysis/media/'+image_name+'.png')
        args['post'] = 1
        args['image'] = image_name
    return render(request, 'analysis/result.html', args)

@csrf_exempt
def top_businesses(request, category):
    args = {'data': 'hello', 'post': 0, 'image': ''}
    if request.method == 'POST':
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        businesses, reviews = get_businesses_with_highest_ratings(category)
        plt.figure(figsize=(12, 10))
        plt.bar(businesses, reviews)
        plt.xlabel('Businesses')
        plt.ylabel('Number of reviews received')
        plt.title('Top '+str(category)+ ' businesses with highest reviews')
        plt.xticks(rotation=20)
        plt.savefig('/home/harshit/Yelp_Analysis/yelp_analysis/media/' + image_name + '.png')
        args['post'] = 1
        args['image'] = image_name
    return render(request, 'analysis/result.html', args)

@csrf_exempt
def top_business_categories(request, category):
    args = {'data': 'hello', 'post': 0, 'image': ''}
    if request.method == 'POST':
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        categories, reviews = get_business_categories_with_highest_ratings(category)
        plt.figure(figsize=(8, 8))
        plt.bar(categories, reviews)
        plt.xlabel('Business Categories')
        plt.ylabel('Number of Businesses')
        plt.title('Top '+str(category)+ ' business categories')
        plt.savefig('/home/harshit/Yelp_Analysis/yelp_analysis/media/' + image_name + '.png')
        args['post'] = 1
        args['image'] = image_name
    return render(request, 'analysis/result.html', args)

@csrf_exempt
def five_star_businesses(request, category):
    print('here I am')
    args = {'data': 'hello', 'post': 0, 'image': ''}
    if request.method == 'POST':
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        businesses = []
        business_ids, reviews = get_businesses_five_stars(category)
        for id in business_ids:
            print(id, get_business_name_from_ids(id))
            if id == None:
                businesses.append('No Name')
            else:
                businesses.append(get_business_name_from_ids(id))
        plt.figure(figsize=(8, 8))
        plt.bar(businesses, reviews)
        plt.xlabel('Businesses')
        plt.ylabel('Number of Five star reviews received')
        plt.title('Top '+str(category)+ ' businesses with highest five stars reviews')
        plt.savefig('/home/harshit/Yelp_Analysis/yelp_analysis/media/' + image_name + '.png')
        args['post'] = 1
        args['image'] = image_name
    return render(request, 'analysis/result.html', args)
