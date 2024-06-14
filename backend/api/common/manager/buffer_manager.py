from django.http import HttpResponse

from urllib.parse import quote
from io import BytesIO
import pandas as pd


class BufferManager:

    @classmethod
    def save_excel_to_buffer(cls, data: dict):
        df = pd.DataFrame(data)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(writer)

        buffer.seek(0)

        return buffer

    @classmethod
    def get_quoted_filename(cls, filename: str):
        return quote(filename.encode("utf-8"))

    @classmethod
    def get_excel_response(cls, file: BytesIO, filename: str):
        response = HttpResponse(
            file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment;filename*=UTF-8''%s" % filename

        return response
