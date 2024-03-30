import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView

from common.mixin.views import TitleMixin
from services.models import ServicesModel
from user.forms import PasswordChangeForm, PasswordResetCustomForm, UserLoginForm, UserRegistrationForm
from user.models import User
from user.tasks import send_update_email_message
from user.utils import RedirectAuthUser


class RegistrationView(TitleMixin, RedirectAuthUser, SuccessMessageMixin, CreateView):
    """Представление обрабатывающее страницу регистрации пользователя."""

    model = User
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("user:login")
    success_message = "Вы успешно зарегистрировались!"
    redirect_auth_user_url = "user:profile"
    title = "Регистрация"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Добро пожаловать {username}.")
        return redirect("home")


class TermsOfUseView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу с политикой конфиденциальности."""

    template_name = "terms_of_use.html"
    title = "Политика конфиденциальности"


class UserLoginView(TitleMixin, RedirectAuthUser, LoginView):
    """Представление обрабатывающее страницу входа в аккаунт."""

    template_name = "login.html"
    form_class = UserLoginForm
    redirect_auth_user_url = "user:profile"
    title = "Вход"

    def get_success_url(self):
        messages.success(self.request, f"Добро пожаловать {self.request.user.get_username()}.")
        return reverse_lazy("home")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """Представление обрабатывающее выход пользователя из аккаунта."""

    permission_denied_message = "Вы не авторизованы."
    raise_exception = True

    def get(self, request: ASGIRequest, *args, **kwargs):
        self.username = request.user.get_username()

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, f"До скорых встреч {self.username}")
        return reverse_lazy("home")


class UserResetPasswordView(TitleMixin, RedirectAuthUser, PasswordResetView):
    """Представление обрабатывающее страницу сброса пароля."""

    template_name = "reset_password.html"
    form_class = PasswordResetCustomForm
    email_template_name = "emails/password_reset_email.html"
    html_email_template_name = "emails/password_reset_email.html"
    redirect_auth_user_url = "user:profile"
    title = "Сброс пароля"

    def get_success_url(self):
        messages.success(self.request, "Письмо успешно отправлено.")
        return reverse_lazy("user:password_reset_confirm")

    def render_to_response(self, context, **response_kwargs):
        if self.request.COOKIES.get("reset_password"):
            messages.warning(self.request, "Пароль можно сбросить раз в 15 минут.")
            return redirect("user:login")
        return super().render_to_response(context, **response_kwargs)


class UserResetPasswordView2(RedirectAuthUser, TemplateView):
    """Представление обрабатывающее страницу успешной отправки ссылки на почту для сброса пароля"""

    template_name = "reset_password_sended.html"
    redirect_auth_user_url = "user:profile"


class PasswordResetConfirmCustomView(TitleMixin, RedirectAuthUser, PasswordResetConfirmView):
    """#### Представление обрабатывающее страницу с формой для ввода нового пароля."""

    form_class = SetPasswordForm
    redirect_auth_user_url = "user:profile"
    template_name = "password_reset_confirm.html"
    title = "Сброс пароля"

    # автоматическая аутентификация пользователя после успешного сброса пароля
    # post_reset_login = True

    def get_success_url(self):
        messages.success(self.request, "Новый пароль успешно сохранён!")
        return reverse_lazy("user:password_reset_complete")


class PasswordResetCompleteCustomView(TitleMixin, RedirectAuthUser, PasswordResetCompleteView):
    """#### Представление обрабатывающее страницу с сообщением об успешной смене пароля."""

    redirect_auth_user_url = "user:profile"

    template_name = "reset_password_complete.html"
    title = "Успех!"

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        time_delta = timedelta(minutes=15)
        response.set_cookie(
            key="reset_password",
            value=timezone.now(),
            expires=timezone.now() + time_delta,
            domain=settings.PARENT_DOMAIN,
        )
        return response


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    """Представление обрабатывающее страницу профиля пользователя."""

    template_name = "profile.html"
    login_url = reverse_lazy("user:login")
    title = "Личный кабинет"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("PasswordChangeForm-errors"):
            context["PasswordChangeFormerrors"] = json.loads(self.request.session.get("PasswordChangeForm-errors", ""))
            del self.request.session["PasswordChangeForm-errors"]
        else:
            context["PasswordChangeFormerrors"] = ""

        context["PasswordChangeForm"] = PasswordChangeForm(self.request.GET or None)
        context["user_services"] = list(reversed(ServicesModel.objects.filter(creator=self.request.user)))

        return context

    def post(self, request: ASGIRequest, *args, **kwargs):
        data: dict = json.loads(request.body)

        if data.get("update_discord"):
            user = self.request.user
            user.discord = data["update_discord"]
            user.save()
            return JsonResponse({"status": "data was successfully discrod updated"})

        if data.get("update_email"):
            user = self.request.user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            email = urlsafe_base64_encode(force_bytes(data["update_email"]))

            if User.objects.filter(email=data["update_email"]).exists():
                return JsonResponse({"status": "the specified mailing address is already in use"})

            activation_url = reverse_lazy(
                "user:confirm_email",
                kwargs={"uidb64": uid, "token": token, "email": email},
            )
            # current_site = Site.objects.get_current().domain
            current_site = "127.0.0.1:8000"
            send_update_email_message.delay(user.email, current_site, activation_url)
            return JsonResponse({"status": "email details were successfully updated"})
        return None


def profileView2(request):
    user = request.user

    if request.method == "POST":
        change_form = PasswordChangeForm(user, request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data["old_password"]
            change_form.save()
            update_session_auth_hash(request, change_form.user)
            messages.success(request, "Вы успешно изменили пароль")
            return redirect(reverse_lazy("user:profile"))
        else:
            change_form_errors = json.dumps(change_form.errors, default=str)
            request.session["PasswordChangeForm-errors"] = change_form_errors
        return redirect(reverse_lazy("user:profile"))
    return None


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token, email):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
            email = urlsafe_base64_decode(email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email = email.decode("utf-8")
            user.save()
            return redirect("user:email_confirmed")

        return redirect("user:email_confirmation_failed")


class EmailConfirmedView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу успешной смены почтового ящика"""

    template_name = "email_confirmed.html"
    title = "Успех!"


class EmailConfirmationFailedView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу не успешного сброса почтового ящика"""

    template_name = "email_confirmed_failed.html"
    title = "Упс!!"
