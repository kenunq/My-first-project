from typing import Callable

from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.forms import BooleanField, CheckboxInput
from django.template import loader
from django_recaptcha import widgets
from django_recaptcha.fields import ReCaptchaField

from mysite.celery import app as celery_app
from user.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "input-login"}))

    password1 = forms.CharField(widget=forms.PasswordInput({"id": "input-password", "autocomplete": "new-password"}))
    password2 = forms.CharField(widget=forms.PasswordInput({"id": "input-repeat-password"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"id": "input-email"}))
    captcha = ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
                "id": "RecaptchaField1",
                "data-callback": "verifyCallback",
                "style": "margin: 0px 25px 26px 25px;",
            }
        )
    )
    terms_of_use = BooleanField(widget=CheckboxInput())

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email",
            "captcha",
            "terms_of_use",
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        return user

    def clean_email(self) -> str:
        new_email = self.cleaned_data.get("email", False)

        if new_email:
            if User.objects.filter(email=new_email).exists():
                raise ValidationError("Такой почтовый адрес уже существует.")
            return new_email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "input-login"}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            {
                "id": "input-password",
                "readonly": None,
                "onfocus": "this.removeAttribute('readonly')",
            }
        )
    )

    remember_me = BooleanField(required=False, widget=CheckboxInput())

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")


def password_reset_send_mail_override(func: Callable) -> Callable:
    def wrap(*args, **kwargs):
        args = list(args)

        args[0] = "PasswordResetCustomForm"
        args[3]["username"] = args[3]["user"].get_username()
        args[4] = settings.EMAIL_HOST_USER
        del args[3]["user"]
        func.delay(*args, **kwargs)

    return wrap


class PasswordResetCustomForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["id"] = "forgot_pass_input"
        self.fields["email"].widget.attrs["onfocus"] = 'this.removeAttribute("readonly")'
        self.fields["email"].label = ""

    class Meta:
        fields = ("email",)

    @password_reset_send_mail_override
    @celery_app.task
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        context.update({"btn_name": subject.rsplit(" ", 2)[0]})

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def clean_email(self) -> str:
        new_email = self.cleaned_data.get("email", False)

        if new_email:
            if not User.objects.filter(email=new_email).exists():
                raise ValidationError("Указанная электронная почта не привязана ни к одному аккаунту.")

            return new_email


class PasswordResetConfirmForm(SetPasswordForm):
    """#### Форма для страницы ввода нового пароля."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["class"] = "new_password1_input"
        self.fields["new_password2"].widget.attrs["class"] = "new_password2_input"

    class Meta:
        fields = ("new_password1", "new_password2")


class PasswordChangeForm(PasswordChangeForm):
    """#### Форма для изменения пароля."""

    old_password = forms.CharField(
        widget=forms.PasswordInput({"id": "old_password_input", "autocomplete": "new-password"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["id"] = "new_password_input"
        self.fields["new_password2"].widget.attrs["id"] = "confirm_new_password_input"

    class Meta:
        fields = ("old_password", "new_password1", "new_password2")
