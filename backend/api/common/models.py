from django.db import models
from django.utils import timezone

from api.common.manager import ActiveManager

from functools import wraps
from django.db import connection
import time


def measure_query_time(func):
    """
    DEBUG = True 에서만 동작한다
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 쿼리 로그 초기화
        connection.queries_log.clear()

        # 시작 시간 기록
        start_time = time.time()

        # 원래 함수 호출
        response = func(self, *args, **kwargs)

        # 끝 시간 기록
        end_time = time.time()

        # 쿼리 로그 확인 및 수행 시간 출력
        total_time = 0
        for query in connection.queries:
            print(f"SQL: {query['sql']}")
            print(f"Time: {query['time']} seconds")
            total_time += float(query["time"])

        print(f"Total queries executed: {len(connection.queries)}")
        print(f"Total time for all queries: {total_time} seconds")
        print(f"Time taken by {func.__name__}: {end_time - start_time} seconds")

        if args:
            request = args[0]
            query_param = None
            if "QUERY_STRING" in request.META.keys():
                if request.META["QUERY_STRING"]:
                    query_param = request.META["QUERY_STRING"]

            response_obj = ResponseModel.objects.create(
                uri=request.get_full_path(),
                method=request.method,
                status_code=response.status_code,
                response_time=round(end_time - request.start_time, 8),
                query_count=len(connection.queries),
                query_time=total_time,
                query_param=query_param,
            )

            response_obj.save()

        return response

    return wrapper


# Create your models here.
class TimestampModel(models.Model):
    created_at = models.DateTimeField("생성일", auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField("삭제일", blank=True, null=True)

    raw_objects = models.Manager()  # default manager
    actives = ActiveManager()
    objects = ActiveManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
        default_manager_name = "raw_objects"  # 이걸 안 쓰면 TimestampModel을 상속받은 모델에서 새로운 manager를 할당하면 obejcts를 쓸 수 없게된다.


class ResponseModel(models.Model):

    request_at = models.DateTimeField("생성일", auto_now_add=True, blank=True, null=True)

    uri = models.CharField("주소", max_length=255)
    query_param = models.TextField(null=True, blank=True)
    method = models.CharField("", max_length=10)
    status_code = models.SmallIntegerField("응답코드")
    response_time = models.FloatField("응답시간")
    query_count = models.SmallIntegerField("쿼리개수")
    query_time = models.FloatField("쿼리시간")

    class Meta:
        verbose_name = "응답"
        verbose_name_plural = "응답"
