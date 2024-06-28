import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

from myapp.models import *

import json
from web3 import Web3, HTTPProvider
blockchain_address = 'http://127.0.0.1:7545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = r'E:\FundEr\myapp\static\funder\build\contracts\MyContract.json'
deployed_contract_addressa = '0xe7642a8B7017780C3dEaf66557F696Af8BBf6765'
with open('myapp/static/funder/build/contracts/MyContract.json') as f:
    contract_data = json.load(f)
contract_abi = contract_data['abi']
contract = web3.eth.contract(address=deployed_contract_addressa, abi=contract_abi)
sender_address = '0xB102De466034208fF665a9467DF69BEA4036bF79'


def pay(sender_address, to, amount):

    blockchain_address = "http://127.0.0.1:7545"
    web3 = Web3(HTTPProvider(blockchain_address))
    if web3.is_connected():
        contract_address = deployed_contract_addressa



        gas_price = web3.eth.gas_price
        gas_limit = 100000

        tx_hash = web3.eth.send_transaction({
            'from': sender_address,
            'to': to,
            'value': web3.to_wei(amount, 'ether'),
            'gas': gas_limit,
            'gasPrice': gas_price,
        })


def login(request):
    request.session['lid'] = ''
    return render(request,'lindex.html')

def login_post(request):
    print(request.POST)
    lusername=request.POST['username']
    lpassword=request.POST['password']
    result=Login.objects.filter(username=lusername,password=lpassword)
    if result.exists():
        result2=Login.objects.get(username=lusername,password=lpassword)
        request.session['lid']=result2.id
        if result2.type=='admin':
            return HttpResponse('''<script>alert('admin login success');window.location='/myapp/admin_home/ '</script>''')
        elif result2.type=='user':
            return HttpResponse('''<script>alert('user login success');window.location='/myapp/user_home/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid password or username');'</script>''')

    else:
        return HttpResponse('''<script>alert('invalid password or bad credential');window.location='/myapp/login/'</script>''')


def logout(request):
    request.session['lid']=""
    return HttpResponse('''<script>alert("Session Closed...");window.location='/myapp/login/'</script>''')

def admin_home(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    return render(request,'admin/adminindex.html')


def admin_add_fund_categories(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')
    return render(request,'admin/add fund category.html')

def admin_add_fund_categories_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    cat = request.POST['textfield3']
    ob = SchemeCategory()
    ob.name = cat
    ob.save()
    return HttpResponse('''<script>alert("Category Added...");window.location='/myapp/admin_add_fund_categories/'</script>''')

def admin_view_fund_categories(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')
    ob = SchemeCategory.objects.all()
    return render(request,'admin/view category.html', {'data':ob})

def admin_delete_fund_categories(request, id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')
    ob = SchemeCategory.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("Category Deleted...");window.location='/myapp/admin_view_fund_categories/'</script>''')


def admin_add_fund_schemes(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')
    ob = SchemeCategory.objects.all()
    return render(request,'admin/add fund scheme.html', {'data':ob})

def admin_add_fund_schemes_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    cid = request.POST['cid']
    title = request.POST['textfield3']
    desc = request.POST['textfield5']
    amt = request.POST['textfield7']
    cnt = request.POST['textfield6']
    photo = request.FILES['photo']
    try:

        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+photo.name
        fs.save(dt, photo)
        path = '/media/'+dt
        id = contract.functions.getSchemeCount().call() + 1

        tx_hash = contract.functions.addScheme(id, title, str(amt), str(cnt), desc, path, 'created', int(cid)).transact(
            {'from': web3.eth.accounts[0]})
    except Exception as e:
        print(e)
    return HttpResponse('''<script>alert("Scheme Added...");window.location='/myapp/admin_add_fund_schemes/'</script>''')

def admin_view_fund_schemes(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    scheme_count = contract.functions.getSchemeCount().call()
    a = []
    try:
        for i in range(scheme_count):
            scheme = contract.functions.getScheme(i).call()
            ob = SchemeCategory.objects.get(id=scheme[7])
            a.append(
                {'id': scheme[0], 'category': ob.name, 'title': scheme[1], 'amount': scheme[2],
                 'count': scheme[3], 'description': scheme[4], 'image': scheme[5],
                 'status': scheme[6]})
    except Exception as e:
        print(e)
    return render(request,'admin/view schemes.html', {'data':a})

def admin_view_fund_requests(request, id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    a = []
    try:
        request_count = contract.functions.getSchemeRequestCount().call()
        for i in range(request_count):
            requests = contract.functions.getSchemeRequest(i).call()
            ob = User.objects.get(id=requests[2])
            if str(requests[5]) == str(id):
                sts = ''
                ex = RequestStatus.objects.filter(SCHEMEREQUEST=requests[0])
                if ex.exists():sts = ex[0].Status
                a.append({'id':requests[0], 'date':requests[1], 'user':ob.name,
                          'purpose':requests[3], 'idPath':requests[4], 'status':sts})
    except Exception as e:
        print(e)
        pass
    return render(request,'admin/view schemes requests.html', {'data':a})

def admin_approve_fund_requests(request, id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    try:
        request_count = contract.functions.getSchemeCount().call()
        for i in range(request_count):
            requests = contract.functions.getSchemeRequest(i).call()
            if str(requests[0]) == str(id):
                recipient_address = User.objects.get(id=requests[2]).wallet_address


                scheme = [
                    {
                        'title': contract.functions.getScheme(j).call()[1]
                           if contract.functions.getScheme(j).call()[0] == int(requests[5]) else '',
                           'amount': contract.functions.getScheme(j).call()[2]
                           if contract.functions.getScheme(j).call()[0] == int(requests[5]) else '0',
                           'count': contract.functions.getScheme(j).call()[3]
                           if contract.functions.getScheme(j).call()[0] == int(requests[5]) else '0',
                    }
                          for j in range(contract.functions.getSchemeCount().call())
                        ]

                ttlCnt = scheme[0]['count']
                ttlAmount = scheme[0]['amount']
                singleAmount = float(ttlAmount)/float(ttlCnt)
                sender_balance = web3.eth.get_balance(sender_address)

                amount_wei = web3.to_wei(singleAmount, 'ether')

                if sender_balance < amount_wei:
                    return HttpResponse(
                        '''<script>alert("'Insufficient balance to transfer Ether'...");history.back()</script>''')
                contract.functions.transferEther(recipient_address, amount_wei).transact({'from': sender_address})
                RequestStatus.objects.filter(SCHEMEREQUEST=id).update(Status='Approved', Amount=singleAmount)

                tob = Transactions()
                tob.Status = 'Completed'
                tob.Date = datetime.date.today()
                tob.Sender = sender_address
                tob.Reciever = recipient_address
                tob.Amount = singleAmount
                tob.SCHEMEREQUEST = id
                tob.save()
                return HttpResponse(
                    '''<script>alert("Request Approved...");window.location='/myapp/admin_view_fund_schemes/'</script>''')

    except Exception as e:
        print(e)
        pass
    return HttpResponse('''<script>alert("Request Approved...");window.location='/myapp/admin_view_fund_schemes/'</script>''')

def admin_reject_fund_requests(request, id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    RequestStatus.objects.filter(SCHEMEREQUEST=id).update(Status='Declined')
    return HttpResponse('''<script>alert("Request Declined...");window.location='/myapp/admin_view_fund_schemes/'</script>''')

def admin_change_password(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    return render(request,'admin/admin_change_password.html')

def admin_change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    var= Login.objects.get(id=request.session['lid'])
    if var.password==old:
        if new == confirm:
            var.password=confirm
            var.save()
            return HttpResponse('''<script>alert("user password changed");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert("PASSWORDS DO NOT MATCH");history.back()</script>''')
    else:
        return HttpResponse('''<script>alert("CURRENT PASSWORD DO NOT MATCH");history.back()</script>''')


def admin_view_complaints(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var=Complaint.objects.all()
    return render(request,'admin/view_complaint.html',{'var':var})

def admin_view_complaints_search(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    f=request.POST["f"]
    t=request.POST["t"]
    var=Complaint.objects.filter(date__range=[f,t])
    return render(request,'admin/view_complaint.html',{'var':var})

def complaint_reply(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var=Complaint.objects.get(id=id)
    return render(request,'admin/complaint_reply.html',{'var':var})

def complaint_reply_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var=request.POST['reply']
    var2=request.POST['id']
    a=Complaint.objects.get(id=var2)
    a.reply=var
    a.status='Replied'
    a.save()
    return HttpResponse('''<script>alert("reply has been successfully sent");window.location='/myapp/admin_view_complaints/'</script>''')

def view_user(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    res=User.objects.all()
    return render(request,"admin/viewuser.html",{'data':res})

def search_user(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    search = request.POST['search']
    res=User.objects.filter(name__icontains=search)
    return render(request,"admin/viewuser.html",{'data':res})
###########################


###################user


def user_home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    return render(request,'user/userindex.html')


def change_password(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    return render(request,'user/change_password.html')

def change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    var= Login.objects.get(id=request.session['lid'])
    if var.password==old:
        if new == confirm:
            var.password=confirm
            var.save()
            return HttpResponse('''<script>alert("user password changed");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert("PASSWORDS DO NOT MATCH");history.back()</script>''')
    else:
        return HttpResponse('''<script>alert("CURRENT PASSWORD DO NOT MATCH");history.back()</script>''')

def signup(request):

    return render(request, "user/user_signup_index.html")

def signup_post(request):

    name = request.POST['textfield']
    dob = request.POST['textfield8']
    gender = request.POST['RadioGroup1']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']

    wallet_address = request.POST['textfield14']
    place = request.POST['textfield4']

    password = request.POST['textfield16']

    photo = request.FILES['fileField']
    if Login.objects.filter(username=email).exists():
        return HttpResponse('''<script>alert("Mail already exists");history.back()</script>''')

    from datetime import datetime
    date = 'users/'+datetime.now().strftime('%Y%m%d-%H%M%S%f') + photo.name
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)

    var = Login()
    var.username = email
    var.password = password
    var.type = 'user'
    var.save()

    var2 = User()
    var2.LOGIN_id = var.id
    var2.name = name
    var2.wallet_address = wallet_address
    var2.place = place
    var2.dob = dob
    var2.phone = phone
    var2.gender = gender
    var2.email = email
    var2.image=path
    var2.save()

    return HttpResponse('''<script>alert("user register success");window.location='/myapp/login/'</script>''')

def view_user_profile(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'user/view_profile.html',{'data':var})

def edit_profile(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    res = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,"user/edit_profile.html",{'data':res})

def editprofilepost(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    name = request.POST['textfield']
    dob = request.POST['textfield8']
    gender = request.POST['RadioGroup1']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']

    wallet_address = request.POST['textfield14']
    place = request.POST['textfield4']


    lid=request.session['lid']

    var2 = User.objects.get(LOGIN_id=lid)
    var2.name = name
    var2.wallet_address = wallet_address
    var2.place = place
    var2.dob = dob
    var2.phone = phone
    var2.gender = gender
    var2.save()

    return HttpResponse('''<script>alert("successfully updated");window.location='/myapp/view_user_profile/'</script>''')

def sent_complaint(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    return render(request,'user/send_complaints.html')

def sent_complaint_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var=request.POST['complaint']

    date=datetime.datetime.now().strftime('%Y-%m-%d')
    c_obj=Complaint()
    c_obj.complaint=var
    c_obj.date=date
    lid = request.session['lid']
    id = User.objects.get(LOGIN_id=lid)
    c_obj.USER_id = id.id
    # c_obj.USER_id=User.objects.get(LOGIN_id=request.session['lid']).LOGIN_id
    c_obj.save()
    return HttpResponse('''<script>alert("complaint succesfully sent");window.location='/myapp/user_home/'</script>''')




def user_view_reply(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    var=Complaint.objects.filter(USER__LOGIN=request.session['lid'])
    return render(request,'user/view_reply.html',{'var':var})

def user_view_replysearch(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    f=request.POST['f']
    t=request.POST['t']
    var=Complaint.objects.filter(USER__LOGIN=request.session['lid'], date__range=[f,t])
    return render(request,'user/view_reply.html',{'var':var})

def user_view_fund_schemes(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    scheme_count = contract.functions.getSchemeCount().call()
    a = []
    try:
        request_count = contract.functions.getSchemeRequestCount().call()
        myRequests = []
        for j in range(request_count):
            requests = contract.functions.getSchemeRequest(j).call()
            if str(requests[2]) == str(User.objects.get(LOGIN_id=request.session['lid']).id):
                myRequests.append(requests[5])
        for i in range(scheme_count):
            scheme = contract.functions.getScheme(i).call()
            if scheme[0] not in myRequests:
                ob = SchemeCategory.objects.get(id=scheme[7])
                a.append(
                    {'id': scheme[0], 'category': ob.name, 'title': scheme[1], 'amount': scheme[2],
                     'count': scheme[3], 'description': scheme[4], 'image': scheme[5],
                     'status': scheme[6]})
    except Exception as e:
        print(e)
    return render(request,'user/view schemes.html', {'data':a})

def user_send_fund_request(request, id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')
    return render(request,'user/request purpose.html', {'id':id})

def user_send_fund_request_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    sid = request.POST['id']
    lid = request.session['lid']
    purpose = request.POST['purpose']
    photo = request.FILES['idProof']
    try:
        date = datetime.date.today()
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+photo.name
        fs.save(dt, photo)
        path = '/media/'+dt
        uid = User.objects.get(LOGIN_id=lid).id
        id = contract.functions.getSchemeCount().call() + 1

        tx_hash = contract.functions.addSchemeRequest(id, str(date), str(uid), str(purpose), path, int(sid)).transact(
            {'from': web3.eth.accounts[0]})

        re = RequestStatus()
        re.SCHEMEREQUEST=sid
        re.Status = 'Pending'
        re.save()
    except Exception as e:
        print(e)
    return HttpResponse('''<script>alert("Fund Requested...");window.location='/myapp/user_view_fund_schemes/'</script>''')

def user_view_fund_requests(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    a = []
    try:
        request_count = contract.functions.getSchemeRequestCount().call()
        for i in range(request_count):
            requests = contract.functions.getSchemeRequest(i).call()

            scheme = [{'title': contract.functions.getScheme(j).call()[1]
                        if contract.functions.getScheme(j).call()[0] == int(requests[5]) else '',
                       'amount': contract.functions.getScheme(j).call()[2]} for j in
                      range(contract.functions.getSchemeCount().call())]




            sts = RequestStatus.objects.filter(SCHEMEREQUEST=requests[0])[0].Status
            uid = User.objects.get(LOGIN_id=request.session['lid']).id
            if str(requests[2]) == str(uid) and sts=='Pending':
                a.append({'id':requests[0], 'date':requests[1],
                          'status':sts, 'purpose':requests[3],
                          'title':scheme[0]['title'], 'amount':scheme[0]['amount'],
                          'idPath':requests[4]})
    except Exception as e:
        pass
    return render(request,'user/view schemes requests.html', {'data':a})

def user_view_approved_fund_requests(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    a = []
    try:
        uid = User.objects.get(LOGIN_id=request.session['lid'])
        request_count = contract.functions.getSchemeRequestCount().call()
        for i in range(request_count):
            requests = contract.functions.getSchemeRequest(i).call()

            scheme = [{'title': contract.functions.getScheme(j).call()[1]
                        if contract.functions.getScheme(j).call()[0] == int(requests[5]) else '',
                       'amount': contract.functions.getScheme(j).call()[2]} for j in
                      range(contract.functions.getSchemeCount().call())]




            sts = RequestStatus.objects.filter(SCHEMEREQUEST=requests[0])[0].Status
            if str(requests[2]) == str(uid.id) and sts=='Approved':
                a.append({'id':requests[0], 'date':requests[1],
                          'status':sts, 'purpose':requests[3],
                          'title':scheme[0]['title'], 'amount':scheme[0]['amount'],
                          'idPath':requests[4]})

    except Exception as e:
        pass
    return render(request,'user/view approved requests.html', {'data':a})


####################################

def get_transaction_history(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert("Session Expired...");window.location='/myapp/login/'</script>''')

    res = Transactions.objects.filter(Reciever=User.objects.get(LOGIN_id=request.session['lid']).wallet_address)
    return render(request,'user/view transactions.html', {'data':res})
