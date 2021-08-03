from django.db.models import query
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
# Create your views here.


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('/')
    else:
        return render(request, 'login.html')

def home(request):
    user_query = User.objects.all()

    return render(request, 'home.html', {'users': user_query})


def room(request, room):
    username = request.user.username
    room_details = Room.objects.get(name=room)

    roomquery = room
    userid = User.objects.get(username=username)
    id = str(roomquery).split(str(userid.id))
    guestid = id[0]
    if guestid == '':
        guestid = id[1]
    guest = User.objects.get(id=guestid)
    print(guest)
    return render(request, 'room.html', {
        'username': username,
        'guest': guest,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    guest = request.POST['username']
    user = request.user.username
    user1 = User.objects.get(username=user)
    user2 = User.objects.get(username=guest)

    room = str(user1.id) + str(user2.id) 
    if user1.id > user2.id:
        room = str(user2.id) + str(user1.id)

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+user)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+user)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)

    user = request.user
    return JsonResponse({"messages": list(messages.values())})


def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('/')
    
