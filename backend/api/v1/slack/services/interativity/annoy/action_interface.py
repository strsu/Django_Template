from abc import ABC, abstractmethod


class ActionInterface(ABC):
    """
    봇 기능을 위한 인터페이스
    """

    @abstractmethod
    def alert(self, data) -> bool:
        """
        Slack을 통해 이슈를 전파하는 함수

        blocks = self.binding(data)
        """
        pass

    @abstractmethod
    def binding(self, data):
        """
        data를 slack block으로 바인딩 하는 함수
        """
        pass

    @abstractmethod
    def resolve(self, action: dict, message: dict, thread_ts: str) -> bool:
        """
        이슈를 처리하는 함수

        action_type = action.get("type")
        data = self.extract(message)

        match action_type:
            case _:
                pass
        """

    @abstractmethod
    def extract(self, message):
        """
        메세지에서 데이터를 추출하는 함수
        """
        pass
