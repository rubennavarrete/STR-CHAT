from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# # Create your views here.
# from firebase import Firebase as pyrebase
import pyrebase

config={
  "apiKey": "AIzaSyD3Igrtg8IbuZhlEkaoJSKClb7Ce8OCGY0",
  "authDomain": "strc-e9f06.firebaseapp.com",
  "projectId": "strc-e9f06",
  "storageBucket": "strc-e9f06.appspot.com",
  "messagingSenderId": "149199499489",
  "appId": "1:149199499489:web:a3a1e477cdb12157edc7a0",
  "databaseURL": "https://strc-e9f06-default-rtdb.firebaseio.com",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    if request.method=="POST":
        message = request.POST['message']
        username = request.POST['username']
        room_id = request.POST['room_id']

        # new_message = value=message, user=username, room=room_id
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        # result=database.child('room').child('user').push({"value":send})
        # new_message.save()
        array = [{ 'message':message },{ 'username': username }, { 'room_id': room_id }]
        full_msz = database.child('allmassage').child('messages').push({'Details':array })
        return HttpResponse('Message sent successfully')
    return HttpResponse('Message error!')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})