from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


class OrderList(ListView):
    pass


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