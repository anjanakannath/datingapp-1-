from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, UserForm, AddressUpsertForm
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView
from .models import Address

# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Correct usage of login
                return redirect('/')

        return render(request, 'accounts/login.html', {'form': form})



def logout_user(request):
    """
    Logs out the current user and returns a success message.

    Args:
        request (HttpRequest): The current HTTP request.

    Returns:
        HttpResponse: A success message indicating that the user has been logged out.
    """
    logout(request)
    return redirect('/')


class ProfileView(TemplateView):
    template_name = 'accounts/profile_view.html'

class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'Dating/address_list.html'
    # queryset = Address.objects.filter(user=1)

    def get_queryset(self):
        # return Address.objects.filter(user=self.request.user)
        return super(AddressListView, self).get_queryset().filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressUpsertForm
    template_name = 'accounts/address_upsert.html'
    success_url = reverse_lazy('accounts:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddressCreateView, self).form_valid(form)
    

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressUpsertForm
    template_name = 'accounts/address_upsert.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        address = get_object_or_404(Address, id=id, user=self.request.user)
        address.delete()
        return redirect('accounts:address_list')
    

def signup(request):
    return render(request, 'accounts/signup.html')


def registersec1(request):
    return render(request, 'accounts/registersec1.html')


def registersec2(request):
    return render(request, 'accounts/registersec2.html')


def registersec3(request):
    return render(request, 'accounts/registersec3.html')


def datingapp(request):
    return render(request, 'accounts/datingapp.html')

def home(request):
    return render(request, 'accounts/home.html.html')

