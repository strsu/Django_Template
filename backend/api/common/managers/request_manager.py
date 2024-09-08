from typing import Any, Optional, Dict, Type, TypeVar, Union
import requests
import time

requests.packages.urllib3.disable_warnings()  # Unverified HTTPS 경고 비활성화

T = TypeVar('T', bound='InternalAPIResponse')

class InternalAPIResponse:
    """
    * Param *
        extras: 실패했을 때 동적으로 필요한 데이터 사용하기 위함
        is_critical : 실패시 로직을 중단해야 하는지 여부

    * Usage *
        result = CustomResponse({}, True) # 성공
        result = CustomResponse.success() # 성공

        result = CustomResponse(None, False, "ddd") # 실패
        result = CustomResponse.fail("오류 메시지") # 실패
    """

    def __init__(
        self,
        data: Optional[Any] = None,
        is_success: Optional[bool] = None,
        msg: Optional[str] = None,
        extras: Optional[Dict[str, Any]] = None,
        is_critical: bool = False,
    ):
        self.is_success = is_success
        self.data = data
        self.msg = msg
        self.extras = extras
        self.is_critical = is_critical

        # 유효성 체크
        self._validate()

    def _validate(self) -> None:
        if not self.is_success and not self.msg:
            raise ValueError("오류 메시지를 제공해야 합니다")

    @classmethod
    def success(cls: Type[T], data: Any = None, extras: Optional[Dict[str, Any]] = None) -> T:
        return cls(data=data, is_success=True, msg=None, extras=extras)

    @classmethod
    def fail(cls: Type[T], msg: str, extras: Optional[Dict[str, Any]] = None, is_critical: bool = False) -> T:
        return cls(data=None, is_success=False, msg=msg, extras=extras, is_critical=is_critical)



class RequestsMetaClass(type):
    """
    실행순서 : __new__ -> __init__ -> __call__

    a = Cookie() 이렇게 만든 a는 객체이다. 그리고 a 객체는 Cookie의 인스턴스이다.

    NOTE - 파이썬은 모든 것이 객체, 그래서 클래스도 객체이다

    클래스라는 객체를 만들기 위한 클래스가 있어야 할텐데. 그게 메타클래스 이다

    "type"이라는 키워드를 활용하면 된다. 사실, type은 두 가지 기능이 있다.
        (1) 자료형 종류를 알아낼 때
        (2) 클래스를 만들 때

    """

    def __new__(cls, *args, **kwargs):
        """
        __new__ : 클래스 인스턴스를 생성 (메모리 할당)
        """
        return super().__new__(cls, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        """
        __init__ : 생성된 인스턴스 초기화
        """
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        """
        __call__ : 인스턴스 실행

        type을 상속받아서 만든 메타클래스의 __call__ 메소드가 호출되면
        (즉, 메타클래스를 이용해서 만든 클래스의 인스턴스를 만들때 == RequestsClass()),
        내부적으로는 type의 __call__이 호출(super.__new__(cls, *args, **kwargs))되고,
        그 type의 __call__이 인스턴스의 생성자 __new__를 호출하면서,
        RequestsClass 클래스의 인스턴스가 만들어진다.
        """
        return super().__call__(*args, **kwargs)


class RequestsClass(metaclass=RequestsMetaClass):
    """
    "class RequestsClass(metaclass=RequestsMetaClass): ..."
        라는 클래스는 이미 RequestsMetaClass 인스턴스이다.

    "RequestsClass()"라고 RequestsClass 클래스의 인스턴스를
    생성하려고 시도를 하면 RequestsMetaClass 인스턴스를 실행하는 것이 된다.
    """
    
    def __init__(self, max_retry: int = 3, wait_time: int = 2000, instant_exception: Optional[Union[Type[Exception], Type[Exception], list]] = None):
        """
        @Param
            max_retry: 최대 재시도 횟수
            wait_time: 재시도 간 대기 시간 (밀리초)
            instant_exception: 즉시 예외처리
                -> SoftTimeLimitExceeded 같은 오류는 재시도 하면 안되서
        """
        self.max_retry = max_retry
        self.wait_time = wait_time
        self.instant_exception = instant_exception if isinstance(instant_exception, list) else ([instant_exception] if instant_exception else [])


    def is_instant_exception(self, exception: Exception) -> bool:
        return any(isinstance(exception, exc) for exc in self.instant_exception)


    def make_request(self, method: str, url: str, **kwargs) -> T:
        """
        HTTP 요청을 보내고 실패 시 설정된 횟수만큼 재시도.

        :param method: HTTP 메서드 (GET, POST 등)
        :param url: 요청할 URL
        :param kwargs: 추가적인 요청 매개변수 (headers, params, data 등)
        :return: Response 객체 또는 실패 시 None
        """
        for attempt in range(1, self.max_retry + 1):
            try:
                response = requests.request(method=method, url=url, **kwargs)
                response.raise_for_status()  # 4xx/5xx 상태 코드 시 예외 발생
                return InternalAPIResponse.success(data=response)
            except requests.exceptions.Timeout as errd:
                """
                RequestException에서 잡을 수 있지만, 
                Timeout에 대한 추가적인 조작을 하고싶으면 이렇게 따로 잡으면 된다.
                """
                msg = str(errd)
            except requests.exceptions.RequestException as e:
                """
                여기서 requests의 모든 예외가 다 잡힌다.
                """
                msg = str(e)
            except Exception as e:
                if self.is_instant_exception(e):
                    raise
                msg = str(errd)
            finally:
                if attempt == self.max_retry:
                    return InternalAPIResponse.fail(msg=msg, extras={"response": response})
                time.sleep(self.wait_time / 1000) # ms

# APIManager 상속
class APIManager(RequestsClass):
    """
    @Usage
        response = APIManager().get(url, headers=headers, verify=False)
        if response.is_success:
            print(response.data.json())
        else:
            print(response.msg)
    """
    def get(self, url, **kwargs) -> T:
        return self.make_request("GET", url, **kwargs)

    def post(self, url, **kwargs) -> T:
        return self.make_request("POST", url, **kwargs)
    
    def put(self, url, **kwargs) -> T:
        return self.make_request("PUT", url, **kwargs)

    def patch(self, url, **kwargs) -> T:
        return self.make_request("PATCH", url, **kwargs)
    
    def delete(self, url, **kwargs) -> T:
        return self.make_request("DELETE", url, **kwargs)
