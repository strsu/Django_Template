from django.db import models
from django.contrib.auth import get_user_model


class File(models.Model):

    date = models.DateTimeField("등록일", auto_now_add=True)
    path = models.TextField("파일 경로", null=True)
    name = models.TextField("파일 명", null=True)
    code = models.TextField("코드", null=True)

    class Meta:
        verbose_name = "file"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    image_ext = instance.image.file.content_type.split("/")[1]
    return "user_{0}/{1}".format(instance.user.uuid, filename)


class ImageDB(models.Model):
    """
    pillow 라이브러리가 필요하다

    image는 upload_to 경로에 저장되고, DB에는 url만 저장된다.

    upload_to
        1. 직접 path 입력하기
        2. 함수를 통해서 동적인 path 만들기
            이 방법은 사용할 instance가 model에 정의되어 있어야 한다.

    별다른 설정을 하지 않아고, s3에 잘 올라간다.
    -> storages 라이브러리가 알아서 해준다.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )
    # file will be uploaded to MEDIA_ROOT/uploads
    image = models.ImageField(upload_to=user_directory_path)

    def get_url_path(self, request):
        """
        image full url 생성방법
        request필요
            -> requst에서 header로 host를 알아와야 하기 때문에
        """
        image_url = self.image.url
        return request.build_absolute_uri(image_url)
