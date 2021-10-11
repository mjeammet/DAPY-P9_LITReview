from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View

@login_required
def home(request):
    context = {
        "user": request.user,
    }
    return render(request, 'reviews_webapp/home.html', context)

@login_required
class SubscriptionPageView(View):
    template_name = "reviews_webapp/subscriptions.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        pass 

def subscr(request):
    template_name = "reviews_webapp/subscriptions.html"
    context = {
        "subscribed_to": ["Micheline"],
        "subscribers": ["Micheline"],
    }
    return render(request, template_name, context)