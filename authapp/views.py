from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import auth


from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from basketapp.models import Basket
# Create your views here.
from geekshop.settings import DEBUG


# делаем отключение csrf token, чтобы siege смог бы подключиться
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'authapp/login.html', context)



class RegisterCreateView(SuccessMessageMixin, CreateView):
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:profile')
    success_message = 'Вы успешно зарегистрировались!'

    def get_context_data(self, **kwargs):
        context = super(RegisterCreateView, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - Регистрация'})
        return context

    # срабатывание отправки письма при реализации CBV, обязательно возвращаем HttpResponse
    def form_valid(self, form):
        super(RegisterCreateView, self).form_valid(form)
        user = form.save()
        send_verify_link(user)
        return HttpResponseRedirect(reverse('users:login'))


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(data=request.POST)
#
#         if form.is_valid() and form.clean_first_name():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             # Выводит ошибки по которым форма не проходит валидацию:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    # Первый способ:
    baskets = Basket.objects.filter(user=request.user)
    # total_quantity = 0
    # total_sum = 0
    # for basket in baskets:
    #     total_quantity += basket.quantity
    #     total_sum += basket.sum()

    # второй способ:
    # total_quantity = sum(basket.quantity for basket in baskets)
    # total_sum = sum(basket.sum() for basket in baskets)

    context = {
        'title': 'GeekShop- Личный кабинет',
        'form': form,
        'baskets': baskets,
        # Третий способ:
        # 'total_quantity': sum(basket.quantity for basket in baskets),
        # 'total_sum': sum(basket.sum() for basket in baskets),
        'profile_form': profile_form,
    }
    return render(request, 'authapp/profile.html', context)


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    print(user.activation_key, verify_link)
    subject = 'Account verify'
    message = f'Your link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)  # user автоматически авторизуется
    return render(request, 'authapp/verify.html')
