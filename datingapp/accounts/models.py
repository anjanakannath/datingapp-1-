from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    country_code = models.CharField(max_length=3)



class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    SMOKE = (
        ('N','No'),
        ('Y','Yes'),
        ('P','Plan to Quit')
    )
    
    DRINKING = (
        ('T','Yes'),
        ('F','No'),
        ('P','Plan to Quit'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    dob = models.DateField(blank=True, null=True)
    smoke = models.CharField(max_length=1,choices=SMOKE,default='N')
    drinking = models.CharField(max_length=1,choices=DRINKING,default='T')
    hobbies = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)


class Photo(models.Model):
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.BooleanField(default=False)  

    def __str__(self):
        return f"Photo {self.id}"
    
class User(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class Photo(models.Model):
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id}"

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self) -> str:
        return self.full_name
    
    @property
    def age(self):
        if self.dob:
            return (datetime.date.today() - self.dob).days // 365
        return None


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=250)
    address_line_2 = models.CharField(max_length=250)
    address_line_3 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self) -> str:
        return f'''
            {self.address_line_1}
            {self.address_line_2}
            {self.address_line_3}
            {self.city}
            {self.state}
            {self.country}
        '''
class EmployeeEmployer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

class JobSeeker(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_field = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.job_field}"
    

class RelationshipType(models.Model):
    SHORT_TERM = 'short_term'
    LONG_TERM = 'long_term'
    RELATIONSHIP_CHOICES = [
        (SHORT_TERM, 'Short Term Relationship'),
        (LONG_TERM, 'Long Term Relationship'),
    ]

    name = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, unique=True)

    def __str__(self):
        return dict(self.RELATIONSHIP_CHOICES)[self.name]
    

    
class UserPreference(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('both', 'Both'),
    ]
    
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    
    def __str__(self):
        return self.get_gender_display()
    

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/')
    qualification = models.CharField(max_length=200)
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    interests = models.CharField(max_length=200)
    hobbies = models.CharField(max_length=200)
    job = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/')
    
    def __str__(self):
        return self.name
class MessageRequest(models.Model):
    username = models.CharField(max_length=50)

class Conversation(models.Model):
    username = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled'),
    ]

    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} ({self.status})'

    class Meta:
        unique_together = ('sender', 'receiver')
