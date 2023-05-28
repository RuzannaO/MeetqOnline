from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
import requests
from .forms import StudentRegisterForm, TeacherRegisterForm, UserUpdateForm, StudentUpdateForm, TeacherUpdateForm
from django.contrib.auth.decorators import login_required
from courses.models import Course, CourseParticipant
from .models import Student, Teacher, Payment, Order
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
import random

class SignUpView(TemplateView):
    template_name = 'users/signup.html'


def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('profile')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, 'Thank you for joining us! Your account is in verification process. We will contact you.')
            return redirect('profile')
    else:
        form = TeacherRegisterForm()
    return render(request, 'users/register.html', {'form': form})





@login_required
def profile(request):
    if request.user.is_teacher:
        redirect_url = '/teacher/' + str(request.user.teacher.id)
        response = redirect(redirect_url)
        return response
    else:
        student_courses = CourseParticipant.objects.filter(student__user=request.user)
        return render(request, 'users/profile_student.html',{
            'student_courses': student_courses
        })


@login_required
def update_profile(request):
    if request.user.is_student:
        cur_student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = StudentUpdateForm(request.POST,
                                       request.FILES,
                                       instance=cur_student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = StudentUpdateForm(instance=cur_student)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

    else:
        cur_teacher = Teacher.objects.get(user=request.user)
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = TeacherUpdateForm(request.POST,
                                       request.FILES,
                                       instance=cur_teacher)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = TeacherUpdateForm(instance=cur_teacher)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

    return render(request, 'users/profile_update.html', context)

@login_required
def payments(request):
    if request.user.is_teacher:
        redirect_url = '/teacher/' + str(request.user.teacher.id)
        response = redirect(redirect_url)
        return response
    else:
        payments_list = Payment.objects.filter(student__user=request.user)
        not_paid = payments_list.filter(is_paid=False)
        paid_payments_list = payments_list.filter(is_paid=True)
        if 'orderId' in request.get_full_path():
            order_id = request.GET['orderId']
            response_code = request.GET['responseCode']
            if response_code == '00':
                cur_order = Order.objects.get(pk=order_id)
                cur_order.status = 'Paid'
                cur_order.save()
                order_info = get_order_information(order_id)
                customer_id = order_info['data']['list'][0]['order']['customerId']
                cur_amount = order_info['data']['list'][0]['order']['amount']
                print(confirm_order(order_id, customer_id, cur_amount))
                cur_payment = cur_order.payment
                cur_payment.is_paid = True
                cur_payment.save()
                not_paid = payments_list.filter(is_paid=False)
                return render(request, 'users/payments.html', {
                    'payments_list': paid_payments_list,
                    'not_paid_payment' : not_paid,
                    'payment_status': 'confirmed'
                })
            else:
                cur_order = Order.objects.get(pk=order_id)
                cur_order.status = 'Error'
                cur_order.save()
                return render(request, 'users/payments.html', {
                    'payments_list': paid_payments_list,
                    'not_paid_payment': not_paid,
                    'payment_status': 'error'
                })
        return render(request, 'users/payments.html',{
            'payments_list': paid_payments_list,
            'not_paid_payment': not_paid,
            'payment_status': 'default'
        })

def get_headers():
    #publicKey = "AwNDCuNhcw5sgLRUdBgUWgpnhf"
    publicKey = "ZqByLA7j8LrkWhAXSJqJRQATUz4qgbnC"
    #privateKey = "5eUzsFfTUU4bQSNA5XZjYhPSpafpLWqhQTMhvxqGYsZQHvGchw"
    privateKey = "YFuYdC45me8AdZ5wxQXjkEbyvJQNsmd3"
    key_full = privateKey + publicKey
    signature = hashlib.md5(key_full.encode('utf-8')).hexdigest()
    request_headers = {
        'content-type': 'application/json',
        'public-key': publicKey,
        'signature': signature
    }
    return request_headers

def get_link(end):
    #url_base = 'https://testpos.itfllc.am/api/bipos/test'
    url_base = 'https://paymentsystem.itfllc.am/payments/live'
    return url_base + end

def make_new_costumer(request):
    costumer_link = get_link('/customer/new')
    first_name = request.user.first_name
    last_name = request.user.last_name
    if not first_name:
        first_name = request.user.username
    if not last_name:
        last_name = 'empty'
    new_costumer_response = requests.post(costumer_link, json={
        'customerID': request.user.id,
        'firstName': first_name,
        'lastName': last_name,
        'phoneNumber': request.user.phone_number

    }, headers=get_headers())
    return new_costumer_response.json()

def make_new_order(customer_id, amount, order_id):
    order_link = get_link('/order/new')
    amount_amd = int(amount) * 490
    new_order = requests.post(order_link, json={
        "customerID": customer_id,
        'attachCard': 0,
        'amount': amount_amd,
        'orderID': order_id,
        'backURL': 'https://mandarinschool.am/payments'
    }, headers=get_headers())
    return new_order.json()

def get_all_order_ids():
    order_link = get_link('/transactions/list')
    order_info = requests.post(order_link, headers=get_headers()).json()['data']['list']
    ids = []
    for order in order_info:
        ids.append(order['order']['id'])
    return ids

def get_order_information(order_id):
    order_link = get_link('/transactions/list')
    order_info = requests.post(order_link, json={
        'orderID': order_id
    }, headers=get_headers())
    return order_info.json()

def confirm_order(order_id, customer_id, amount):
    confirm_link = get_link('/order/confirm-payment')
    order_confirm = requests.post(confirm_link, json={
        'orderID' : order_id,
        'customerID': customer_id,
        'amount' : amount
    }, headers=get_headers())
    return order_confirm.json()

@login_required
def make_order(request):
    if request.user.is_teacher:
        redirect_url = '/teacher/' + str(request.user.teacher.id)
        response = redirect(redirect_url)
        return response
    else:
        response_customer = make_new_costumer(request)
        payment_not_paid = Payment.objects.filter(student__user=request.user).filter(is_paid=False).first()

        current_ids = Order.objects.all().values_list('pk', flat=True)
        current_ids_in_itf = get_all_order_ids()
        order_id = random.randint(10000, 99999)
        while order_id in current_ids or order_id in current_ids_in_itf:
            order_id = random.randint(10000, 99999)

        while True:
            new_order = make_new_order(request.user.id, payment_not_paid.amount, order_id)
            if 'errors' in new_order['data']:
                if 'orderID' in new_order['data']['errors']:
                    order_id += 1
                else:
                    break
            else:
                break
        Order.objects.create(id=order_id, payment = payment_not_paid, itf_order_id = new_order['data']['itfOrderId'], last_massage = new_order['message'], status = new_order['status'] )
        try:
            redirect_url = new_order['data']['redirectURL']
        except:
            redirect_url = 'home'
        return redirect(redirect_url)

