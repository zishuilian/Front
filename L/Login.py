from Core import userAction
from flask import make_response
def cachehave(user, cache):
    isLogin = cache.get(user)
    print('isLogin:', isLogin)
    if isLogin is None:
        return False
    elif isLogin is 1:
        return True

def userCreate():
    userAction.userCreateAccount("textuser","123")

def delete_cookie():
    response=make_response("delete")
    response.delete_cookie('userID')
    return response

def set_cookie(user):
    response= make_response('set')
    response.set_cookie('userID', user)
    return response

def login(user:str, password:str):
    return userAction.userLogIn(user, password)
