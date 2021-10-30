from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings
from django.views.generic import View

from . import forms


class SignupPageView(View):
    template_name = "authentication/signup.html"
    form = forms.SignupForm()

    def get(self, request):
        return render(request, self.template_name, {"form": self.form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {"form": form})
