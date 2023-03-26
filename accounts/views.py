from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from blog.models import Post

from .forms import RegistrationForm, UserEditForm, UserProfileForm
from .models import Profile
from .tokens import account_activation_token


@login_required
def favourites_list(request):
    new = Post.newmanager.filter(favourites=request.user)
    context = {"new": new}
    return render(request, "accounts/favourites.html", context)


@login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def like(request):
    if request.POST.get("action") == "post":
        result = ""
        id = int(request.POST.get("postid"))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse(
            {
                "result": result,
            }
        )


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
    else:
        return {"NotLoggedIn": User.objects.none()}


@login_required
def profile(request):
    context = {"section": "profile"}
    return render(request, "accounts/profile.html", context)


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "accounts/update.html", context)


@login_required
def delete_user(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect("accounts:login")

    return render(request, "accounts/delete.html")


def accounts_register(request):
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return HttpResponse(
                '<h1 style="margin: 2rem auto;">You have registered successfully, an activation email has been sent.</h1>'
            )
    else:
        registerForm = RegistrationForm()
    return render(request, "registration/register.html", {"form": registerForm})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("login")
    else:
        return render(request, "registration/account_activation_invalid.html")
