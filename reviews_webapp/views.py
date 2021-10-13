from django.shortcuts import redirect, render
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


class SubscriptionPageView(LoginRequiredMixin, View):
    """View for subscription page. Requires to be logged in."""
    template_name = "reviews_webapp/subscriptions.html"
    sub_form = SubscriptionForm()
    subscriptions = [relationship_object for relationship_object in UserFollows.objects.filter(user=User.objects.get(pk=1))]
    followers = [relationship_object.user for relationship_object in UserFollows.objects.filter(followed_user=User.objects.get(pk=1))]

    def get(self, request):
        context = {
            "form": self.sub_form,
            "subscriptions": self.subscriptions,
            "subscribers": self.followers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        loggedin_username = request.user
        loggedin_user = User.objects.filter(username=loggedin_username)[0]

        if (request.POST.get("username")):
            added_username = request.POST["username"]

            # TODO verify form is valid 
            # AKA user exists and relationship doesnt't exist
            print(self.sub_form.is_valid())

            if len(User.objects.filter(username=added_username)) == 1 and added_username != loggedin_user:
                new_relationship = UserFollows(user=loggedin_user, followed_user=User.objects.filter(username=added_username)[0])
                new_relationship.save()
            
        elif (request.POST.get("unsubscribe_id")):
            id_to_remove = request.POST["unsubscribe_id"]
            relationship_to_delete = UserFollows.objects.get(pk=id_to_remove)
            relationship_to_delete.delete()

        context = {
            "form": SubscriptionForm(request.POST),
            "subscriptions": [relationship_object for relationship_object in UserFollows.objects.filter(user=User.objects.get(pk=1))],
            "subscribers": self.followers,
        }
        return render(request, self.template_name, context)