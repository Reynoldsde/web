from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User, PermissionsMixin, Permission
from products.models import Task

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, passowrd=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(passowrd)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            passowrd=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class vip_plans(models.Model):
    plan_name = models.CharField(max_length=255, null=True, blank=True)
    sets_per_day = models.IntegerField(null=True, blank=True)
    profit_per_submission = models.FloatField(null=True, blank=True)
    account_minimum_balance = models.FloatField(null=True, blank=True)\
    
    def __str__(self):
        return self.plan_name

class account(AbstractBaseUser):
    profile_picture = models.ImageField(null=True, blank=True, upload_to='account_img/')
    userid = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=40, unique=False, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True,)
    groups = models.CharField(max_length=30, unique=False, blank=True, null=True,)
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, help_text=('Specific permissions for this user.'), related_name="user_set", related_query_name="user")
    email = models.EmailField(max_length=320, blank=True, null=True, unique=True, error_messages={'unique': ("A user with that email address already exists.")})
    phone = models.IntegerField(help_text='Contact phone number', default=0)
    balance = models.FloatField(null=True, blank=True, default=0)
    pending_withdraw_balance = models.FloatField(null=True, blank=True, default=0)
    total_withdrawed = models.FloatField(null=True, blank=True, default=0)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    vip_plan = models.ForeignKey(vip_plans, on_delete=models.DO_NOTHING, null=True, blank=True)
    assigned_task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, null=True, blank=True)
    show_premium_products = models.BooleanField(default=True)
    task_index = models.IntegerField(null=True, blank=True, default=0)
    encounter_negative = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=300, blank=True, null=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username']

    def __str__(self):
        return str(self.name) + " | " + str(self.email) if self.name and self.email else "Deleted"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True