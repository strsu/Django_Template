from django.db import models
from django.contrib.auth.hashers import check_password

from api.v1.user.models import User
from api.common.models import TimestampModel


class BoardCategory(TimestampModel):
    name = models.CharField("게시판 카테고리", max_length=32)

    class Meta:
        db_table = "board_category"
        verbose_name = "board_category"


class BoardComment(TimestampModel):
    board = models.ForeignKey(
        "board.Board",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField("삭제 비밀번호", max_length=128, null=True, blank=True)

    comment = models.TextField()
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    likes = models.ManyToManyField(User, related_name="liked_comment")

    def toggle_like(self, user):
        if user.liked_comment.filter(id=self.id):
            self.likes.remove(user)  # 이미 추천한 경우 추천 취소
        else:
            self.likes.add(user)  # 추천하지 않은 경우 추천 추가

    def check_password(self, entered_password):
        # 게시물의 해싱된 비밀번호를 가져옴
        stored_hashed_password = BoardComment.objects.get(id=self.id).password

        # 비밀번호 검증
        if check_password(entered_password, stored_hashed_password):
            # 비밀번호가 일치함
            return True

        return False

    class Meta:
        db_table = "board_comment"
        verbose_name = "board_comment"


class BoardMedia(TimestampModel):
    board = models.ForeignKey(
        "board.Board",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )

    filename = models.CharField("사진/영상 위치", max_length=256)

    def __str__(self):
        return self.filename

    class Meta:
        db_table = "board_media"
        verbose_name = "board_media"


# Create your models here.
class Board(TimestampModel):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    password = models.CharField("삭제 비밀번호", max_length=128, null=True, blank=True)

    category = models.ForeignKey(
        BoardCategory,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=128)  # 게시글 제목
    text = models.TextField("내용")

    views = models.IntegerField("조회수", default=0)
    likes = models.ManyToManyField(User, related_name="liked_board")

    is_secret = models.BooleanField("비밀글", default=False)

    def __str__(self):
        return f"{self.title}"

    def toggle_like(self, user):
        if user.liked_board.filter(id=self.id):
            self.likes.remove(user)  # 이미 추천한 경우 추천 취소
        else:
            self.likes.add(user)  # 추천하지 않은 경우 추천 추가

    def check_password(self, entered_password):
        # 게시물의 해싱된 비밀번호를 가져옴
        stored_hashed_password = Board.objects.get(id=self.id).password

        # 비밀번호 검증
        if check_password(entered_password, stored_hashed_password):
            # 비밀번호가 일치함
            return True

        return False

    class Meta:
        verbose_name = "board"
