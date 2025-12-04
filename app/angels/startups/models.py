from django.db import models
from django_countries.fields import CountryField

class Finanace(models.Choices):
    Equity = 'Equity'
    Convertible_Notes = 'Convertible Notes'
    SAFE = 'SAFE'
    Loan = 'Loan'
    Other = 'Other'
    Undecided = 'Undecided'
    Not_Interested_In_Funding = 'Not Interested In Funding' 

class StartupForm(models.Model):
    #apply form 1
    startup_name = models.CharField(null=False)
    startup_logo = models.ImageField(upload_to='logos/',null=False)
    one_liner = models.CharField(max_length=255,null=False)
    startup_website = models.URLField(null=False)
    startup_email = models.EmailField(null=False)
    registered_city = models.CharField(max_length=100,null=False)
    registered_date = models.DateField(null=False)
    registered_country = models.CharField(max_length=100,null=False)
    startup_stage = models.CharField(max_length=50,null=False)
    industry = models.CharField(max_length=50,null=False)
    startup_video = models.FileField(upload_to='videos/',null=False)

    #details form
    startup_problem_statement = models.TextField(null=False)
    startup_solutions = models.TextField(null=False)
    startup_market_opportunity = models.TextField(null=False)
    business_model = models.TextField(null=False)
    
    #apply form 3
    finance = models.CharField(max_length=50, choices=Finanace.choices, null=False)
    capital_seeking_min = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    capital_seeking_max = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    startup_strategy = models.TextField(null=False)
    others = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class StartupTeamMember(models.Model):
    startup = models.ForeignKey(StartupForm, related_name='team_members', on_delete=models.CASCADE)
    email = models.EmailField(null=False)
    name = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    linkedin_profile = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=100, null=False)
    is_founder = models.BooleanField(default=False)
    experience = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class AuthUsers(models.Model):
    member_name = models.CharField(max_length=100, null=False)
    member_surname = models.CharField(max_length=100, null=False)
    member_email = models.EmailField(null=False)
    member_phone = models.CharField(max_length=15, null=False)
    member_role = models.CharField(max_length=50, null=False)    #1 admin 2 user
    member_password = models.CharField(max_length=100, null=False)


