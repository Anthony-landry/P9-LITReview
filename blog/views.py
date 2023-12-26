from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse

# contrib auth

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# generic views
from django.views.generic import CreateView, TemplateView

from accounts.models import UserFollows
from blog.models import Ticket, Review

from typing import Optional


from blog import forms
from django.urls import reverse_lazy


class NewTicket(LoginRequiredMixin, CreateView):
    """
    review request <==> ticket
    """

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewTicketForm
    success_url = reverse_lazy('flux')
    template_name = 'blog/create_ticket.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)


class NewReviewTicket(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewForm
    success_url = reverse_lazy('flux')
    template_name = 'blog/create_review_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = Ticket.objects.get(
            pk=self.kwargs["id"]
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        review = form.save(commit=False)
        context = self.get_context_data()
        review.ticket = context["ticket"]
        review.save()
        return super().form_valid(form)


class NewReviewSolo(TemplateView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    new_ticket_form = forms.NewTicketForm
    new_review_form = forms.NewReviewForm
    success_url = reverse_lazy('flux')
    template_name = 'blog/create_review_solo.html'

    def post(self, request):
        post_data = request.POST or None
        post_files = request.FILES or None
        new_ticket_form = self.new_ticket_form(
            post_data, post_files, prefix="newticket"
        )
        new_review_form = self.new_review_form(
            post_data, prefix="newreview"
        )

        context = self.get_context_data(
            new_ticket_form=new_ticket_form,
            new_review_form=new_review_form
        )

        if new_ticket_form.is_valid() and new_review_form.is_valid():
            review_request = self.form_save(new_ticket_form)
            self.form_save(new_review_form, review_request)
            return HttpResponseRedirect(self.success_url)
        else:
            # print("errors")
            print(new_ticket_form.errors)
            print(new_review_form.errors)

        return self.render_to_response(context)

    def form_save(self, form, review_request=None) -> Optional[Ticket]:
        """
        This function returns a ticket (review_request) when it's
        called to save a ticket.
        This allows the form to be aware of it.
        Then, when the function is called to save a review, it sets the
        review's ticket member so that the "ticket_id" review foreign key
        field can be assigned later on by the model's constructor.
        """
        form.instance.user = self.request.user


        if review_request:
            review = form.save(commit=False)
            review.ticket = review_request
            review.save()
            return
        review_request = form.save()
        return review_request

    def get(self, request, *args, **kwargs):
        return self.post(request)
