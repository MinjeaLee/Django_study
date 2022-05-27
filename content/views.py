import os
from django.conf import settings
from django.shortcuts import render
# APIView import
from rest_framework.views import APIView
from rest_framework.response import Response
# uuid
from uuid import uuid4
from django_study.settings import MEDIA_ROOT
from .models import Feed, Reply, Like, Bookmark

from user.models import User
# Create your views here.


class Main(APIView):
    def get(self, request):

        feed_object_list = Feed.objects.all().order_by('-id') # select * from feed
        feed_list = []

        for feed in feed_object_list:

            user = User.objects.filter(email=feed.email).first()        # search user

            reply_object_list = Reply.objects.filter(feed_id = feed.id) # user's user_id
            reply_list = []

            for reply in reply_object_list:

                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    reply_content = reply.reply_content,
                    user_id = user.user_id,
                ))

            feed_list.append(dict(
                id = feed.id,
                image=feed.image, 
                content=feed.content, 
                like_count=feed.like_count, 
                profile_image=user.profile_image, 
                user_id=user.user_id,
                reply_list=reply_list
            ))

        print("로그인 한 사용자 정보: ", request.session.get('user'))

        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first() # select * from user where email = email

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

        Feed.objects.create(image=image, content=content, email=email, like_count=0)    # insert into feed

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

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get("feed_id", None)
        reply_content = request.data.get("reply_content", None)

        email = request.session.get('email', None)


        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

    



