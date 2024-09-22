import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as BaseUserViewSet

from django.http import HttpResponse
import yaml

from .serializers import UserSerializer


WEBHOOK_TOKEN = 'fnhhlfuj12fos91o'


class UserContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.contactId:
            return Response({'error': 'contactId not found.'}, status=400)

        # contact_id = user.contactId
        contact_id = 9

        url = f'https://b-p24.ru/rest/7/{WEBHOOK_TOKEN}/crm.contact.get.json?id={contact_id}'

        response = requests.get(url)

        return Response(response.json(), status=response.status_code)


class UserManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_contact_view = UserContactView()
        data = user_contact_view.get(request).data
        assigned_by_id = data.get('result', {}).get('ASSIGNED_BY_ID')

        url = f'https://b-p24.ru/rest/7/{WEBHOOK_TOKEN}/crm.contact.get.json?id={assigned_by_id}'

        response = requests.get(url)

        return Response(response.json(), status=response.status_code)


class UserCompaniesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_contact_view = UserContactView()
        data = user_contact_view.get(request).data
        user_id = data.get('result', {}).get('ID')

        url = f'https://b-p24.ru/rest/7/{WEBHOOK_TOKEN}/crm.contact.company.items.get.json?id={user_id}'

        response = requests.get(url)

        return Response(response.json(), status=response.status_code)
    

class UserCompanyDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_companies_view = UserCompaniesView()
        companies_response = user_companies_view.get(request)
        company_id_list = [company['COMPANY_ID'] for company in
                           companies_response.data.get('result', [])]
        company_details_list = []

        for company_id in company_id_list:
            url = f'https://b-p24.ru/rest/7/{WEBHOOK_TOKEN}/crm.company.get.json?id={company_id}'
            response = requests.get(url)

            if response.status_code == 200:
                company_details_list.append(response.json().get('result', {}))
            else:
                company_details_list.append({'error': 'Error fetching company'
                                             f'{company_id}: {response.text}'})

        return Response(company_details_list, status=200)


class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'is_authenticated': True})


class UserViewSet(BaseUserViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


def schema_view(request):
    with open('schema.yaml', 'r') as f:
        schema = yaml.safe_load(f)
    return HttpResponse(yaml.dump(schema), content_type='application/yaml')
