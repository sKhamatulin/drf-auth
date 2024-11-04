import requests

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as BaseUserViewSet

import yaml

from .serializers import UserSerializer


WEBHOOK_TOKEN = 'tuzwh9ecszs0jhhc'
B24_USER_ID = '7'


class UserContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.contactId:
            return Response({'error': 'contactId not found.'}, status=400)

        # contact_id = user.contactId
        contact_id = 11

        url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/crm.contact.get.json?id={contact_id}'

        response = requests.get(url)

        data = response.json().get('result', {})

        filtered_data = {
            'ID': data.get('ID'),
            'NAME': data.get('NAME'),
            'SECOND_NAME': data.get('SECOND_NAME'),
            'LAST_NAME': data.get('LAST_NAME'),
            'LEAD_ID': data.get('LEAD_ID'),
            'TYPE_ID': data.get('TYPE_ID'),
            'BIRTHDATE': data.get('BIRTHDATE'),
            'HAS_PHONE': data.get('HAS_PHONE'),
            'HAS_EMAIL': data.get('HAS_EMAIL'),
            'HAS_IMOL': data.get('HAS_IMOL'),
            'DATE_CREATE': data.get('DATE_CREATE'),
            'DATE_MODIFY': data.get('DATE_MODIFY'),
            'ASSIGNED_BY_ID': data.get('ASSIGNED_BY_ID'),
            'LAST_ACTIVITY_TIME': data.get('LAST_ACTIVITY_TIME'),
            'ADDRESS': data.get('ADDRESS'),
            'ADDRESS_2': data.get('ADDRESS_2'),
            'ADDRESS_CITY': data.get('ADDRESS_CITY'),
            'ADDRESS_POSTAL_CODE': data.get('ADDRESS_POSTAL_CODE'),
            'ADDRESS_REGION': data.get('ADDRESS_REGION'),
            'ADDRESS_PROVINCE': data.get('ADDRESS_PROVINCE'),
            'ADDRESS_COUNTRY': data.get('ADDRESS_COUNTRY'),
            'ADDRESS_LOC_ADDR_ID': data.get('ADDRESS_LOC_ADDR_ID'),
            'LAST_ACTIVITY_BY': data.get('LAST_ACTIVITY_BY'),
        }

        return Response({'result': filtered_data}, status=response.status_code)


class UserManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_contact_view = UserContactView()
        data = user_contact_view.get(request).data
        assigned_by_id = data.get('result', {}).get('ASSIGNED_BY_ID')

        url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/user.get.json?id={assigned_by_id}'

        response = requests.get(url)

        # data = response.json().get('result', {})

        # filtered_data = {
        #     'ID': data.get('ID'),
        #     'ACTIVE': data.get('ACTIVE'),
        #     'NAME': data.get('NAME'),
        #     'LAST_NAME': data.get('LAST_NAME'),
        #     'SECOND_NAME': data.get('SECOND_NAME'),
        #     'TITLE': data.get('TITLE'),
        #     'IS_ONLINE': data.get('IS_ONLINE'),
        #     'PERSONAL_PROFESSION': data.get('PERSONAL_PROFESSION'),
        #     'PERSONAL_GENDER': data.get('PERSONAL_GENDER'),
        #     'PERSONAL_BIRTHDAY': data.get('PERSONAL_BIRTHDAY'),
        #     'PERSONAL_CITY': data.get('PERSONAL_CITY'),
        #     'PERSONAL_STATE': data.get('PERSONAL_STATE'),
        #     'UF_EMPLOYMENT_DATE': data.get('UF_EMPLOYMENT_DATE'),
        #     'UF_DEPARTMENT': data.get('UF_DEPARTMENT'),
        # }

        # return Response({'result': filtered_data}, status=response.status_code)

        return Response(response.json(), status=response.status_code)


class UserCompaniesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_contact_view = UserContactView()
        data = user_contact_view.get(request).data
        user_id = data.get('result', {}).get('ID')

        url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/crm.contact.company.items.get.json?id={user_id}'

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
            url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/crm.company.get.json?id={company_id}'
            response = requests.get(url)

            if response.status_code == 200:
                company_data = response.json().get('result', {})

                filtered_company_data = {
                    'COMPANY_TYPE': company_data.get('COMPANY_TYPE'),
                    'TITLE': company_data.get('TITLE'),
                    'LOGO': company_data.get('LOGO'),
                    'LEAD_ID': company_data.get('LEAD_ID'),
                    'HAS_PHONE': company_data.get('HAS_PHONE'),
                    'HAS_EMAIL': company_data.get('HAS_EMAIL'),
                    'HAS_IMOL': company_data.get('HAS_IMOL'),
                    'BANKING_DETAILS': company_data.get('BANKING_DETAILS'),
                    'INDUSTRY': company_data.get('INDUSTRY'),
                    'REVENUE': company_data.get('REVENUE'),
                    'CURRENCY_ID': company_data.get('CURRENCY_ID'),
                    'EMPLOYEES': company_data.get('EMPLOYEES'),
                    'OPENED': company_data.get('OPENED'),
                    'IS_MY_COMPANY': company_data.get('IS_MY_COMPANY'),
                    'LAST_ACTIVITY_TIME': company_data.get('LAST_ACTIVITY_TIME'),
                    'ADDRESS': company_data.get('ADDRESS'),
                    'ADDRESS_2': company_data.get('ADDRESS_2'),
                    'ADDRESS_CITY': company_data.get('ADDRESS_CITY'),
                    'ADDRESS_POSTAL_CODE': company_data.get('ADDRESS_POSTAL_CODE'),
                    'ADDRESS_REGION': company_data.get('ADDRESS_REGION'),
                    'ADDRESS_PROVINCE': company_data.get('ADDRESS_PROVINCE'),
                    'ADDRESS_COUNTRY': company_data.get('ADDRESS_COUNTRY'),
                    'ADDRESS_COUNTRY_CODE': company_data.get('ADDRESS_COUNTRY_CODE'),
                    'ADDRESS_LOC_ADDR_ID': company_data.get('ADDRESS_LOC_ADDR_ID'),
                    'ADDRESS_LEGAL': company_data.get('ADDRESS_LEGAL'),
                    'REG_ADDRESS': company_data.get('REG_ADDRESS'),
                    'REG_ADDRESS_2': company_data.get('REG_ADDRESS_2'),
                    'REG_ADDRESS_CITY': company_data.get('REG_ADDRESS_CITY'),
                    'REG_ADDRESS_POSTAL_CODE': company_data.get('REG_ADDRESS_POSTAL_CODE'),
                    'REG_ADDRESS_REGION': company_data.get('REG_ADDRESS_REGION'),
                    'REG_ADDRESS_PROVINCE': company_data.get('REG_ADDRESS_PROVINCE'),
                    'REG_ADDRESS_COUNTRY': company_data.get('REG_ADDRESS_COUNTRY'),
                    'REG_ADDRESS_COUNTRY_CODE': company_data.get('REG_ADDRESS_COUNTRY_CODE'),
                    'REG_ADDRESS_LOC_ADDR_ID': company_data.get('REG_ADDRESS_LOC_ADDR_ID'),
                    'LAST_ACTIVITY_BY': company_data.get('LAST_ACTIVITY_BY'),
                    'UF_CRM_1729153192833': company_data.get('UF_CRM_1729153192833'),
                }

                company_details_list.append(filtered_company_data)
            else:
                company_details_list.append({'error': 'Error fetching company'
                                             f'{company_id}: {response.text}'})

        return Response(company_details_list, status=200)


# class UserCompanyDocumentsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         user_companies_view = UserCompanyDetailsView()
#         print(user_companies_view)
#         companies_response = user_companies_view.get(request)
#         companies_data = companies_response.data

#         if not companies_data:
#             return Response({"error": "No associated companies found."},
#                             status=404)

#         company = companies_data[0]  # Берем первую компанию пользователя
#         folder_id = company.get('UF_CRM_1729153192833')

#         if not folder_id:
#             return Response({"error": "Folder ID not found in company data."},
#                             status=400)

#         url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/disk.folder.getchildren.json?id={folder_id}'
#         response = requests.get(url)
#         response_data = response.json()

#         documents = response_data.get('result', [])
#         if not documents:
#             return Response({"error": "No documents found in the company folder."},
#                             status=404)

#         document_list = [
#             {
#                 'ID': doc.get('ID'),
#                 'NAME': doc.get('NAME'),
#                 'TYPE': doc.get('TYPE'),
#                 'DOWNLOAD_URL': doc.get('DOWNLOAD_URL'),
#                 'SIZE': doc.get('SIZE'),
#                 'CREATE_TIME': doc.get('CREATE_TIME'),
#                 'UPDATE_TIME': doc.get('UPDATE_TIME'),
#             }
#             for doc in documents
#         ]

#         return Response({"documents": document_list}, status=200)


class UserCompanyDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_companies_view = UserCompanyDetailsView()
        companies_response = user_companies_view.get(request)
        companies_data = companies_response.data

        if not companies_data:
            return Response({"error": "No associated companies found."}, status=404)

        company = companies_data[0]  # Берем первую компанию пользователя
        folder_id = company.get('UF_CRM_1729153192833')

        if not folder_id:
            return Response({"error": "Folder ID not found in company data."}, status=400)

        url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/disk.folder.getchildren.json?id={folder_id}'
        response = requests.get(url)
        response_data = response.json()
        base_url = request.build_absolute_uri('/api/v1/hooks/downloadfile')

        documents = response_data.get('result', [])
        if not documents:
            return Response({"error": "No documents found in the company folder."}, status=404)

        document_list = [
            {
                'ID': doc.get('ID'),
                'NAME': doc.get('NAME'),
                'TYPE': doc.get('TYPE'),
                'DOWNLOAD_URL_OLD': doc.get('DOWNLOAD_URL'),
                'DOWNLOAD_URL': f"{base_url}/{folder_id}/{doc.get('ID')}",
                'SIZE': doc.get('SIZE'),
                'CREATE_TIME': doc.get('CREATE_TIME'),
                'UPDATE_TIME': doc.get('UPDATE_TIME'),
            }
            for doc in documents
        ]

        return Response({"documents": document_list}, status=200)


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, folder_id, file_id):
        # Получение информации о файле
        url = f'https://b-p24.ru/rest/{B24_USER_ID}/{WEBHOOK_TOKEN}/disk.folder.getchildren.json?id={folder_id}'
        response = requests.get(url)
        response_data = response.json()
        print('response_data = ' + str(response_data))

        document = next((doc for doc in response_data.get('result', []) if doc.get('ID') == file_id), None)

        if not document:
            return Response({"error": "Document not found."}, status=404)

        download_url = document.get('DOWNLOAD_URL')
        print('download_url = ' + str(download_url))

        # Загружаем файл с Bitrix24
        file_response = requests.get(download_url)
        print('file_response = ' + str(file_response))

        # Возвращаем файл пользователю
        return HttpResponse(file_response.content, content_type=file_response.headers['Content-Type'], headers={
            'Content-Disposition': f'attachment; filename="{document["NAME"]}"'
        })


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
