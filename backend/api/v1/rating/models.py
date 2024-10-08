from django.db import models
from django.core.validators import FileExtensionValidator

from django.contrib.auth import get_user_model

from api.common.models import TimestampModel


class Genre(models.Model):
    content = models.CharField(max_length=16, blank=True, null=True)
    genre = models.CharField(max_length=16, unique=True, blank=True, null=True)

    def __str__(self):
        return self.genre

    class Meta:
        ordering = ["content", "genre"]


class Nation(models.Model):
    nation = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.nation

    class Meta:
        pass


class MovieRateType(models.Model):
    rate_type = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.rate_type

    class Meta:
        pass


class ActorRateType(models.Model):
    rate_type = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.rate_type

    class Meta:
        pass


class Movie(TimestampModel):
    folder = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    open = models.DateField("개봉년도", blank=True, null=True)

    nation = models.ForeignKey(
        Nation,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="movie_nation",
        verbose_name="movie_nation_id",
    )

    genre = models.ManyToManyField(Genre, related_name="movie_genre", blank=True)

    file = models.FileField(
        upload_to="./media/",
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["avi", "mp4", "wmv", "mkv", "ts", "flv", "mpeg"]
            )
        ],
    )

    def __str__(self):
        return self.title

    class Meta:
        pass


class Actor(TimestampModel):
    name = models.CharField(max_length=64)
    birth = models.DateField("생년월일", blank=True, null=True)

    height = models.FloatField("키", blank=True, null=True)

    movie = models.ManyToManyField(Movie, related_name="attend_movie")

    def __str__(self):
        return self.name

    class Meta:
        pass


class MovieRating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="movie_rate",
        verbose_name="movie id",
    )
    rate_type = models.ForeignKey(
        MovieRateType,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="movie_rate_type",
        verbose_name="movie_rate_type id",
    )
    score = models.FloatField()

    def __str__(self):
        return self.movie.title

    class Meta:
        unique_together = [["user", "movie", "rate_type"]]


class ActorRating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )
    actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="actor_rate",
        verbose_name="actor id",
    )
    rate_type = models.ForeignKey(
        ActorRateType,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="actor_rate_type",
        verbose_name="actor_rate_type id",
    )
    score = models.FloatField()

    class Meta:
        unique_together = [["user", "actor", "rate_type"]]
