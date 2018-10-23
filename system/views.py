from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Shops, Review, Activity, Poll, Choice, Vote
from .forms import ReviewForm, UserCreateForm
# for render_to_response
from django.shortcuts import render_to_response
from django.views import generic

# For login in user
from django.contrib.auth import login, logout
# login and registration form creation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.contenttypes.models import ContentType

from datetime import datetime, timedelta, timezone
from django.urls import reverse
from django.http import JsonResponse
import pytz

import json
#from django.core import serializers

# Create your views here.
def blank(request):
    shops = None
    json_shops = json.dumps(shops)
    if request.method == 'GET':
        search_text = request.GET.get('search')
        #print("Search Text: " + str(search_text) )
        if search_text != None:
            sort_by = request.GET.get('sort_by')
            shops = Shops.objects.filter(company_name__contains=search_text).order_by("company_name").values_list('pk', flat=True)
            search_count = Shops.objects.filter(company_name__contains=search_text).order_by("company_name").count();
            shops = list(shops)
            json_shops = json.dumps(shops)
            #print( "Shops from home" + str(shops) )
            #serialized_shops = serializers.serialize('json', shops)
        else:
            search_text = "";
            search_count = 0;
    else:
        search_text = "";
        search_count = 0;


    # some data we might wanna pass over
    form = AuthenticationForm()
    #else redirect to login page
    if request.user.is_authenticated:
        user = request.user
        activity = Activity.objects.filter(user=user)
        context = {'form': form, 'activity':activity, 'shops': json_shops, "search_text": search_text, "search_count": search_count }
    else:
        context = {'form': form, 'shops': json_shops, "search_text": search_text, "search_count": search_count  }
    # context = {
    #     'username': request.user.get_username,
    #     'all_reports': Shops.objects.all()
    # }

    return render(request, 'system/index.html', context)
    #return redirect('system:home')
    #return HttpResponse('Hello World')

def userfavourite (request):
    # some data we might wanna pass over
    form = AuthenticationForm()
    #else redirect to login page
    if request.user.is_authenticated:
        user = request.user
        activity = Activity.objects.filter(user=user)
        context = {'form': form, 'activity':activity  }
    else:
        context = {'form': form }
        return redirect('system:login_user')
    # context = {
    #     'username': request.user.get_username,
    #     'all_reports': Shops.objects.all()
    # }

    return render(request, 'system/favourite.html', context)

def home(request):

    shops = None
    json_shops = json.dumps(shops)
    if request.method == 'GET':
        search_text = request.GET.get('search')
        #print("Search Text: " + str(search_text) )
        if search_text != None:
            sort_by = request.GET.get('sort_by')
            shops = Shops.objects.filter(company_name__contains=search_text).order_by("company_name").values_list('pk', flat=True)
            search_count = Shops.objects.filter(company_name__contains=search_text).order_by("company_name").count();
            shops = list(shops)
            json_shops = json.dumps(shops)
            #print( "Shops from home" + str(shops) )
            #serialized_shops = serializers.serialize('json', shops)
        else:
            search_text = "";
            search_count = 0;
    else:
        search_text = "";
        search_count = 0;


    # some data we might wanna pass over
    form = AuthenticationForm()
    #else redirect to login page
    if request.user.is_authenticated:
        user = request.user
        activity = Activity.objects.filter(user=user)
        context = {'form': form, 'activity':activity, 'shops': json_shops, "search_text": search_text, "search_count": search_count }
    else:
        context = {'form': form, 'shops': json_shops, "search_text": search_text, "search_count": search_count  }
    # context = {
    #     'username': request.user.get_username,
    #     'all_reports': Shops.objects.all()
    # }

    return render(request, 'system/home.html', context)

def createpoll(request):
    # some data we might wanna pass over
    form = AuthenticationForm()
    #else redirect to login page
    if request.user.is_authenticated:
        user = request.user
        activity = Activity.objects.filter(user=user)
        context = {'form': form, 'activity':activity }
    else:
        context = {'form': form }
        return redirect('system:login_user')
    # context = {
    #     'username': request.user.get_username,
    #     'all_reports': Shops.objects.all()
    # }

    return render(request, 'system/createpoll.html', context)

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('system:home')
        #return redirect('system:login_user')

def register(request):
    if request.user.is_authenticated:
        return redirect('system:home')
    form = AuthenticationForm()
    if request.method == 'POST':
        form_register = UserCreateForm(request.POST)
        if form_register.is_valid():
            form_register.save()
            return redirect('system:home')
    else:
        # Note: UserCreateForm is Used that is defined in form.py
        form_register = UserCreateForm()

    template_name = 'system/register.html'
    return render(request, template_name, {'form_register': form_register, 'form': form } )

def login_user(request):
    if request.user.is_authenticated:
        return redirect('system:home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log user in
            user = form.get_user()
            login(request, user)
            return redirect('system:home')
    else:
        form = AuthenticationForm()

    template_name = 'system/login.html'
    return render(request, template_name, {'form': form} )


def search( request ):
    if request.method == 'POST':
        #theShopsId = json.loads(request.POST.get('search_result'))
        theShopsId = request.POST.getlist('search_result[]')
        #theShopsId
        # selected_shop = Shops.objects.filter(id__in=theID)
        # #search_text = request.POST['search_text']
        sort_by = request.POST['sort_by']
        region_filtered = request.POST.getlist('region_filtered[]')
        type_filtered = request.POST.getlist('type_filtered[]')
    else:
        theShopsId = [];

    #print(search_text)

    print( "Shops ID: " + str(theShopsId) )

    # SQLITE_LIMIT_VARIABLE_NUMBER issue where SQLite will have this error "“Too many SQL variables” error in django witih sqlite3"
    # The issue SUSPECTED comes from ".filter(id__in=theShopsId).". Earlier version works fine
    # Remove this line if database is change 
    theShopsId = theShopsId[:950]

    #print("Region: " + str(region_filtered) )
    #print("Type: " + str(type_filtered) )

    search_text = "";

    #shops = Shops.objects.filter(company_name__contains=search_text)
    if( sort_by == "alphabeticalAZ" ):
        #shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(company_name__contains=search_text).order_by("company_name")
        shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(id__in=theShopsId).order_by("company_name")
        #shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(company_name__contains=search_text).order_by("company_name")
    elif( sort_by == "alphabeticalZA" ):
        #shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(company_name__contains=search_text).order_by("-company_name")
        shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(id__in=theShopsId).order_by("-company_name")
    elif( sort_by == "popularity" ):
        #shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(company_name__contains=search_text).order_by("-current_rating")
        shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(id__in=theShopsId).order_by("-current_rating")
    else:
        #shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(company_name__contains=search_text)
        shops = Shops.objects.filter(region__in=region_filtered).filter(categorization__in=type_filtered).filter(id__in=theShopsId)


    #print( "Shop Count: " + str(shops) )

    return render_to_response("ajax_search.html", {'shops': shops } )

def search_poll( request ):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = "";

    print(search_text)

    shops = Shops.objects.filter(company_name__contains=search_text)

    return render_to_response("ajax_poll.html", {'shops': shops } )

def add_review( request, pk ):
    shop = get_object_or_404( Shops, pk=pk )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.shop = shop
            review.save()
            shop.number_of_people_rated = shop.number_of_people_rated  + 1
            shop.current_rating = shop.current_rating + review.rating
            shop.save()
            return redirect('system:detail', pk=shop.pk)
    else:
        form = ReviewForm()

    template_name = 'system/add_review.html'
    return render( request, template_name, {'form':form} )

def favourite(request, pk ):
    shop = get_object_or_404( Shops, pk=pk )
    #Activity.objects.create(content_object=post, activity_type=Activity.LIKE, user=request.user)
    shop.favourite.create(activity_type= Activity.FAVORITE, user=request.user)
    return redirect('system:detail', pk=shop.pk)

def managepoll(request):
    # some data we might wanna pass over
    form = AuthenticationForm()
    #else redirect to login page
    if request.user.is_authenticated:
        user = request.user
        polls = Poll.objects.filter(user=user).filter(deleted = False)
        context = {'form': form, 'polls': polls }
    else:
        context = {'form': form }
        return redirect('system:login_user')
    # context = {
    #     'username': request.user.get_username,
    #     'all_reports': Shops.objects.all()
    # }

    return render(request, 'system/managepoll.html', context)

def submitpoll(request):
    if request.method == 'POST':
        selected_choice = request.POST.get('selected_pk')
        code = request.POST.get('code')
        poll_pk = request.POST.get('poll_pk')
        print("Hello FROM SUBMITPOST")

        poll = Poll.objects.get(pk=poll_pk)
        poll.current_participant = poll.current_participant + 1
        poll.save()

        choice = Choice.objects.get(pk=selected_choice)
        choice.vote_count = choice.vote_count + 1
        choice.save()

        vote = Vote(user=request.user,poll=poll, selected=choice)
        vote.save()
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'success': True,
        'url': reverse('system:poll_detail', args=[poll.code,]),
    }

    return JsonResponse(data)

def closepoll(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        poll_pk = request.POST.get('poll_pk')
        print("Hello FROM closepoll")

        poll = Poll.objects.get(pk=poll_pk)
        poll.closed = True
        poll.save()
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'success': True,
        'url': reverse('system:poll_detail', args=[poll.code,]),
    }

    return JsonResponse(data)

def poll_detail(request, code):
    active_poll = Poll.objects.filter( deleted = False )
    instance = get_object_or_404(active_poll, code=code)
    choices = Choice.objects.filter(poll=instance)

    print(instance.user.username)
    print(request.user.username)

    # initialization
    isPollOwner = False
    isShowResult = True

    #timezone.activate(pytz.timezone("Asia/Singapore"))
    my_date = datetime.now(pytz.timezone("Asia/Singapore"))
    print("Date: " + str(my_date))
    print("instance.expiry_date: " + str(instance.expiry_date))
    if my_date > instance.expiry_date:
        print("Closing timeslot")
        instance.closed = True
        instance.save()

    if request.user.is_authenticated:
        if request.user == instance.user:
            isPollOwner = True
        else:
            voteCount = Vote.objects.filter(poll=instance).filter(user=request.user).count()
            if voteCount > 0 or instance.closed == True:
                isShowResult = True
            else:
                isShowResult = False
    else:
        return redirect('system:login_user')

    context = {
        'instance': instance,
        'choices': choices,
        'isShowResult': isShowResult,
        'isPollOwner': isPollOwner,
    }

    print("Redirect Page to Poll.html")

    template_name = 'system/poll.html'
    return render(request, template_name, context )

def finishpoll(request):
    if request.method == 'POST':
        poll_title = request.POST.get('title')
        participant = request.POST.get('participant')
        expirydate = request.POST.get('expirydate')
        choices = request.POST.getlist('choices[]')

        #print("Date: " + str(expirydate))

        print("Creating Poll...")

        poll = Poll(title=poll_title, user=request.user,current_participant=0, no_of_participant= participant)
        # Note: commit=False don't work for form that doesn't have ModelForm
        poll.save()
        code = poll.pk ^ 0xABCDEFAB
        #print("Code:" + str(code) )
        poll.code = code;
        poll.expiry_date = poll.expiry_date + timedelta(days=int(expirydate))
        poll.save()

        print("Created Poll...")

        print(choices)

        for value in choices:
            print("Value:" + value)
            shop = Shops.objects.get(pk=value)
            choice = Choice (poll=poll, shop=shop, vote_count=0)
            choice.save()
            #print "%s %s" %(key, value)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'success': True,
        'url': reverse('system:poll_detail', args=[poll.code,]),
    }

    return JsonResponse(data)
    #return redirect(, code = poll.code)

def deletepoll(request):
    if request.method == 'POST':
        poll_id = request.POST.get('poll_pk')
        print("Deleting Poll...")
        poll = Poll.objects.get( pk = poll_id )
        poll.deleted = True
        poll.save()
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'success': True,
        'url': reverse('system:managepoll'),
    }

    return JsonResponse(data)
    #return redirect(, code = poll.code)

class DetailView( generic.DetailView ):
    model = Shops
    template_name = 'system/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        shop = Shops.objects.get(pk = self.kwargs['pk'] )
        # Note the "reviews_set" is from models.py inside Review foreign key initialization
        reviews = shop.reviews_set.all()
        form = AuthenticationForm()
        context['reviews'] = reviews
        context['form'] = form

        if self.request.user.is_authenticated:
            user = self.request.user
            related_object_type = ContentType.objects.get_for_model(shop)
            activity = Activity.objects.filter(user=user).filter(content_type__pk = related_object_type.id, object_id=shop.pk)
            context['favourited'] = activity

        return context
