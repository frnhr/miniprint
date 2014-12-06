from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        u = self.create_user(email, password=password)
        u.is_staff = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nick = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField('last login', null=False, editable=False)


    @property
    def is_superuser(self):
        return self.is_staff

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.nick or self.email

    def get_full_name(self):
        return self.get_short_name()

    def save(self, *args, **kwargs):
        if not self.date_joined:
            self.date_joined = timezone.now()
        if self.nick == '':
            self.nick = None
        return super(User, self).save(*args, **kwargs)


class Company(models.Model):
    user = models.OneToOneField(User, related_name='company')
    name = models.CharField(max_length=500)
