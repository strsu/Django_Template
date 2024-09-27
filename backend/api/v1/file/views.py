from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.exceptions.custom_exceptions import CustomParameterException

from api.v1.file.models import File
from api.v1.file.serializer import FileSerializer

from datetime import datetime
import requests
import urllib3
import PyPDF2
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        file = File.objects.get(code=request.GET.get("code"))
        file_path = f"/opt/staticfiles/chat/img/{file.path}"
        with open(file_path, "rb") as f:
            file_data = f.read()

        # HttpResponse로 파일 응답
        response = HttpResponse(file_data, content_type="text/plain")
        response["Content-Disposition"] = f'attachment; filename="{file.name}"'
        return response


class VideoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        video_dict = {}

        def get_video_list(path):
            nonlocal video_dict

            res = requests.get(
                f"http://nginx/listing/media{path}",
                headers={"Content-Type": "application/json"},
                verify=False,
            )

            if res.status_code == 200:
                file_list = res.json()
                if file_list:
                    for file in file_list:
                        if file["name"] == "$RECYCLE.BIN":
                            continue
                        if file["type"] == "directory":
                            if path == "/":
                                get_video_list(f"{path}{file['name']}")
                            else:
                                get_video_list(f"{path}/{file['name']}")
                        else:
                            if ".mp4" in file["name"]:
                                if path[1:] not in video_dict:
                                    video_dict[path[1:]] = []

                                video_dict[path[1:]].append(file["name"])
            else:
                print(path, res.status_code)

        get_video_list("/")

        return Response(video_dict, status=200)


class PDFUploadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "pdf.html", {})


class PDFUpload2View(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "pdf2.html", {})


class PDFMergeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # HTML 파일 경로 리스트
        pdfs = request.FILES.getlist("pdfs")

        # 변환된 PDF 파일을 저장할 경로 리스트
        pdf_files = []
        for i, pdf in enumerate(pdfs):
            pdf_path = os.path.join(settings.MEDIA_ROOT, f"temp_{i}.pdf")
            pdf_files.append(pdf_path)
            with open(pdf_path, "wb") as f:
                f.write(pdf.read())

        # 병합된 PDF 파일을 저장할 경로
        merged_pdf_path = os.path.join(settings.MEDIA_ROOT, "merged.pdf")

        # PDF 파일 병합
        pdf_merger = PyPDF2.PdfMerger()
        for pdf in pdf_files:
            pdf_merger.append(pdf)

        with open(merged_pdf_path, "wb") as merged_pdf_file:
            pdf_merger.write(merged_pdf_file)

        # 중간에 생성된 PDF 파일 삭제 (선택 사항)
        for pdf in pdf_files:
            os.remove(pdf)

        # 병합된 PDF 파일을 HTTP 응답으로 반환
        with open(merged_pdf_path, "rb") as merged_pdf_file:
            response = HttpResponse(
                merged_pdf_file.read(), content_type="application/pdf"
            )
            response["Content-Disposition"] = f'attachment; filename="merged.pdf"'
            response["Content-Disposition"] = f'inline; filename="merged.pdf"'

        # 병합된 PDF 파일 삭제 (선택 사항)
        os.remove(merged_pdf_path)

        return response


class MultipartFormDataView(APIView):

    def post(self, request):
        """
        multipart/form-data 연습

        getlist를 써야 리스트로 읽어온다.
            -> 아니면 for문이 이미지파일명 개수만큼 돌게됨.
        """

        ## 방법 1
        files = request.FILES
        for image in files.getlist("images"):
            image_name = image.name
            image_ext = image.content_type.split("/")[1]
            pdf_path = os.path.join(settings.MEDIA_ROOT, image_name)
            with open(pdf_path, "wb") as f:
                f.write(image.read())

        ## 방법 2
        data = request.data
        for image in data.getlist("images"):
            image_name = image.name
            image_ext = image.content_type.split("/")[1]
            print(image_name, image_ext)

        return Response(status=201)
