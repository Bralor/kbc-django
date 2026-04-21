from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from blog.models import Blog
from blog.validators import validate_no_spam_words, MinWordCountValidator


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        min_length=3,
        widget=forms.Textarea,
        validators=[validate_no_spam_words],  # reusable validator
    )


class BlogReviewForm(forms.Form):
    blog = forms.ModelChoiceField(queryset=Blog.objects.all())
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '')

        # rating may be absent if it failed its own validation
        rating = self.cleaned_data.get('rating')

        if rating is not None and rating < 2 and not comment:
            raise ValidationError(
                "Please explain your low rating — comment is required for ratings of 1 or 2."
            )

        return comment


# class BlogCreateForm(forms.Form):
#     title = forms.CharField(max_length=200)
#     author = forms.CharField(max_length=100, validators=[
#         RegexValidator(
#             regex=r'^[a-zA-Z]+$',
#             message='Author can only contain letters.',
#         )
#     ])
#     author_email = forms.EmailField(required=False)
#     published_date = forms.DateField()
#     category_type = forms.ChoiceField(choices=CategoryType.choices)


class BlogModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea,
        validators=[MinWordCountValidator(min_words=3)],  # reusable validator
    )
    class Meta:
        model = Blog
        fields = ['title', 'author', 'author_email', 'content', 'published_date', 'category_type']

    def clean(self):
        """Validate date logic across fields."""
        cleaned_data = super().clean()
        published_date = cleaned_data.get('published_date')

        if published_date:
            today = date.today()

            days_ahead = (published_date - today).days
            if days_ahead > 1:
                raise ValidationError(
                    f"Published date is {days_ahead} days in the future — "
                    "Published date cannot be in the future."
                )

            days_old = (date.today() - published_date).days
            if days_old > 365:
                self.add_error(
                    'published_date',
                    f"Published date is {days_old} days in the past — cannot be older than 1 year."
                )
        return cleaned_data

    def clean_author(self):
        # value has already passed the basic field validation
        author = self.cleaned_data['author']  

        # Disallow reserved/system account names
        forbidden = ['admin', 'root']
        if author.lower() in forbidden:
            raise ValidationError(f"The name '{author}' is reserved and not allowed.")

        return author.lower()


class BlogSearchForm(forms.Form):
    SORT_CHOICES = [
        ('title', 'Title'),
        ('author', 'Author'),
        ('published_date', 'Published date'),
    ]

    q = forms.CharField(
        required=False,
        label='Search by title',
        help_text='Case-insensitive search over Blog.title',
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        initial='title',
        label='Sort by',
    )