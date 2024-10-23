from .models import User, Session
from django.shortcuts import redirect


authList = ['/', '/users/new/', '/users/', '/sessions/', '/sessions/new/']

def authMiddleware(next):

    def middleware(request):
        if request.path not in authList:
            sessionToken = request.COOKIES.get("sessionId")
            if sessionToken == None:
                print("BLOCKING PATH")
                return redirect("/sessions/new/")
            else:
                userRef = Session.objects.filter(token=sessionToken).first()
                if userRef is None:
                    print("BLOCKING PATH FROM SPOOFED SESSION ID")
                    return redirect("/sessions/new/")
                else:
                    user = User.objects.get(id=userRef.userId)
                    userObj = {
                        "userObj":user
                    }
                    request.user = userObj
                    res = next(request)
                    return res
        else:
            res = next(request)
            return res
    
    return middleware
