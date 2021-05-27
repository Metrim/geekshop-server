from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


# # CRUD - Create, Read, Update, Delete
class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

# То же самое, но в виде функции:
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_read(request):
#     context = {'users': User.objects.all()}
#     return render(request, 'adminapp/admin-users-read.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('adminapp:admin_users_read')


# То же самое, но в виде функции:
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == "POST":
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#
#         if form.is_valid() and form.clean_first_name():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#         else:
#             # Выводит ошибки по которым форма не проходит валидацию:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, "adminapp/admin-users-create.html", context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admin_staff:admin_users_read')


# То же самое, но в виде функции:
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     selected_user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=selected_user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#
#     context = {
#         'form': form,
#         'selected_user': selected_user,
#     }
#     return render(request, "adminapp/admin-users-update-delete.html", context)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')

# То же самое, но в виде функции:
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id=user_id)
#     # Первый способ тотального удаления пользователя:
#     # user.delete()
#     # Второй способ мнимого удаления пользователя:
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
