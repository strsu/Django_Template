from django.db import models
from api.v1.user.models import User


# Create your models here.
class LogModel(models.Model):
    memo = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField("생성일", auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField("삭제일", blank=True, null=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    genre = models.CharField(max_length=16, unique=True)

    class Meta:
        ordering = ["genre"]


class Nation(models.Model):
    nation = models.CharField(max_length=16, unique=True)

    class Meta:
        pass


class MovieRateType(models.Model):
    rate_type = models.CharField(max_length=16, unique=True)

    class Meta:
        pass


class ActorRateType(models.Model):
    rate_type = models.CharField(max_length=16, unique=True)

    class Meta:
        pass


class Movie(LogModel):
    title = models.CharField(max_length=64)
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

    class Meta:
        pass


class Actor(LogModel):
    name = models.CharField(max_length=64)
    birth = models.DateField("생년월일", blank=True, null=True)

    height = models.FloatField("키", blank=True, null=True)

    movie = models.ManyToManyField(Movie, related_name="attend_movie")

    class Meta:
        pass


class MovieRating(models.Model):
    user = models.ForeignKey(
        User,
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

    class Meta:
        unique_together = [["user", "movie", "rate_type"]]


class ActorRating(models.Model):
    user = models.ForeignKey(
        User,
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
