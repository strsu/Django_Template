from django.db import models
from django.contrib.postgres.fields import ArrayField

from api.common.models import TimestampModel


class Author(models.Model):

    author = models.CharField("글쓴이", max_length=128)

    def __str__(self):
        return f"{self.author}"

    class Meta:
        db_table = "v2_author"
        verbose_name = "author"


# Create your models here.
class Board(TimestampModel):
    title = models.CharField("제목", max_length=128)  # 게시글 제목
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    date = models.DateField("업로드일")

    reading = models.IntegerField("조회수", default=0)
    recommend = models.IntegerField("추천", default=0)

    imgs = ArrayField(models.CharField(max_length=20))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "v2_board"
        verbose_name = "board"
