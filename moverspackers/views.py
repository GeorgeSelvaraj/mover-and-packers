from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.views.decorators.http import      require_POST
from datetime import datetime

from .models import *


def _is_super_admin(request):
    return request.user.is_authenticated and request.user.is_superuser


# ================= HOME =================
def index(request):
    return render(request, 'index.html')


def registration(request):
    return render(request, 'registration.html')


# ================= ADMIN LOGIN =================
def admin_login(request):
    error = ""

    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pwd')

        user = authenticate(username=u, password=p)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_home')
        else:
            error = "yes"

    return render(request, 'admin_login.html', {'error': error})


# ================= ADMIN HOME =================
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    totalservices = Services.objects.count()
    totalagents = Agent.objects.filter(is_active=True).count()
    totalunread = Contact.objects.filter(isread=False).count()
    totalread = Contact.objects.filter(isread=True).count()
    newbooking = SiteUser.objects.filter(status=None).count()
    oldbooking = SiteUser.objects.filter(status="1").count()

    return render(request, 'admin_home.html', locals())


# ================= LOGOUT =================
def Logout(request):
    logout(request)
    return redirect('index')


# ================= CHANGE PASSWORD =================
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            error = "no"
            form = PasswordChangeForm(request.user)
        else:
            error = "yes"
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form,
        'error': error
    })


# ================= ADMIN USER MANAGEMENT =================
def manage_admins(request):
    if not _is_super_admin(request):
        return redirect('admin_login')

    error = ""
    field_errors = []

    if request.method == "POST":
        username = (request.POST.get('username') or "").strip()
        email = (request.POST.get('email') or "").strip()
        password = request.POST.get('password') or ""
        is_super = request.POST.get('is_superuser') == "on"

        if not username or not password:
            error = "missing"
        elif User.objects.filter(username__iexact=username).exists():
            error = "duplicate"
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                error = "weak"
                field_errors = list(e.messages)

            if not error:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.is_staff = True
                user.is_superuser = is_super
                user.save()
                error = "no"

    admins = User.objects.filter(is_staff=True).order_by('-id')
    return render(request, 'manage_admins.html', {
        'admins': admins,
        'error': error,
        'field_errors': field_errors,
    })


@require_POST
def delete_admin(request, pid):
    if not _is_super_admin(request):
        return redirect('admin_login')

    if request.user.id == pid:
        return redirect('manage_admins')

    user = get_object_or_404(User, id=pid, is_staff=True)
    user.delete()
    return redirect('manage_admins')


@require_POST
def toggle_admin(request, pid):
    if not _is_super_admin(request):
        return redirect('admin_login')

    if request.user.id == pid:
        return redirect('manage_admins')

    user = get_object_or_404(User, id=pid, is_staff=True)
    user.is_active = not user.is_active
    user.save()
    return redirect('manage_admins')


def reset_admin_password(request, pid):
    if not _is_super_admin(request):
        return redirect('admin_login')

    admin_user = get_object_or_404(User, id=pid, is_staff=True)
    error = ""
    field_errors = []

    if request.method == "POST":
        new1 = request.POST.get('new_password') or ""
        new2 = request.POST.get('confirm_password') or ""

        if not new1 or not new2:
            error = "missing"
        elif new1 != new2:
            error = "mismatch"
        else:
            try:
                validate_password(new1, user=admin_user)
            except ValidationError as e:
                error = "weak"
                field_errors = list(e.messages)

            if not error:
                admin_user.set_password(new1)
                admin_user.save()
                error = "no"

    return render(request, 'reset_admin_password.html', {
        'admin_user': admin_user,
        'error': error,
        'field_errors': field_errors,
    })


# ================= SERVICES =================
def add_services(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""

    if request.method == 'POST':
        try:
            Services.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
                price=request.POST.get('price')
            )
            error = "no"
        except Exception as e:
            print("ADD SERVICE ERROR:", e)
            error = "yes"

    return render(request, 'add_services.html', {'error': error})


def manage_services(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    services = Services.objects.all().order_by('-id')
    return render(request, 'manage_services.html', {'services': services})


def edit_service(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    service = get_object_or_404(Services, id=pid)
    error = ""

    if request.method == 'POST':
        try:
            service.title = request.POST.get('title')
            service.description = request.POST.get('description')

            price = request.POST.get('price')
            if price:
                service.price = price

            if request.FILES.get('image'):
                service.image = request.FILES.get('image')

            service.save()
            error = "no"

        except Exception as e:
            print("EDIT SERVICE ERROR:", e)
            error = "yes"

    return render(request, 'edit_service.html', {
        'service': service,
        'error': error
    })


def delete_service(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    service = get_object_or_404(Services, id=pid)
    service.delete()
    return redirect('manage_services')


def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})


# ================= AGENTS =================
def agents(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""

    if request.method == 'POST':
        try:
            Agent.objects.create(
                name=request.POST.get('name'),
                mobile=request.POST.get('mobile'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                is_active=request.POST.get('is_active') == "on"
            )
            error = "no"
        except Exception as e:
            print("ADD AGENT ERROR:", e)
            error = "yes"

    agent_list = Agent.objects.all().order_by('-id')
    return render(request, 'agents.html', {
        'agents': agent_list,
        'error': error
    })


def delete_agent(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    agent = get_object_or_404(Agent, id=pid)
    agent.delete()
    return redirect('agents')


# ================= ABOUT =================
def about(request):
    return render(request, 'about.html')


# ================= REQUEST QUOTE =================
def request_quote(request):
    error = ""
    services = Services.objects.all()

    if request.method == 'POST':
        try:
            service_id = request.POST.get('service')
            selected_service = None

            if service_id:
                try:
                    selected_service = Services.objects.get(id=service_id)
                except:
                    selected_service = None

            SiteUser.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                mobile=request.POST.get('contact'),
                location=request.POST.get('location'),
                shiftingloc=request.POST.get('shifting_location'),
                shiftingdate=request.POST.get('shifting_date'),
                briefitems=request.POST.get('brief_items'),
                items=request.POST.get('items'),
                requestdate=datetime.now(),

                # SERVICE LINK
                service=selected_service,

                # PRICE AUTO
                total_amount=selected_service.price if selected_service else 0,
                advance_paid=0,
                payment_status="Pending"
            )

            error = "no"

        except Exception as e:
            print("REQUEST QUOTE ERROR:", e)
            error = "yes"

    return render(request, 'request_quote.html', {
        'error': error,
        'services': services
    })


# ================= BOOKINGS =================
def new_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    booking = SiteUser.objects.filter(status=None).order_by('-id')
    return render(request, 'new_booking.html', {'booking': booking})


def view_bookingdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    booking = get_object_or_404(SiteUser, id=pid)
    services = Services.objects.all()
    agents = Agent.objects.filter(
        Q(is_active=True) | Q(id=booking.assigned_agent_id)
    ).order_by('name')
    error = ""

    if request.method == 'POST':
        try:
            booking.name = request.POST.get('name')
            booking.email = request.POST.get('email')
            booking.mobile = request.POST.get('mobile')
            booking.location = request.POST.get('location')
            booking.shiftingloc = request.POST.get('shiftingloc')
            booking.shiftingdate = request.POST.get('shiftingdate')

            booking.briefitems = request.POST.get('briefitems')
            booking.items = request.POST.get('items')
            booking.remarks = request.POST.get('remarks')

            # SERVICE UPDATE
            service_id = request.POST.get('service')
            if service_id:
                try:
                    booking.service = Services.objects.get(id=service_id)
                except:
                    pass

            # AGENT ASSIGNMENT
            agent_id = request.POST.get('assigned_agent')
            if agent_id:
                booking.assigned_agent = Agent.objects.filter(id=agent_id).first()
            else:
                booking.assigned_agent = None

            # PAYMENT
            booking.total_amount = request.POST.get('total_amount') or 0
            booking.advance_paid = request.POST.get('advance_paid') or 0
            booking.payment_status = request.POST.get('payment_status') or "Pending"

            booking.status = "1"
            booking.updatedate = datetime.now()

            booking.save()
            error = "no"

        except Exception as e:
            print("BOOKING ERROR:", e)
            error = "yes"

    return render(request, 'view_bookingdetail.html', {
        'booking': booking,
        'services': services,
        'agents': agents,
        'error': error
    })


def old_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    booking = SiteUser.objects.filter(status="1").order_by('-id')
    return render(request, 'old_booking.html', {'booking': booking})


def delete_booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    booking = get_object_or_404(SiteUser, id=pid)
    booking.delete()
    return redirect('old_booking')


# ================= CONTACT =================
def contact(request):
    error = ""

    if request.method == 'POST':
        try:
            Contact.objects.create(
                name=request.POST.get('fullname'),
                contact_no=request.POST.get('contact'),
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
                isread=False,
                messagedate=datetime.now()
            )
            error = "no"
        except Exception as e:
            print("CONTACT ERROR:", e)
            error = "yes"

    return render(request, 'contact.html', {'error': error})


# ================= QUERIES =================
def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    contact = Contact.objects.filter(isread=False).order_by('-id')
    return render(request, 'unread_queries.html', {'contact': contact})


def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    contact = Contact.objects.filter(isread=True).order_by('-id')
    return render(request, 'read_queries.html', {'contact': contact})


def view_queries(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    contact = get_object_or_404(Contact, id=pid)
    error = ""

    if not contact.isread:
        contact.isread = True
        contact.save()

    if request.method == "POST":
        try:
            contact.name = request.POST.get('name')
            contact.contact_no = request.POST.get('contact_no')
            contact.email = request.POST.get('email')
            contact.subject = request.POST.get('subject')
            contact.message = request.POST.get('message')

            contact.save()
            error = "no"

        except Exception as e:
            print("QUERY ERROR:", e)
            error = "yes"

    return render(request, 'view_queries.html', {
        'contact': contact,
        'error': error
    })


def delete_query(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    contact = get_object_or_404(Contact, id=pid)
    contact.delete()
    return redirect('read_queries')


# ================= SEARCH =================
def search(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    sd = ""
    data = None
    module = None

    if request.method == "POST":
        module = request.POST.get('module')
        sd = request.POST.get('searchdata', '').strip()

        if sd:
            if module == "query":
                data = Contact.objects.filter(
                    Q(name__icontains=sd) |
                    Q(contact_no__icontains=sd) |
                    Q(email__icontains=sd) |
                    Q(subject__icontains=sd)
                ).order_by('-id')

            elif module == "booking":
                data = SiteUser.objects.filter(
                    Q(name__icontains=sd) |
                    Q(mobile__icontains=sd) |
                    Q(email__icontains=sd) |
                    Q(location__icontains=sd)
                ).order_by('-id')

    return render(request, 'search.html', {
        'sd': sd,
        'data': data,
        'module': module
    })


# ================= REPORT =================
def booking_report(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = None
    module = None
    fd = None
    td = None

    if request.method == "POST":
        module = request.POST.get('module')
        fd = request.POST.get('fromdate')
        td = request.POST.get('todate')

        if module == "booking":
            if fd and td:
                data = SiteUser.objects.filter(
                    requestdate__date__gte=fd,
                    requestdate__date__lte=td
                ).order_by('-id')
            else:
                data = SiteUser.objects.all().order_by('-id')

        elif module == "query":
            if fd and td:
                data = Contact.objects.filter(
                    messagedate__gte=fd,
                    messagedate__lte=td
                ).order_by('-id')
            else:
                data = Contact.objects.all().order_by('-id')

        elif module == "service":
            data = Services.objects.all().order_by('-id')

    return render(request, 'booking_report.html', {
        'data': data,
        'module': module,
        'fd': fd,
        'td': td
    })