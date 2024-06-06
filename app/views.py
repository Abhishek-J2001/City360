from django.shortcuts import render, HttpResponseRedirect
from .models import *
from datetime import date as d, datetime as dt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')

######## HOME ########


def login(request):
    msg = ""
    msg = request.GET.get('msg')
    if request.POST:
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        data = Login.objects.filter(email=email, password=password)
        if data:
            data = Login.objects.get(email=email, password=password)

            if data.userType == "admin":
                msg = "Welcome to Admin Page"
                return HttpResponseRedirect("/admin_home?msg="+msg)

            elif data.userType == "worker":
                workdata = WorkersReg.objects.get(email=email)
                uid = workdata.id
                request.session['uid'] = uid
                msg = "Welcome to Worker Page"
                return HttpResponseRedirect("/worker_home?msg="+msg)

            elif data.userType == "user":
                usrdata = UserReg.objects.get(email=email)
                uid = usrdata.id
                request.session['uid'] = uid
                msg = "Welcome to User Page"
                return HttpResponseRedirect("/user_home?msg="+msg)
        else:
            msg = "Invalid username or password provided"
    return render(request, 'login.html', {"msg": msg})


def userregistration(request):
    msg = ""
    msg = request.GET.get('msg')
    if request.POST:
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Number")
        password = request.POST.get("Password")
        address = request.POST.get("Address")
        gender = request.POST.get("Gender")
        image = request.FILES["image"]
        if UserReg.objects.filter(email=email).exists() or Login.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                email=email, password=password, userType='user')
            abc.save()
            reg = UserReg.objects.create(name=name, email=email, address=address,
                                         phone=phone, password=password, usrid=abc, image=image, gender=gender)
            reg.save()
            msg = "Registration Successful"
    return render(request, 'userregistration.html', {"msg": msg})


def workerregistration(request):
    msg = ""
    msg = request.GET.get('msg')
    cat = Category.objects.all()
    if request.POST:
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Number")
        password = request.POST.get("Password")
        address = request.POST.get("Address")
        image = request.FILES["image"]
        gender = request.POST.get("Gender")
        experience = request.POST.get("Experience")
        location = request.POST.get("Location")
        category = request.POST.get("Category")
        wages = request.POST.get("Wages")
        if WorkersReg.objects.filter(email=email).exists() or Login.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                email=email, password=password, userType='worker')
            abc.save()
            reg = WorkersReg.objects.create(name=name, email=email, address=address,
                                            phone=phone, password=password, worid=abc, image=image, gender=gender, experience=experience, location=location, category=category, wages=wages)

            reg.save()
            msg = "Registration Successful"
    return render(request, 'workerregistration.html', {"msg": msg, "cat": cat})

######## // HOME ########
######## ADMIN ########


def admin_home(request):
    msg = ""
    msg = request.GET.get('msg')
    return render(request, 'admin/adminhome.html', {"msg": msg})


def addcategory(request):
    msg = ""
    msg = request.GET.get('msg')
    if request.POST:
        category = request.POST.get("Category")
        image = request.FILES["image"]
        abc = Category.objects.create(
            category=category, image=image)
        abc.save()
        msg = "Added Successfully"
    return render(request, 'admin/addcategory.html', {"msg": msg})


def viewuser(request):
    abc = UserReg.objects.filter(status="pending")
    efg = UserReg.objects.filter(status="approved")
    return render(request, 'admin/viewuser.html', {"abc": abc, "efg": efg})


def approveuser(request):
    msg = ""
    id = request.GET.get("id")
    print(id)
    efg = UserReg.objects.filter(usrid=id).update(status="approved")
    msg = "Approved"
    return HttpResponseRedirect("/viewuser?msg="+msg)


def rejecteduser(request):
    msg = ""
    id = request.GET.get("ab")
    aab = Login.objects.filter(id=id).delete()
    efg = UserReg.objects.filter(id=id).delete()
    msg = "Rejected"
    return HttpResponseRedirect("/viewuser?msg="+msg)


def deleteuser(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    email = request.GET.get("cd")
    abb = UserReg.objects.filter(email=email).delete()
    abo = Login.objects.filter(email=email).delete()
    msg = "Deleted employee"
    return HttpResponseRedirect("/viewuser", {"msg": msg})


def viewworker(request):
    msg = request.GET.get("msg")
    abc = WorkersReg.objects.filter(status="pending")
    efg = WorkersReg.objects.filter(status="approved")
    return render(request, 'admin/viewworker.html', {"abc": abc, "efg": efg, "msg": msg})


def approveworker(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    print(id)
    efg = WorkersReg.objects.filter(worid=id).update(status="approved")
    msg = "Approved"
    return HttpResponseRedirect("/viewworker?msg="+msg)


def rejectedworker(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    aab = Login.objects.filter(id=id).delete()
    efg = WorkersReg.objects.filter(id=id).delete()
    msg = "Rejected"
    return HttpResponseRedirect("/viewworker?msg="+msg)


def deleteworker(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    email = request.GET.get("cd")
    abb = WorkersReg.objects.filter(email=email).delete()
    abo = Login.objects.filter(email=email).delete()
    msg = "Deleted employee"
    return HttpResponseRedirect("/viewworker", {"msg": msg})


def userfeedback(request):
    msg = ""
    msg = request.GET.get('msg')
    abc = Addfeedback.objects.all()
    return render(request, 'admin/userfeedback.html', {"msg": msg, "abc": abc})


def viewcategory(request):
    msg = ""
    msg = request.GET.get("msg")
    abc = Category.objects.all()
    return render(request, 'admin/viewcategory.html', {"abc": abc, "msg": msg})


def deletecategory(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    abb = Category.objects.filter(id=id).delete()
    msg = "Deleted"
    return HttpResponseRedirect("/viewcategory", {"msg": msg})


def workerfeedback(request):
    msg = ""
    msg = request.GET.get('msg')
    abc = Workeraddfeedback.objects.all()
    return render(request, 'admin/workerfeedback.html', {"msg": msg, "abc": abc})

######## // ADMIN ########
######## USER ########


def user_home(request):
    msg = ""
    msg = request.GET.get('msg')
    return render(request, 'user/userhome.html', {"msg": msg})


def userviewcategory(request):
    msg = request.GET.get('msg')
    abc = Category.objects.all()
    return render(request, 'user/userviewcategory.html', {"abc": abc, "msg": msg})


def bookingcategory(request):
    msg = request.GET.get('msg')
    type = request.GET.get("type")
    abc = WorkersReg.objects.filter(category=type)
    return render(request, 'user/bookingcategory.html', {"abc": abc, "msg": msg})


def bookworker(request):
    msg = ""
    msg = request.GET.get('msg')
    id = request.GET.get("id")
    # print(id, " 3333333333333333333333333333333333")
    uid = request.session['uid']
    # print(uid, " 3333333333333333333333333333333333")
    # worid = request.session['worid']
    rr = d.today()
    today = rr.strftime("%Y-%m-%d")
    abc = WorkersReg.objects.filter(id=id)
    if request.POST:
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Number")
        category = request.POST.get("Category")
        location = request.POST.get("Location")
        startingdate = request.POST.get("Startdate")
        endingdate = request.POST.get("Enddate")
        wages = request.POST.get("Wages")

        sdate = dt.strptime(startingdate, "%Y-%m-%d")
        edate = dt.strptime(endingdate, "%Y-%m-%d")

        date_diff = edate-sdate
        print("date_diff", date_diff)

        totalWage = int(date_diff.days) * (int(wages))

        efg = Booking.objects.create(name=name, email=email, phone=phone, category=category, location=location,
                                     startingdate=startingdate, endingdate=endingdate, wages=totalWage, usrid_id=uid, worid=id)
        efg.save()
        msg = "Booked Successfully"
        return HttpResponseRedirect("/userviewcategory?msg="+msg)
    return render(request, 'user/bookworker.html', {"msg": msg, "abc": abc, "today": today})


def userviewbooking(request):
    msg = request.GET.get('msg')
    uid = request.session['uid']
    abc = Booking.objects.filter(usrid=uid, status="notbooked")
    efg = Booking.objects.filter(usrid=uid, status="approved")
    return render(request, 'user/userviewbooking.html', {"abc": abc, "efg": efg})


def cancelbooking(request):
    msg = ""
    id = request.GET.get("id")
    efg = Booking.objects.filter(id=id).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/userviewcategory?msg="+msg)


def useraddfeedback(request):
    msg = ""
    msg = request.GET.get('msg')
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = WorkersReg.objects.filter(id=id)
    if request.POST:
        name = request.POST.get("Name")
        category = request.POST.get("Category")
        feedback = request.POST.get("Feedback")
        efg = Useraddfeedback.objects.create(
            category=category, name=name, feedback=feedback, usrid_id=uid, worid=id)
        efg.save()
        msg = " Feedback Added Successfully"
        return HttpResponseRedirect("/userviewcategory?msg="+msg)      
    return render(request, 'user/useraddfeedback.html', {"msg": msg, "abc": abc})


def userviewfeedback(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = Useraddfeedback.objects.filter(worid=id)
    return render(request, 'user/userviewfeedback.html', {"abc": abc})


def addfeedback(request):
    msg = ""
    msg = request.GET.get('msg')
    uid = request.session['uid']
    if request.POST:
        feedback = request.POST.get("Feedback")
        efg = Addfeedback.objects.create(
            feedback=feedback, usrid_id=uid)
        efg.save()
        msg = " Feedback Added Successfully"
    return render(request, 'user/addfeedback.html', {"msg": msg})


def userprofile(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = UserReg.objects.filter(id=uid)
    return render(request, 'user/userprofile.html', {"abc": abc})


def updateuser(request):
    msg = ""
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = UserReg.objects.filter(usrid=id)
    if request.POST:
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Number")
        password = request.POST.get("Password")
        address = request.POST.get("Address")
        gender = request.POST.get("Gender")
        image = request.FILES["image"]

        updatedata = UserReg.objects.filter(usrid=id).update(
            name=name, email=email, phone=phone, password=password, address=address, gender=gender, image=image)
        print(updatedata)
        logdata = Login.objects.filter(id=id).update(
            email=email, password=password)
        print(logdata)

        msg = "updated Successfully"
    return render(request, 'user/updateuser.html', {"msg": msg, "abc": abc})


def payment(request):
    msg = ""
    msg = request.GET.get('msg')
    id = request.GET.get('id')
    efg = Booking.objects.filter(id=id)
    if request.POST:
        abc = Booking.objects.filter(id=id).update(status="paid")
        msg = "Payment Successfull"
        return HttpResponseRedirect("/userviewbooking?msg="+msg)
    return render(request, 'user/payment.html', {"msg": msg, "efg":efg})

def userviewpayment(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = Booking.objects.filter(usrid=uid, status="paid")
    return render(request, 'user/userviewpayment.html', {"abc": abc})



######## // USER ########
######## WORKER ########

def worker_home(request):
    msg = ""
    msg = request.GET.get('msg')
    return render(request, 'worker/workerhome.html', {"msg": msg})


def workerviewbooking(request):
    msg = request.GET.get('msg')
    uid = request.session['uid']
    print(uid)
    id = request.GET.get("id")
    abc = Booking.objects.filter(worid=uid, status="notbooked")
    efg = Booking.objects.filter(worid=uid, status="approved")
    return render(request, 'worker/workerviewbooking.html', {"abc": abc, "msg": msg, "efg": efg})


def approvebooking(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    print(id)
    efg = Booking.objects.filter(id=id).update(status="approved")
    msg = "Approved"
    return HttpResponseRedirect("/worker_home?msg="+msg)


def rejectbooking(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    efg = Booking.objects.filter(id=id).delete()
    msg = "Rejected"
    return HttpResponseRedirect("/worker_home?msg="+msg)


def deletebooking(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    abb = Booking.objects.filter(id=id).delete()
    msg = "Deleted"
    return HttpResponseRedirect("/worker_home?msg="+msg)


def workerviewfeedback(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = Useraddfeedback.objects.filter(worid=uid)
    return render(request, 'worker/workerviewfeedback.html', {"abc": abc})


def workeraddfeedback(request):
    msg = ""
    msg = request.GET.get('msg')
    uid = request.session['uid']
    if request.POST:
        feedback = request.POST.get("Feedback")
        efg = Workeraddfeedback.objects.create(
            feedback=feedback, worid_id=uid)
        efg.save()
        msg = " Feedback Added Successfully"
        return HttpResponseRedirect("/worker_home?msg="+msg)
    return render(request, 'worker/workeraddfeedback.html', {"msg": msg})


def workerprofile(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = WorkersReg.objects.filter(id=uid)
    return render(request, 'worker/workerprofile.html', {"abc": abc})


def updateworker(request):
    msg = ""
    id = request.GET.get("id")
    uid = request.session['uid']
    abc = WorkersReg.objects.filter(worid=id)
    cat = Category.objects.all()
    if request.POST:
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Number")
        password = request.POST.get("Password")
        address = request.POST.get("Address")
        image = request.FILES["image"]
        gender = request.POST.get("Gender")
        experience = request.POST.get("Experience")
        location = request.POST.get("Location")
        category = request.POST.get("Category")
        wages = request.POST.get("Wages")
        updatedata = WorkersReg.objects.filter(worid=id).update(
            name=name, email=email, phone=phone, password=password, address=address, gender=gender, image=image, experience=experience, location=location, category=category, wages=wages)
        print(updatedata)
        logdata = Login.objects.filter(id=id).update(
            email=email, password=password)
        print(logdata)
        msg = "updated Successfully"
    return render(request, 'worker/updateworker.html', {"msg": msg, "abc": abc, "cat": cat})

def workerviewpayment(request):
    msg = request.GET.get('msg')
    uid = request.session['uid']
    print(uid)
    id = request.GET.get("id")
    abc = Booking.objects.filter(worid=uid, status="paid")
    return render(request, 'worker/workerviewpayment.html', {"abc": abc, "msg": msg})

def deletepayment(request):
    msg = ""
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    efg = Booking.objects.filter(id=id).delete()
    msg = "Deleted"
    return HttpResponseRedirect("/worker_home?msg="+msg)
