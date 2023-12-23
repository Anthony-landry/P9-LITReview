from django.contrib import admin

from blog.models import Ticket, Review


# Manage admin

class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "time_created")


# Register your models here.

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
