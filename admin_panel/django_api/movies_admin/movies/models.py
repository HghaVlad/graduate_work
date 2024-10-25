import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('Full name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    MOVIE = 'MOVIE'
    TV_SHOW = 'TV_SHOW'
    TYPE_CHOICES = [
        (MOVIE, 'Movie'),
        (TV_SHOW, 'TV Show'),
    ]
    title = models.TextField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=TYPE_CHOICES)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')
    file_path = models.FileField(_('file'), blank=True, null=True,
                                 upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Film work genre')
        verbose_name_plural = _('Film work genres')


class PersonFilmWork(UUIDMixin):
    ACTOR = 'ACTOR'
    DIRECTOR = 'DIRECTOR'
    WRITER = 'WRITER'
    TYPE_CHOICES = [
        (ACTOR, _('Actor')),
        (DIRECTOR, _('Director')),
        (WRITER, _('Writer')),
    ]
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Film work person')
        verbose_name_plural = _('Film work persons')

DEFAULT_CHOICES = (
    ('5', 'The Best'),
    ('4', 'Good'),
    ('3', 'Normal'),
    ('2', 'Bad'),
    ('1', 'The Worst'),
)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250) 
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    image = models.ImageField(upload_to='blog/posts_images/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    rating_choices = models.IntegerField(choices=DEFAULT_CHOICES)
    objects = models.Manager() 
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def calculate_average_rating():
        sum_of_raiting = 0
        count = 0
            for raiting in range(6):
                objs = Comment.objects.filter(rating_choices=raiting)
                count += objs.count()
                sum_of_raiting += objs.count() * i
            if count > 0:
                return sum_of_raiting / count
            else:
                return None

    def get_average_rating(self, max_value=None):
        total_average, post_averages = self.get_averages(max_value=max_value)
        return total_average

    def get_post_averages(self, max_value=None):
        total_average, post_averages = self.get_averages(max_value=max_value)
        return post_averages



class Comment(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('active', 'Active'),
    )
    rating_choices = DEFAULT_CHOICES
    value = models.CharField(
        max_length=20, 
        verbose_name=('Value'), 
        choices=rating_choices,
        blank=True, null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(upload_to='comments/images/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    active = models.BooleanField(default=True)
    commented = CommentedManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.value, self.post)
