# urls.py
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),  
    path('login/', LoginView.as_view(), name='login'),
    path('profileviewuser/', ProfileView.as_view(), name='profile_viewuser'),
    path('profilevieclient/', ProfileView.as_view(), name='profile_vieclient'),


    path('address/', AddressListView.as_view(), name='address_list'),
    path('address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/update/<int:id>/', AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:id>/', AddressDeleteView.as_view(), name='address_delete'),
    path('logout/', logout_user, name='logout'),

    path('registersec1/', registersec1, name='registersec1'),  
    path('registersec2/', registersec2, name='registersec2'),  
    path('registersec3/', registersec3, name='registersec3'),  
    path('datingapp/', datingapp, name='datingapp'), 
    path('profilelist',profile_list, name='profile_list'), 
    path('messages/',messages_view, name='messages'), 
    path('friend-requests/',friend_requests, name='friend_requests'),
    path('shortlisted/',shortlisted, name='shortlisted'),
    path('shortlisted_by/',shortlisted_by, name='shortlisted_by'),
    path('contacted-profiles/',contacted_profiles, name='contacted_profiles'),





    



    
]

    
     

