from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SubscriptionForm
from .models import UserFollows
from authentication.models import User

@login_required
def home(request):
    context = {
        "user": request.user,
    }
    return render(request, 'reviews_webapp/home.html', context) 

class SubscriptionPageView(View, LoginRequiredMixin):
    template_name = "reviews_webapp/subscriptions.html"
    sub_form = SubscriptionForm()
    subscriptions = [user_object.followed_user for user_object in UserFollows.objects.filter(user=User.objects.get(pk=1))]
    followers = [user_object.user for user_object in UserFollows.objects.filter(followed_user=User.objects.get(pk=1))]

    def get(self, request):
        context = {
            "form": self.sub_form,
            "subscriptions": self.subscriptions,
            "subscribers": self.followers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # form is valid ?
        # if self.sub_form.is_existing_user():
        # subscriptions.append(request.POST['username'])
        
        context = {
            "form": SubscriptionForm(request.POST),
            "subscriptions": self.subscriptions,
            "subscribers": self.followers,
        }
        return render(request, self.template_name, context)