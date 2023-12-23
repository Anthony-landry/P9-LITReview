from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import UserFollows

from blog.models import Ticket, Review


@login_required(login_url='accounts:login')
def flux_view(request):
    followed_users = list(UserFollows.objects.filter(user_id=request.user.id))
    followed_users__ids = [
        followed_user.followed_user_id for followed_user in followed_users
    ]
    feed_ids = followed_users__ids + [request.user.id]

    # tickets et revues des gens suivis
    tickets = list(Ticket.objects.filter(user_id__in=feed_ids))
    reviews = list(Review.objects.filter(user_id__in=feed_ids))

    # tickets et revues de l'utilisateur
    user_reviews = list(Review.objects.filter(user_id=request.user.id))
    user_reviews__ticket_ids = [
        user_review.ticket_id for user_review in user_reviews
    ]
    tickets_and_reviews = sorted(
        tickets + reviews,
        key=lambda item: item.time_created,
        reverse=True
    )

    context = {
        "tickets_and_reviews": tickets_and_reviews,
        "user_reviews__ticket_ids": user_reviews__ticket_ids
    }
    return render(request, 'litreview/flux.html', context=context)

@login_required(login_url='accounts:login')
def index(request):
    return redirect("flux")