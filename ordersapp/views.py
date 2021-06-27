from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from ordersapp.models import Order


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    pass


class OrderRead(DetailView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DeleteView):
    pass


def forming_complete(request, pk):
    pass