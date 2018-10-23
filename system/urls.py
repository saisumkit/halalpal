from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

app_name = 'system'

urlpatterns = [
    path( '', views.blank, name='blank' ),

    # register pages
    url(r'^register/$', views.register, name='register'),
    #url( r'^register/$', views.UserFormView.as_view(), name='register'),

    # Login Page
    url(r'^login/$', views.login_user, name='login_user'),

    # Logout Page
	url(r'^logout/$', views.logout_user, name='logout_user'),

    # index page refer to the main page
    path('home',views.home, name='home'),

    url( r'^search/$', views.search, name="search" ),

    # Detail views
    url( r'^shop/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # write a reviews
    #url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^shop/(?P<pk>[0-9]+)/review/$', views.add_review, name="add_review"),

    # favourite a shops
    #url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^shop/(?P<pk>[0-9]+)/favourite/$', views.favourite, name="favourite"),

    path('createpoll',views.createpoll, name='createpoll'),

    path('managepoll',views.managepoll, name='managepoll'),

    url(r'^favourite/$',views.userfavourite, name='userfavourite'),

    url( r'^searchpoll/$', views.search_poll, name="search_poll" ),

    url( r'^submitpoll/$', views.submitpoll, name="submitpoll" ),

    url( r'^closepoll/$', views.closepoll, name="closepoll" ),

    url(r'^finishpoll/$', views.finishpoll, name='finishpoll'),

    url(r'^deletepoll/$', views.deletepoll, name='deletepoll'),

    # Detail views for poll
    url( r'^poll/(?P<code>[0-9]+)/$', views.poll_detail, name='poll_detail'),
]
