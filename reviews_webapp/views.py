from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TicketForm, SubscriptionForm
from .models import UserFollows
from authentication.models import User
from reviews_webapp.models import Ticket

class FeedPageView(LoginRequiredMixin, View):
    
    def get(self, request):
        username = request.user
        user_id = request.user.id
        subscriptions = [user.followed_user.id for user in UserFollows.objects.filter(user=1)]
        subscriptions.append(user_id)
        tickets = Ticket.objects.filter(user__id__in=subscriptions).order_by('-time_created')

        context = {
            "user": username,
            "posts": tickets,
        }
        return render(request, 'reviews_webapp/feed.html', context)

    def post(self, request):
        delete_post(request)
        return self.get(request)


class PostsPageView(LoginRequiredMixin, View):
    template_name = "reviews_webapp/my_posts.html"

    def get(self, request):
        username = request.user
        user_id = request.user.id

        context = {
            "user": username,
            "posts": Ticket.objects.filter(user__id=user_id).order_by('-time_created'),
        }
        return render(request, self.template_name, context)


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


class TicketPageView(LoginRequiredMixin, View):
    """A view to create or update tickets."""
    template = 'reviews_webapp/ticket.html'

    def get(self, request, ticket_id):
        if ticket_id == "new":
            context = {
                'title': "Créer un ticket",
                'form': TicketForm()
            }
            return render(request, self.template, context)
        else:
            ticket = Ticket.objects.get(pk=ticket_id)
            context = {
                "title": "Modifier un ticket",
                'form': TicketForm(
                    initial={
                        'title': ticket.title,
                        'description': ticket.description,
                        'image': ticket.image,
                        })
            }
            return render(request, self.template, context)

    def post(self, request, ticket_id):
        if ticket_id == "new":
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                # TODO gérer l'ajout d'une image dans un ticket
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('posts')
        else:
            ticket = Ticket.objects.get(pk=ticket_id)
            form = TicketForm(request.POST, request.FILES, instance = ticket)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.save()
            return self.get(request, ticket_id)

def delete_post(request):
    id_to_delete = request.POST["post_id"]
    ticket_to_delete = Ticket.objects.get(pk=id_to_delete)
    ticket_to_delete.delete()