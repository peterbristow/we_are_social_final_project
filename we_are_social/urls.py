"""we_are_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

PJB Note:
Importing "views" from more than one app,
will get a collision unless using aliases with "as".
Use "name" to avoid hard coding urls on code or inside templates.
E.g. reverse('index').
"""

from django.conf.urls import url, include
from django.contrib import admin
from .settings import MEDIA_ROOT
from paypal.standard.ipn import urls as paypal_urls
from paypal_store import views as paypal_views
from accounts import views as accounts_views  # aliases: see above note
from home import views as home_views
from products import views as product_views
from magazines import views as magazine_views
from threads import views as forum_views
from reusable_blog_v1 import urls as reusable_blog_v1_urls
from polls import api_views as poll_api_views
from threads import api_views as thread_api_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    url(r'^$', home_views.get_index, name='index'),

    # Auth URLs
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),

    # Stripe URLs
    url(r'^cancel_subscription/$', accounts_views.cancel_subscription, name='cancel_subscription'),
    url(r'^subscriptions_webhook/$', accounts_views.subscriptions_webhook, name='subscriptions_webhook'),

    # Paypal URLs
    url(r'^a-very-hard-to-guess-url/', include(paypal_urls)),
    url(r'^paypal-return/$', paypal_views.paypal_return),
    url(r'^paypal-cancel/$', paypal_views.paypal_cancel),
    url(r'^products/$', product_views.all_products, name='products'),
    url(r'^magazines/$', magazine_views.all_magazines, name='magazines'),

    # Blog URLs
    url(r'^blog/', include(reusable_blog_v1_urls)),

    # Forum URLs
    url(r'^forum/$', forum_views.forum),
    url(r'^threads/(?P<subject_id>\d+)/$', forum_views.threads, name='threads'),
    url(r'^new_thread/(?P<subject_id>\d+)/$', forum_views.new_thread, name='new_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', forum_views.thread, name='thread'),
    url(r'^post/new/(?P<thread_id>\d+)/$', forum_views.new_post, name='new_post'),
    url(r'^post/edit/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', forum_views.edit_post, name='edit_post'),
    url(r'^post/delete/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^thread/vote/(?P<thread_id>\d+)/(?P<subject_id>\d+)/$', forum_views.thread_vote, name='cast_vote'),

    # REST URLs
    url(r'^threads/polls/$', poll_api_views.PollViewSet.as_view()),  # visit to get a full list of Polls in JSON format.
    # we add on a parameter, pk, which is our primary key for the model. Our
    # RetrieveAPIView will use this to do the filtering.
    url(r'^threads/polls/(?P<pk>[\d]+)$', poll_api_views.PollInstanceView.as_view(), name='poll-instance'),
    url(r'^threads/polls/vote/(?P<thread_id>\d+)/$', poll_api_views.VoteCreateView.as_view(), name='create_vote'),

    url(r'^threads/$', thread_api_views.ThreadViewSet.as_view()),
    url(r'^post/update/(?P<pk>[\d+]+)/$', thread_api_views.PostUpdateView.as_view(),
        name="update-poll"),
    url(r'^post/delete/(?P<pk>[\d]+)/$', thread_api_views.PostDeleteView.as_view(), name='delete-poll'),

]
