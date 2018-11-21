from flask import Flask, request, make_response, session
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.contrib.cache import SimpleCache
import Core.AccountTable as AT
from L.Login import cachehave
import tool
from Core.Bus import Bus
from L import Login
from Core import userAction
from flask import flash, redirect, url_for
from Interface import PassengerInterface
from L import Account
import userOperate
import managerOperate
'''
注意变量名不能是函数名，要不然会直接传函数指针进去。
变量名要规范，必须是username而不是user
多assert做类型，和非空判断
变量基本都是str类型
ID 类全部使用str类型
'''
autologinCache = SimpleCache()   #用于自动登陆的缓存

link = {
    'showTicket': '/showTicket',
    'passengerInfo': '/passengerInfo',
    'ticketHistory': '/ticketHistory',
    'logout': '/login',
    'buyTicket': '/buyTicket',
    'logincookie': '/logincookie',
    'user': '/user',
    'findbus': '/findbus',
    'buyticket': '/buyticket',
    'userBuyTicket': '/userBuyTicket',
    'addPassenger': '/addPassenger',
    'deletePassenger': '/deletePassenger',
    'changePassenger': '/changePassenger',
    'managerChangeBus': '/managerChangeBus',
    'managerFindBus': '/managerFindBus',
    'managerAddBus': '/managerAddBus',
    'register': '/register'
}

message_dict = {
    'passwordError': '帐号密码错误',
    'buyTicketError': '购买车票失败',
    'registerError': '帐号已经存在，请更换帐号进行注册！'
}


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


app = Flask(__name__, static_url_path='', static_folder='static/')

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # for example, '3ef6ffg4'


@app.route('/', methods=['post', 'get'])
def home():
    if Login.cachehave(request.cookies.get('userID'), autologinCache):
        return redirect(url_for('user/'+request.cookies.get('userID')))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['post', 'get'])
def login():
    user = request.cookies.get('userID')
    if cachehave(user,  autologinCache):
        return redirect(url_for(link['showTicket']))
    else:
        return render_template('Login/login.html', link=link)


@app.route('/chart', methods=['get', 'post'])
def chart():
    return render_template('Admin/chart.html')


@app.route('/dispatch', methods=['get'])
def dispatch():
    return render_template('Admin/dispatch.html')


@app.route('/revenue', methods=['get'])
def revenue():
    return render_template('Admin/revenue.html')


@app.route('/adminTable', methods=['get', 'post'])
def adminTable():
    # buses = tool.get_buses()
    buses = [Bus()]

    return render_template('Admin/table.html', buses=buses, link=link)


@app.route('/system', methods=['get', 'post'])
def system():
    return render_template('Admin/system.html')


@app.route('/logincookie', methods=['post', 'get'])
def logincookie():
    username = request.form.get('loginUserName')
    password = request.form.get('loginPassWord')
    assert username is not None
    assert password is not None
    t = Login.login(username, password)
    if t == 2:  # 登录成功
        if AT.AccountTable().getLevel(username) == 0:
            # Login.set_cookie(user)
            session.permanent = True
            session['username'] = username
            # autologinCache.set(user, 1, timeout=1 * 60)
            print('user {} login'.format(username))
            return render_template('User/showTicket.html', user=username, link=link, buses=tool.get_buses())
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('error', message='passwordError'))


@app.route('/register', methods=['post','get'])
def register():
    session.pop('username')
    username = request.form.get('reg_username')  # 只有post方式才能获取这个值
    password = request.form.get('reg_password')
    assert username is not None
    assert password is not None
    print('user {} register'.format(username))
    if userOperate.register(username, password):
        session['username'] = username
        return redirect(url_for('user', u=user))      #注册成功
    else:
        return redirect(url_for('error', message='registerError'))


@app.route('/admin',methods=['get','post'])
def admin():
    bus_list = userOperate.get_buses()
    return render_template('Admin/table.html', buses=bus_list, link=link )


@app.route('/showTicket', methods=['get', 'post'])
def showTicket():
    username = session['username']
    buses = tool.get_buses()
    print(buses)
    return render_template('User/showTicket.html', user=username, link=link, buses=buses)


@app.route('/error/<message>', methods=['get', 'post'])
def error(message):
    if message in ['passwordError', 'registerError']:
        return render_template('error.html', message=message_dict[message], turnLink=url_for('login'))
    else:
        return render_template('error.html', message=message_dict[message], turnLink=url_for('showTicket'))


@app.route('/searchTicket', methods=['get', 'post'])  #
def searchTicket():
    start = request.form.get('起点站')
    end = request.form.get("终点站")
    bus_list = tool.get_bus(start, end)
    return render_template('User/showTicket.html', buses=bus_list, link=link)


@app.route('/user', methods=['get', 'post'])
def user():
    username = request.form.get('loginUserName')
    if username is None:
        username = session['username']
        assert username is not None
    bus_list = userOperate.get_buses()
    return render_template('User/showTicket.html', user=username, buses=bus_list, link=link)


@app.route('/findbus', methods=['get', 'post'])
def findbus():
    username = session['username']
    # user = request.form.get('user')
    start = request.form.get('起点站')
    end = request.form.get("终点站")
    bus_list = userOperate.get_bus(start, end)
    return render_template('User/showTicket.html', user=user, buses=bus_list, link=link)


@app.route('/buyTicket', methods=['post', 'get'])
def buyTicket():
    username = session.get('username')
    print('user {} open buy ticket page.'.format(username))
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusId = request.form.get("BusId")
    BusDate = request.form.get("BusDate")
    tool.assert_not_none([username, Departure, Destination, BusId, BusDate])
    b = userOperate.get_one_bus(Departure, Destination, BusId, BusDate)
    return userOperate.openBuyTicket(b, username, link)


@app.route('/userBuyTicket',methods=['post', 'get'])
def userBuyTicket():  # 真正买票的界面。
    username = session.get('username')
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusId = request.form.get("BusId")
    BusDate = request.form.get("BusDate")
    card = request.form.get("card")
    tool.assert_not_none([Departure, Destination, BusId, BusDate, card])
    _ = userOperate.buyTicket(username, card, Departure, Destination, BusDate, BusId)
    if _:
        done, undo = _
        done = done[0]
        return render_template('User/ticketHistory.html', done=done, undo=undo, link=link)
    return redirect(url_for('error', message='buyTicketError'))


@app.route('/passengerInfo', methods=['post', 'get'])
def passengerInfo():
    username = session.get('username')
    tool.assert_not_none([username])
    person = userOperate.showUserCard(username)
    passenger_list = [PassengerInterface.PassengerInterface(i) for i in person]
    return render_template('User/passengerInfo.html', user=username, passengers=passenger_list, link=link)


@app.route('/addPassenger', methods=['post', 'get'])
def addPassenger():
    username = session.get('username')
    print('user {} want to add passenger'.format(username))
    card = request.form.get("p_id")
    name = request.form.get('p_name')
    tel = request.form.get('p_tel')
    tool.assert_not_none([card, name, tel])
    passengers = userOperate.addPassenger(username, card, name, tel, link)
    return render_template('User/passengerInfo.html', passengers=passengers, link=link)


@app.route('/deletePassenger', methods=['post', 'get'])
def deletePassenger():
    user = request.form.get('user')
    card = request.form.get("card")
    return userOperate.deletePassenger(user, card, link)

@app.route('/changePassenger',methods=['post', 'get'])
def changePassenger():
    user = request.form.get('user')
    card = request.form.get("card")
    name = request.form.get('name')
    phone = request.form.get('phone')
    return userOperate.changePassenger(user, card, name, phone, link)

@app.route('/returnTicket', methods=['post', 'get'])
def returnTicket():
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusId = request.form.get("BusId")
    BusDate = request.form.get("BusDate")
    username = session['username']
    card = request.form.get("card")


@app.route('/ticketHistory', methods=['get', 'post'])
def ticketHsitory():
    username = session['username']
    print('user {} look up his tickets'.format(username))
    undo_bus_list, total_num = userAction.checkBookList(username)
    done = userAction.checkExpireTicket(username)
    return render_template('User/ticketHistory.html', undoBuses=undo_bus_list, doneBuses=done, link=link)


@app.route('/managerChangeBus', methods=['post','get'])
def changeBus():
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusId = request.form.get("BusId")
    BusDate = request.form.get("BusDate")
    obus = userOperate.get_one_bus(Departure, Destination, BusId, BusDate)
    nbus = obus
    nDeparture = request.form.get("nDeparture")
    nDestination = request.form.get("nDestination")
    nBusId = request.form.get("nBusId")
    nBusDate = request.form.get("nBusDate")
    nleft_num=request.form.get("nleft_num")
    nprice=request.form.get("nprice")
    ndtime=request.form.get("ndtime")
    natime=request.form.get("natime")
    tool.assert_not_none([nDeparture, nDestination, nBusId, nBusDate, nleft_num, nprice, ndtime, natime])
    if (nDeparture!= None ):
        nbus['Departure'] = nDeparture
    if (nDestination!= None):
        nbus['Destination'] = nDestination
    if (nBusId != None):
        nbus['BusId'] = nBusId
    if (nBusDate != None):
        nbus['BusDate'] = nBusDate
    if (nleft_num != None):
        nbus['left_num'] = nleft_num
    if (nprice != None):
        nbus['price'] = nprice
    if (ndtime != None):
        nbus['dtime'] = ndtime
    if (natime != None):
        nbus['atime'] = natime
    if( managerOperate.UpdateBus(obus, nbus) ):
        return True


@app.route('/managerFindBus', methods=['post', 'get'])
def mfindbus():
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusDate = request.form.get("BusDate")
    # bus_list = tool.get_bus(Departure, Destination, BusDate)
    bus_list = [{
        "Departure": 'a'
    }]
    return render_template('Admin/table.html', buses=bus_list, link=link)


@app.route('/managerAddBus',methods=['post','get'])
def maddbus():
    Departure = request.form.get("Departure")
    Destination = request.form.get("Destination")
    BusId = request.form.get("BusId")
    BusDate = request.form.get("BusDate")
    left_num = request.form.get("left_num")
    price = request.form.get("price")
    dtime = request.form.get("dtime")
    atime = request.form.get("atime")
    bus=Bus(BusDate, BusId, dtime , atime, Departure, Destination, left_num, price)
    if(managerOperate.InsertBus(bus)):
        return True


if __name__ == '__main__':
    app.run(port=8000, debug=True)
