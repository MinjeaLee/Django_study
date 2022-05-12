from django.shortcuts import render


# import APIView
from rest_framework.views import APIView

class Main(APIView):
    def get(self, request):
        return render(request, 'django_study/main.html')

    def post(self, request):
        return render(request, 'django_study/main.html')