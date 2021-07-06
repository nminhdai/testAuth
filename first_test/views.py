from django.shortcuts import render
from django.contrib import auth
import pyrebase

config = {
    'apiKey': "AIzaSyC0zfw9sfuY8zUiYWxDBQNnsPCp24604Ms",
    'authDomain': "testauth-f2181.firebaseapp.com",
    'databaseURL':"https://testauth-f2181-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'projectId': "testauth-f2181",
    'storageBucket': "testauth-f2181.appspot.com",
    'messagingSenderId': "637678915551",
    'appId': "1:637678915551:web:e257a9a44929a3a3837e6a",
}
# Initialize Firebase
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
def signIn(request):
    return render(request, "signIn.html")

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message="Invalid credentials"
        return render(request,"signIn.html",{"message": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {"email":email})

def logout(request):
    auth.logout(request)
    return render(request, 'signIn.html')

def signUp(request):
    return render(request, 'signup.html')

def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user=authe.create_user_with_email_and_password(email, password)
    except:
        message="Unable to create account try again"
        return render(request, "signup.html", {"message": message})
   
    uid = user['localId']
    data ={"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request, "signIn.html")
