from django.shortcuts import render, redirect, reverse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

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

    warning = ""
    user = get_user_model()

    try:
        if "username" in request.POST:
            if request.user.username != request.POST["username"]:
                user_followed = user.objects.get(username=request.POST["username"])
                if UserFollows.objects.filter(followed_user=user_followed, user=request.user).exists():
                    warning = "Vous suivez déjà cet utilisateur."
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_followed)
            else:
                warning = "Vous ne pouvez pas vous suivre vous-même..."
        else:
            warning = "Pas de nom d'utilisateur saisie"
    except ObjectDoesNotExist:
        warning = "Nom d'utilisateur invalide."
    except MultipleObjectsReturned:
        warning = "Plusieurs utilisateurs trouvés avec ce nom d'utilisateur."

    # Récupération des utilisateurs suivis et des abonnés
    followed_users = user.objects.filter(
        followed_by__user=request.user
    ).exclude(is_superuser=True).distinct()

    followers = user.objects.filter(
        following__followed_user=request.user
    ).exclude(is_superuser=True).distinct()

    context = {
        "followed_users": followed_users,
        "follower": followers,
        "warning": warning
    }

    return render(request, "accounts/abo.html", context=context)


@login_required(login_url='accounts:login')
def unfollow_view(request, id):
    userF = UserFollows.objects.get(
        user_id=request.user.id,
        followed_user_id=id
    )
    if userF:
        userF.delete()

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
    if post.user != request.user:
        return redirect('flux')
        # return HttpResponse('Unauthorized', status=401)

    post.delete()
    return redirect('accounts:posts')


def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if ticket.user != request.user:
        return redirect('flux')
        # return HttpResponse('Unauthorized', status=401)

    ticket.delete()
    return redirect('accounts:posts')


# class PostUpdate(UpdateView):
#     model = Review
#     template_name = "accounts/modifymyposte.html"
#     context_object_name = "post"
#     fields = ["headline", "rating", "body"]

def update_post(request, pk):
    post = Review.objects.get(pk=pk)

    if post.user != request.user:
        return redirect('flux')
        # return HttpResponse('Unauthorized', status=401)

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
