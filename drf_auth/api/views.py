from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import yaml


class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({'is_authenticated': True})



def schema_view(request):
    with open('schema.yaml', 'r') as f:
        schema = yaml.safe_load(f)
    return HttpResponse(yaml.dump(schema), content_type='application/yaml')

## /Users/sergeykhamatulin/Dev/AuthorIT/intizar/drf-auth/drf-auth/drf_auth/schema.yaml