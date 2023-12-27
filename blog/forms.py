from blog.models import Ticket, Review

from django.forms import ModelForm, IntegerField

from django_starfield import Stars


class NewTicketForm(ModelForm):
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        fields = ('title', 'description', 'image')
        model = Ticket

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Titre'
        self.fields['title'].required = True
        self.fields['description'].required = True

    # def save(self, commit=True):
    #     if not self.cleaned_data.get('image'): #
    #         path = os.path.join(settings.STATIC_ROOT, "img/default_image.png")
    #         default_file = open(path, 'rb')
    #         self.default_django_file = File(default_file, name="image.png")
    #         self.instance.image = self.default_django_file
    #         # self.instance.image._committed = True
    #     super().save(commit)
    #     return self.instance


class NewReviewForm(ModelForm):
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        fields = ('headline', 'rating', 'body')
        model = Review

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['headline'].label = 'Titre'
        self.fields['headline'].required = True
        self.fields['rating'] = IntegerField(widget=Stars)
        self.fields['rating'].label = 'Note'
        self.fields['rating'].required = True
        self.fields['body'].label = 'Description'
        self.fields['body'].required = True
