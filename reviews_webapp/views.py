from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value
from django.db import IntegrityError
from itertools import chain

from .forms import TicketForm, SubscriptionForm, ReviewForm, DeleteForm
from .models import UserFollows, Ticket, Review
from authentication.models import User


class FeedPageView(LoginRequiredMixin, View):

    def get(self, request):
        # username = request.user
        user_id = request.user.id
        subscriptions = [user.followed_user.id for user in UserFollows.objects.filter(user=user_id)]
        subscriptions.append(user_id)

        context = {
            # "user": username,
            "posts": get_posts(subscriptions),
        }
        return render(request, 'reviews_webapp/feed.html', context)


class PostsPageView(LoginRequiredMixin, View):
    template_name = "reviews_webapp/my_posts.html"

    def get(self, request):
        username = request.user
        user_id = request.user.id

        context = {
            "user": username,
            "posts": get_posts([user_id], owned_only=True),
            "deletereview_form": DeleteForm(),
            "deleteticket_form": DeleteForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if (request.POST.get("delete_form")):
            delete_form = DeleteForm(request.POST)
            if delete_form.is_valid():
                if 'ticket_id' in request.POST:
                    post_id = request.POST['ticket_id']
                    ticket = Ticket.objects.get(pk=post_id)
                    ticket.delete()
                elif 'review_id' in request.POST:
                    post_id = request.POST['review_id']
                    review = Review.objects.get(pk=post_id)
                    review.delete()
        return self.get(request)


class SubscriptionPageView(LoginRequiredMixin, View):
    """View for subscription page. Requires to be logged in."""
    template_name = "reviews_webapp/subscriptions.html"
    sub_form = SubscriptionForm()

    def get(self, request, error_message=""):
        logged_in_user = request.user
        # subscriptions = UserFollows.objects.filter(user=logged_in_user).order_by('id')
        subscriptions = logged_in_user.following.all().order_by('id')
        # followers = UserFollows.objects.filter(followed_user=User.objects.get(pk=user_id)).order_by('id')
        followers = logged_in_user.followed_by.all()

        context = {
            "form": self.sub_form,
            "subscriptions": subscriptions,
            "subscribers": followers,
        }
        if error_message != "":
            context["error_message"] = error_message
        return render(request, self.template_name, context)

    def post(self, request):
        loggedin_user = request.user

        if (request.POST.get("username")):
            subscription_form = SubscriptionForm(request.POST)

            if subscription_form.is_valid():
                added_user = request.POST["username"]
                try:
                    new_subscription = User.objects.get(username=added_user)
                    if added_user != loggedin_user.username:
                        new_relationship = UserFollows(user=loggedin_user, followed_user=new_subscription)
                        new_relationship.save()
                    else:
                        return self.get(request, error_message="C'est vous ! ;)")
                except IntegrityError:
                    return self.get(request, error_message=f"{added_user} déjà suivi.e !")
                except User.DoesNotExist:
                    return self.get(request, error_message=f"Utilisateur '{added_user}' inconnu ! ")
                except Exception as exception:
                    raise(exception)
        elif request.POST.get("unsubscribe_id"):
            # id_to_remove = DeleteForm(request.POST)
            id_to_remove = request.POST["unsubscribe_id"]
            relationship_to_delete = UserFollows.objects.get(pk=id_to_remove)
            relationship_to_delete.delete()

        return self.get(request)


class TicketPageView(LoginRequiredMixin, DetailView):
    """A view to create or update tickets."""
    template = 'reviews_webapp/post_details.html'

    def get(self, request, ticket_id):
        if ticket_id == "0":
            context = {
                'title': "Créer un ticket",
                'ticket_form': TicketForm(),
            }
        else:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            if ticket.user == request.user:
                context = {
                    "title": "Modifier un ticket",
                    'ticket_form': TicketForm(instance=ticket),
                }
            else:
                context = {
                    'read_only': False if ticket.user == request.user else True,
                    'ticket': ticket,
                }
        return render(request, self.template, context)

    def post(self, request, ticket_id):
        if ticket_id == "0":
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
        else:
            ticket = Ticket.objects.get(pk=ticket_id)
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.save()
        return redirect('posts')


class ReviewPageView(LoginRequiredMixin, DetailView):
    """A view to create or update tickets."""
    template = 'reviews_webapp/post_details.html'

    def get(self, request, ticket_id):
        if ticket_id == '0':
            context = {
                'title': "Créer une critique",
                'ticket_form': TicketForm(),
                'review_form': ReviewForm(),
            }
            print(request.path_info)
            return render(request, self.template, context)
        else:
            ticket = Ticket.objects.get(pk=ticket_id)
            review = Review.objects.filter(ticket__id=ticket_id)
            if review:
                context = {
                    'title': "Ecrire une critique",
                    'ticket': ticket,
                    'review_form': ReviewForm(instance=review[0]),
                }
                return render(request, self.template, context)
            else:
                context = {
                    "title": "Modifier une critique",
                    'ticket': ticket,
                    'review_form': ReviewForm()
                }
                return render(request, self.template, context)

    def post(self, request, ticket_id):
        if ticket_id == '0':
            ticket_form = TicketForm(request.POST, request.FILES)
            review_form = ReviewForm(request.POST)
            print('Ticket validation', ticket_form.is_valid())
            print('Review validation', review_form.is_valid())
            if ticket_form.is_valid() and review_form.is_valid():
                print('\n\nCA RENTRE DANS CE CAS ?')
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
            return redirect('posts')
        else:
            review = Review.objects.filter(ticket__id=ticket_id)
            if review:
                form = ReviewForm(request.POST, instance=review[0])
                if form.is_valid():
                    review = form.save(commit=True)
                else:
                    return self.get(request, ticket_id)
            else:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.ticket = Ticket.objects.get(pk=ticket_id)
                    review.save()
            return redirect('posts')


def page_not_found_view(request, *args, **kwargs):
    return render(request, "reviews_webapp/404.html", {})


def get_posts(users_to_display, owned_only=False):
    tickets = Ticket.objects.filter(user__id__in=users_to_display).order_by('-time_created')
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.filter(user__id__in=users_to_display).order_by('-time_created')
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    if not owned_only:
        tickets_ids = [ticket.id for ticket in tickets]
        # response by users which are not followed
        response_reviews = Review.objects.filter(ticket__id__in=tickets_ids).exclude(user__id__in=users_to_display)
        response_reviews = response_reviews.annotate(content_type=Value('REVIEW', CharField()))
    else:
        response_reviews = ""

    posts = sorted(
        chain(tickets, reviews, response_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return posts
