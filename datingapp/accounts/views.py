from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, UserForm, AddressUpsertForm
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView
from .models import Address
from .models import Profile
from .models import MessageRequest, Conversation
from .forms import MessageRequestForm, ConversationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import RegistrationForm 
from .models import UserProfile  




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
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        user = User.objects.create_user(username=name, email=email, password=mobile_number)
        user.profile.mobile_number = mobile_number
        user.save()

        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/signup.html')
    

def registersec1(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form data
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            age = form.cleaned_data['age']
            dob = form.cleaned_data['dob']
            hobbies = form.cleaned_data['hobbies']
            interests = form.cleaned_data['interests']
            qualification = form.cleaned_data['qualification']
            smoking = form.cleaned_data['smoking']
            drinking = form.cleaned_data['drinking']

            # Handle file uploads
            profile_photo = request.FILES.get('gallery')
            if profile_photo:
                fs = FileSystemStorage()
                filename = fs.save(profile_photo.name, profile_photo)
                uploaded_file_url = fs.url(filename)
                # Do something with the uploaded file URL, like saving it in the database
            
            # Save other form data to your model or perform additional processing here

            return redirect('success_page')  # Redirect to a success page or another view

    else:
        form = RegistrationForm()

    return render(request, 'accounts/registrsec1.html', {'form': form})

def registersec2(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data
            role = form.cleaned_data['role']
            company_name = form.cleaned_data.get('company_name', '')
            location = form.cleaned_data.get('location', '')
            expertise_level = form.cleaned_data.get('expertise_level', '')
            
            # Here, you can save the data to your database or perform other actions
            
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = RegistrationForm()

    return render(request, 'registrsec2.html', {'form': form})


def registersec3(request):
    if request.method == 'POST':
        relationship = request.POST.get('relationship')
        # Process the form data here, e.g., save to database or perform actions
        # For demonstration, we'll just redirect to a success page.
        return redirect('success')  # Redirect to a success page or another view
    
    return render(request, 'registersec3.html')

def datingapp(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        # Process the form data here, such as saving it to the database
        # For demonstration, we’ll just return a success message
        return HttpResponse(f"Selected Gender: {gender}")
    
    return render(request, 'accounts/datingapp.html')  


def profile_viewcilent(request, user_id):
    # Fetch the user profile based on user_id
    profile = get_object_or_404(UserProfile, id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        # Process different actions
        if action == 'message':
            # Handle sending a message
            return HttpResponse("Message sent!")
        elif action == 'send':
            # Handle sending an item or request
            return HttpResponse("Item sent!")
        elif action == 'shortlist':
            # Handle shortlisting the profile
            return HttpResponse("Profile shortlisted!")
        elif action == 'dont_show':
            # Handle hiding or ignoring the profile
            return HttpResponse("Profile hidden!")
        elif action == 'accept':
            # Handle accepting a request
            return HttpResponse("Request accepted!")
        elif action == 'friend_request':
            # Handle sending a friend request
            return HttpResponse("Friend request sent!")
    
    return render(request, 'accounts/profile_viewcilent.html', {'profile': profile})

def profile_viewuser(request, user_id):
    # Fetch the user profile based on user_id
    profile = get_object_or_404(UserProfile, id=user_id)
    
    # Render the profile page with the fetched profile data
    return render(request, 'accounts/profile_viewuser.html', {
        'profile': profile
    })

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})


def messages_view(request):
    message_requests = MessageRequest.objects.all()
    conversations = Conversation.objects.all()
    message_request_form = MessageRequestForm()
    conversation_form = ConversationForm()
    context = {
        'message_requests': message_requests,
        'conversations': conversations,
        'message_request_form': message_request_form,
        'conversation_form': conversation_form,
    }
    return render(request, 'Accounts/messages.html', context)

def handle_message_request(request):
    if request.method == 'POST':
        form = MessageRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messages_view')
    return redirect('messages_view')

def handle_conversation(request):
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messages_view')
    return redirect('messages_view')

from django.shortcuts import render
from .models import FriendRequest

def friend_requests_view(request):
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    received_requests = FriendRequest.objects.filter(receiver=request.user)
    accepted_requests = FriendRequest.objects.filter(sender=request.user, status='accepted')
    rejected_requests = FriendRequest.objects.filter(sender=request.user, status='rejected')
    canceled_requests = FriendRequest.objects.filter(sender=request.user, status='canceled')
    pending_requests = FriendRequest.objects.filter(sender=request.user, status='pending')

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'canceled_requests': canceled_requests,
        'pending_requests': pending_requests,
    }
    return render(request, 'friend_requests.html', context)

