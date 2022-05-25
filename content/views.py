import os
from django.conf import settings
from django.shortcuts import render
# APIView import
from rest_framework.views import APIView
from rest_framework.response import Response
# uuid
from uuid import uuid4
from django_study.settings import MEDIA_ROOT
from .models import Feed

from user.models import User
# Create your views here.
class Main(APIView):
    def get(self, request):

        feed_list = Feed.objects.all().order_by('-id') # select * from feed

        print("로그인 한 사용자 정보: ", request.session.get('user'))

        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()

        if email is None:
            return render(request, 'user/login.html')
        if user is None:
            return render(request, 'user/login.html')



        return render(request, 'django_study/main.html', context=dict(feeds=feed_list, user=user))

class UploadFeed(APIView):
    def post(self, request):

        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get("content")
        user_id = request.data.get("user_id")
        profile_image = request.data.get("profile_image")
        like_count = request.data.get("like_count")

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=like_count)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        return render(request, 'django_study/profile.html')