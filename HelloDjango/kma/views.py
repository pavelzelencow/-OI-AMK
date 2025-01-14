from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import DefaultWeb, PhoneNumber, UserApiKey
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .test_lead.kma_leads import KmaAPITest, KmaAPiError


@login_required
def default_webs(request):
    webs = DefaultWeb.objects.all()
    content = {
        'webs': webs
    }
    return render(request, 'kma/default_webs.html', content)

@login_required
def phones(requests):
    phones = PhoneNumber.objects.all().order_by('short')
    try:
        user_api_key = UserApiKey.objects.get(user=requests.user)
        content = {
            'phones': phones,
            'user_api_key': user_api_key,
        }
        return render(requests, 'kma/phones.html', content)
    except UserApiKey.DoesNotExist:
        content = {
            'phones': phones,
        }
        return render(requests, 'kma/phones.html', content)


@csrf_exempt
@login_required
def get_phone_code(request):
    try:
        country_code = request.GET['country_code']
        country_code = country_code.lower()
        phone_model = PhoneNumber.objects.get(short=country_code)
        answer = {
            'success': True,
            'phone_code': phone_model.phone_code,
        }
    except BaseException as error:
        answer = {
            'success': False,
            'message': str(error)
        }
    return JsonResponse(answer, safe=False)

@login_required
def manual(request):
    return render(request, 'kma/manual/index.html')



@login_required
@csrf_exempt
def test_rekl(requests):
    try:
        countrys = requests.POST['countrys']
        countrys_list = countrys.split(',')
        test_name = requests.POST['test_name']
        offer_id = requests.POST['offer_id']
        country_phones = PhoneNumber.get_country_phone(*countrys_list)
        test_name = False if test_name != 'eng_test' else True
        user_api_key = UserApiKey.objects.get(user=requests.user)
        kma = KmaAPITest(user_api_key.token,offer_id, country_phones, test_name)
        kma.test_offer()
        link = 'https://google.com/'
        leads = ['ru', 'by', 'ua']
        answer = {
            'success': True,
            'link': kma.get_tracker_link(),
            # 'link': link,
            'leads': kma.get_leads_data(),
        }
    except KmaAPiError as error:
        answer = {
            'success': False,
            'message': str(error.__doc__),
            'data': error.data,
        }
    return JsonResponse(answer, safe=False)

@login_required
@csrf_exempt
def get_offer(requests):
    try:
        offer_id = requests.POST['offer_id']
        user_api = UserApiKey.objects.get(user=requests.user)
        offer_data = KmaAPITest.get_offer(offer_id, user_api.token)
        answer = {
            'success': True,
            'offer_data': offer_data,
        }
    except BaseException as error:
        answer = {
            'success': False,
            'message': str(error)
        }
    return JsonResponse(answer)