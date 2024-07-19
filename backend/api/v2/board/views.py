from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Board, Author


class BoardView(APIView):
    def get(self, requests):

        page = requests.GET.get("page", 1)
        author_name = requests.GET.get("author")

        board = Board.actives.select_related("author")

        if author_name:
            try:
                author = Author.objects.get(author=author_name)
            except Exception as e:
                return Response(status=404)
            else:
                board = board.filter(author=author)

        page_idx = 10 * (int(page) - 1)

        board = board.order_by("-id")[page_idx : page_idx + 10]

        return Response(board.values(), status=200)
