"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.feed, name='feed')
Class-based views
    1. Add an import:  from other_app.views import feed
    2. Add a URL to urlpatterns:  path('', feed.as_view(), name='feed')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import reviews_webapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('password_change', PasswordChangeView.as_view(
        template_name='authentication/password_change.html'),
        name="password_change"),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    path('feed', reviews_webapp.views.FeedPageView.as_view(), name="feed"),
    path('signup/', authentication.views.SignupPageView.as_view(), name='signup'),
    path('subscriptions/', reviews_webapp.views.SubscriptionPageView.as_view(), name='subscriptions'),
    path('posts/', reviews_webapp.views.PostsPageView.as_view(), name='posts'),
    path('ticket/<ticket_id>', reviews_webapp.views.TicketPageView.as_view(), name='ticket'),
    path('ticket/<ticket_id>/review/', reviews_webapp.views.ReviewPageView.as_view(), name='review'),
]

# handler404 = reviews_webapp.views.page_not_found_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
