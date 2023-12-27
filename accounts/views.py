from django.shortcuts import render, redirect, reverse

# contrib auth
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator

# generic views
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic import RedirectView

from accounts import forms
from django.urls import reverse_lazy

from accounts.forms import UpdateTicketForm
from accounts.models import UserFollows
from blog.models import Review, Ticket


# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        self.request.session['username'] = self.request.POST.get('email')
        form.save()
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # User already authenticated : redirect to the "flux" page
            return redirect('flux')
        return super().dispatch(*args, **kwargs)


class Login(LoginView):
    form_class = forms.UserLoginForm
    success_url = reverse_lazy('flux')
    template_name = 'accounts/login.html'
    fields = '__all__'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # User already authenticated : redirect to the "flux" page
            return redirect('flux')
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name="dispatch")
class Logout(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'flux'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(Logout, self).get_redirect_url(*args, **kwargs)


@login_required(login_url='accounts:login')
def follow_view(request):
    context = {}
    warning = ""
    user = get_user_model()

    if "username" in request.POST:
        user_followed = user.objects.filter(username=request.POST["username"])
        if len(user_followed) == 1 and \
                not UserFollows.objects.filter(followed_user_id=user_followed[0].id, user_id=request.user.id):
            if user_followed[0] != request.user:
                new_follow = UserFollows()
                new_follow.user = request.user
                new_follow.followed_user = user_followed[0]
                new_follow.save()
                # new_follow = UserFollows.objects.create(user=request.user, followed_user=user_followed[0])
            else:
                warning = "Vous ne pouvez pas vous suivre vous-même..."
        else:
            warning = "Nom d'utilisateur invalide (inexistant ou deja suivi)"

    followed_users = list(user.objects.filter(
        followed_by__in=UserFollows.objects.filter(
            user_id=request.user.id
        )
    ).exclude(is_superuser=True))

    follower = list(user.objects.filter(
        following__in=UserFollows.objects.filter(
            followed_user=request.user.id
        )).exclude(is_superuser=True))

    context["followed_users"] = followed_users
    context["follower"] = follower
    context["warning"] = warning

    return render(request, "accounts/abo.html", context=context)


@login_required(login_url='accounts:login')
def unfollow_view(request, id):
    try:
        userF = UserFollows.objects.get(
            user_id=request.user.id,
            followed_user_id=id
        )
        if userF:
            userF.delete()
    finally:
        pass

    return redirect(reverse('accounts:follow'))


class ReviewList(ListView):
    model = Review
    template_name = "accounts/myposts.html"
    context_object_name = "tickets_and_reviews"

    def get_queryset(self):
        reviews = list(Review.objects.filter(user=self.request.user))  # .order_by("-time_created")
        tickets = list(Ticket.objects.filter(user=self.request.user))

        tickets_and_reviews = sorted(
            tickets + reviews,
            key=lambda item: item.time_created,
            reverse=True
        )

        return tickets_and_reviews


def delete_post(request, id):
    post = Review.objects.get(id=id)
    post.delete()
    return redirect('accounts:posts')


def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.delete()
    return redirect('accounts:posts')


# class PostUpdate(UpdateView):
#     model = Review
#     template_name = "accounts/modifymyposte.html"
#     context_object_name = "post"
#     fields = ["headline", "rating", "body"]

def update_post(request, pk):
    post = Review.objects.get(pk=pk)

    if request.method == "POST":
        updated_title = request.POST.get("title")
        updated_body = request.POST.get("body")
        rating = request.POST.get("rating")

        updated_fields = {
            "headline": updated_title,
            "body": updated_body,
            "rating": rating,
        }

        # Works only for queryset
        Review.objects.filter(pk=pk).update(**updated_fields)

        return redirect('accounts:posts')

    return render(request, 'accounts/modifymypost.html', context={"post": post})


class TicketUpdate(UpdateView):
    model = Ticket
    template_name = "accounts/modifymyticket.html"
    context_object_name = "ticket"
    form_class = UpdateTicketForm
    success_url = reverse_lazy('flux')
