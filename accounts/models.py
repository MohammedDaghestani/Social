from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The users must have an email')
        email = self.normalize_email(email)
        user = self.model( email=email, first_name = first_name,last_name = last_name,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by this
    model.

    Email, first name, last name and password are required. Other fields are optional.
    """
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_('UUID'), help_text=_('uniqe id for the user'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    facebook_user_id            = models.CharField(_('facebook user id'), max_length=255, blank=True, null=True)
    facebook_user_code          = models.CharField(_('facebook code'),max_length=1000, blank=True, null=True)
    facebook_user_access_token  = models.CharField(_('facebook user access token'),max_length=1000, blank=True, null=True)
    facebook_user_name          = models.CharField(_('facebook name'), max_length=255, blank=True, null=True)
    pic_url                     = models.URLField(_('facebook profile picture'), max_length=500)

    def __str__(self):
        return self.user.get_full_name()

class FacebookApp(models.Model):
    name        = models.CharField(_('app name'), max_length=100)
    app_id      = models.CharField(_('facebook app id') ,max_length=255, primary_key=True)
    app_secret  = models.CharField(_('facebook app secret') ,max_length=255)
    redirect_url= models.CharField(_('redirect URL'), max_length=1000)
    def __str__(self) -> str:
        return self.name

class FacebookPage(models.Model):
    user_profile   = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    id             = models.CharField(_('facebook page id'), max_length=255, primary_key=True)
    name           = models.CharField(_('facebook page name'), max_length=255)
    access_token   = models.CharField(_('facebook page access token'), max_length=1000)
    pic_url        = models.URLField(_("Picture URL"), max_length=500)
    def __str__(self):
        return self.name


class AutomatePostCommentsResponse(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4, verbose_name=(_('ID')), help_text=_('Unique ID for the reply'))
    page = models.ForeignKey(FacebookPage, on_delete=models.CASCADE)
    post = models.CharField(_("post id"), max_length=255)
    words = models.JSONField(blank = True, null= True)
    response = models.CharField(max_length=500)
    private_response = models.CharField(max_length=2000, blank=True, null=True)
    # name = models.CharField(_('automate name'), max_length=255)

    def __str__(self):
        return str(self.id)

    