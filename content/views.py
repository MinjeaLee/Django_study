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

        feed_object_list = Feed.objects.all().order_by('-id') # select * from feed
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            feed_list.append(dict(image=feed.image, content=feed.content, like_count=feed.like_count, profile_image=user.profile_image, user_id=user.user_id))

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
        email = request.session.get('email')

        Feed.objects.create(image=image, content=content, email=email, like_count=0)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):

        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()

        if email is None:
            return render(request, 'user/login.html')
        if user is None:
            return render(request, 'user/login.html')

        return render(request, 'content/profile.html', context=dict(user=user))