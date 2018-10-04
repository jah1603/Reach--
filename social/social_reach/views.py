# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render
from registration.backends.simple.views import RegistrationView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import User

from social_reach.models import Category, Page, UserProfile, ProfileLikedByActiveUser, ProfileGreetedByActiveUser, Match
from social_reach.forms import CategoryForm, PageForm
from social_reach.forms import UserForm, UserProfileForm

from social_reach.scraper import InstagramScraper


class RangoRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return '/social_reach/'


def add_page(request, category_slug_url):
        cat_list = get_category_list()
	print category_slug_url
	try:
		category = Category.objects.filter(slug=category_slug_url)[0]
	except Category.DoesNotExist:
		category = None

	print category
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if category:
			page = form.save(commit=False)
			page.category = category
			page.views = 0
			page.save()
			return show_category(request, category_slug_url)
		else:
			print form.errors
	_context = {
		'form': form,
		'category': category,
		'title' : 'Add a Page',
        'cat_list': cat_list
	}
	return render(request, 'rango/add_page.html', context=_context)


def add_category(request):
        cat_list = get_category_list()
	form = CategoryForm()



	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print(form.errors)


	return render(request, 'rango/add_category.html', {'form':form, 'cat_list': cat_list})


def show_user(request, username):
    context = RequestContext(request)
    context = {}

    cat_list = get_category_list()

    try:
        user = UserProfile.objects.get(user__username=username)
        if len(ProfileGreetedByActiveUser.objects.filter(profile=username, greeter__user__username=request.user)) > 0:
            greeted_user = ProfileGreetedByActiveUser.objects.filter(profile=username, greeter__user__username=request.user)[0]
            context['greeted'] = greeted_user

        user = UserProfile.objects.get(user__username=username)
        if len(ProfileLikedByActiveUser.objects.filter(profile=username, liker__user__username=request.user)) > 0:
            liked_user = ProfileLikedByActiveUser.objects.filter(profile=username, liker__user__username=request.user)[0]
            context['liked'] = liked_user
        print("HELLO")
        context['viewed_user'] = user
        context['cat_list'] = cat_list

    except UserProfile.DoesNotExist:
        context['viewed_user'] = None
        context['cat_list'] = cat_list

    except ProfileGreetedByActiveUser.DoesNotExist:
        context['greeted'] = None
        context['liked'] = liked_user
        context['viewed_user'] = user
        context['cat_list'] = cat_list
    except ProfileLikedByActiveUser.DoesNotExist:
        context['greeted'] = None
        context['liked'] = None
        context['viewed_user'] = user
        context['cat_list'] = cat_list
    return render(request, 'rango/user_profile.html', context=context)



@login_required
def like_user(request):
    context = RequestContext(request)
    user_id = None
    if request.method == 'GET':
        user_id = request.GET['user_id']
    if user_id:
        user = UserProfile.objects.get(id=int(user_id))
        likes = user.likes
	print("Length", len(Match.objects.filter(first_user=user, second_user=UserProfile.objects.get(user__username=request.user))))

        if user:
            if len(ProfileLikedByActiveUser.objects.filter(profile=user.user.username, liker__user__username=request.user)) == 0:
                    likes = user.likes + 1
                    user.likes = likes
                    user.save()
                    liked_profile = ProfileLikedByActiveUser.objects.create(profile=user.user.username, liker= UserProfile.objects.get(user__username=request.user))
                    liked_profile.save()


	if len(ProfileLikedByActiveUser.objects.filter(profile=UserProfile.objects.get(user__username=request.user), liker=user)) == 1:
			user = UserProfile.objects.get(id=int(user_id))
			if len(Match.objects.filter(first_user=user, second_user=UserProfile.objects.get(user__username=request.user))) == 0:
				match = Match.objects.create(first_user=user, second_user=UserProfile.objects.get(user__username=request.user))
				match.save()
				likes = user.likes
				print("MATCHHH", match)
				print("Length", len(Match.objects.filter(first_user=user, second_user=UserProfile.objects.get(user__username=request.user))))

    	return HttpResponse(likes)
    return HttpResponse(likes)


@login_required
def greet_user(request):
    context = RequestContext(request)
    user_id = None
    if request.method == 'GET':
        user_id = request.GET['user_id']
    if user_id:
        user = UserProfile.objects.get(id=int(user_id))
        greetings = user.greetings
        if user:
            if len(ProfileGreetedByActiveUser.objects.filter(profile=user.user.username, greeter__user__username=request.user)) == 0:
                greetings = user.greetings + 1
                user.greetings = greetings
                user.save()
                greeted_profile = ProfileGreetedByActiveUser.objects.create(profile=user.user.username, greeter= UserProfile.objects.get(user__username=request.user))
                greeted_profile.save()
                return HttpResponse(greetings)
    return HttpResponse(greetings)



def track_url(request):
    context = RequestContext(request)
    page_id = None
    url = '/social_reach/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id = page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)



def show_category(request, category_name_url):
	_context = {}

        cat_list = get_category_list()

	try:
		category = Category.objects.get(slug=category_name_url)

		pages = Page.objects.filter(category=category).order_by('-views')
		_context['category'] = category
		_context['pages'] = pages
	except Category.DoesNotExist:
		_context['category'] = None
		_context['pages'] = None
        _context['cat_list'] = cat_list


	return render(request, 'rango/category.html', context=_context)

def get_category_list():
    cat_list = Category.objects.all().order_by('-views')
    for cat in cat_list:
        cat.url = cat.slug

        return cat_list


@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up

    return render(request, 'rango/profile.html', context_dict)

def index(request):

	user_list = UserProfile.objects.order_by('-user')[:5]

	pages_list = Page.objects.order_by('-views')[:5]
        print(user_list[1].user.username)
        cat_list = get_category_list()
	_context = {
		'users': user_list,
		'most_viewed_pages': pages_list,
		'title' : 'Welcome to Tango with Django',
        'cat_list': cat_list
	}

	response = render(request, 'rango/index.html', context=_context)

        visits = int(request.COOKIES.get('visits', '0'))

        if request.session.get('last_visit'):
# Yes it does! Get the cookie's value.
            last_visit_time = request.session.get('last_visit')
            print(last_visit_time)
            visits = request.session.get('visits', 0)
# If it's been more than a day since the last visit...
            if  (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
# ...reassign the value of the cookie to +1 of what it was before...
                request.session['visits'] = visits + 1
                request.session['last_visit'] = str(datetime.now())
        else:
# Cookie last_visit doesn't exist, so create it to the current date/time.
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = 1
# Return response back to the user, updating any cookies that need changed.

	return render(request, 'rango/index.html', _context)


def about(request):

    cat_list = get_category_list()

    if request.session.get('visits'):
        count = request.session.get('visits')
        print(count)
    else:
        count = 0

    matches_you_liked_first = Match.objects.filter(first_user__user__username=request.user)

    return render(request, 'rango/about.html', 	{'visits': count, 'cat_list': cat_list, 'matches_you_first': matches_you_liked_first, 'matches_them_first': Match.objects.filter(second_user__user__username=request.user)
}
)


def register(request):
	cat_list = get_category_list()
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			instagram_scraper =  InstagramScraper()
			results = instagram_scraper.scrape_instagram_followers(profile.instagram_handle)

			profile.instagram_followers=profile.instagram_followers + results
			profile.save()

			registered = True
		else:
			print user_form.errors
			print profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', {
			'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered,
			'cat_list': cat_list
		})


def user_login(request):
	cat_list = get_category_list()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('social_reach:index'))
			else:
				return HttpResponse("Your account has been disabled. Please contact the admin.")
		else:
			return HttpResponse("Invalid username/password.")
	else:
		return render(request, 'rango/login.html', {'cat_list': cat_list})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('social_reach:index'))


@login_required
def restricted(request):
        cat_list = get_category_list()
	return render(request, 'rango/restricted.html', {'cat_list': cat_list})
