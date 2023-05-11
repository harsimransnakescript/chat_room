from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from .consumers import connected_users




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            auth_login(request, user_obj)
            print(user_obj)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['phone']
        password = request.POST['password']
        user_obj  = User.objects.create(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        pro_obj = Profile.objects.create(user_id=user_obj.id ,fullname = fullname, mobile = mobile)
        pro_obj.save()
        return redirect('login/')

    else:
        return render(request, 'signup.html')
    

@user_passes_test(lambda user: user.is_staff,login_url='/user')
def index(request):
    return render(request, "index.html")

@login_required
def room(request, room_name):
    username = request.user.username
    user_obj = User.objects.filter(username=username, is_superuser=True).first()
    if user_obj:
        return HttpResponse('You are admin, So You cannot open chat room ')
    return render(request, "room.html", {"room_name": room_name, "username": username})

def normal_user_View(request):
    username = request.user
    user_obj = User.objects.filter(username=username).first()
    if user_obj:
        user_id = user_obj.id
        pro_obj = Profile.objects.filter(user_id=user_id).first()
        room_name = pro_obj.roomName
        if room_name:
             data = [{'roomname': room_name},]
        else:
            data = ''
        data = {"data": data}
    return render(request, "normal_user.html" , data)

@csrf_exempt
def chat_room_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            print("===>",body)
            room_name = body.get('name')
            if room_name:
                room = Room.objects.create(name=room_name)
                data = {'name': room.name}
                return JsonResponse(data)
            else:
                roomname = body.get('roomanme')
                full_names = body.get('user_ids') 
                for fullname in full_names:
                     print(fullname)
                     pro_obj = Profile.objects.filter(fullname =fullname).first()
                     pro_obj.roomName = roomname
                     pro_obj.save()
                data = {'name': roomname}
                return JsonResponse(data)
        except Exception as e:
            return HttpResponseBadRequest('Failed to create chat room')
    elif request.method == 'GET':
        rooms = Room.objects.all()
        room_names = [room.name for room in rooms]
        return JsonResponse(room_names, safe=False)
    else:
        return HttpResponseBadRequest('Invalid request method')
    

def user_list_View(request):
    users = Profile.objects.all().values('fullname')
    return JsonResponse(list(users), safe=False)

def add_roomName(request):
    # get the current user's profile
    profile = Profile.objects.get(user=request.user)

    # get the list of user IDs from the JSON data
    user_ids = request.POST.getlist('users[]')

    # add the selected users to the chat room
    for user_id in user_ids:
        # get the user's profile
        user_profile = Profile.objects.get(user_id=user_id)

        # add the user's name and email to the room's users list
        room_users = profile.roomName
        room_users.append({
            'name': user_profile.fullname,
            'email': user_profile.email
        })
        profile.room_users = room_users

    # save the updated profile
    profile.save()

    # return a JSON response
    return JsonResponse({'success': True})

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.cache import cache_control


from django.http import JsonResponse


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_status(request, room_name):
    online_pro_objs = Profile.objects.filter(roomName=room_name, is_verified=True)
    online_usernames = [pro_obj.fullname for pro_obj in online_pro_objs]

    offline_pro_objs = Profile.objects.filter(roomName=room_name, is_verified=False)
    offline_usernames = [pro_obj.fullname for pro_obj in offline_pro_objs]

   
    response_data = {
        'status': {'online' : online_usernames },
        'status1': {'offline' : offline_usernames },
    }
    print(response_data)
    return JsonResponse(response_data)
