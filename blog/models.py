from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.templatetags.static import static


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/',
        # default='images/default.jpeg'
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return self.image.url if self.image else static("img/default_image.png")

    def __str__(self):
        return f"Ticket | {self.title} | {self.user.username}"

    class Meta:
        ordering = ['-time_created']

    @property
    def linked_to_user_review(self):
        if Review.objects.filter(user=self.user, ticket=self):
            return True
        return False


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review | {self.headline} | {self.user.username}"

    class Meta:
        ordering = ['-time_created']
