from kma.models import PhoneNumber


def add_phones():
    with open('/home/vlad/PycharmProjects/-OI-AMK/HelloDjango/scripts/Тесты - Лист13.csv') as file:
        for line in file:
            if line.endswith('\n'):
                line = line[:-1]
            short, phone, ru_full_name = line.split(',')
            model = PhoneNumber(
                short=short,
                phone=phone,
                ru_full_name=ru_full_name
            )
            try:
                model.save()
            except BaseException:
                pass

def add_phone_codes():
    with open('/home/vlad/PycharmProjects/-OI-AMK/HelloDjango/scripts/Тесты - Лист13.csv') as file:
        for line in file:
            if line.endswith('\n'):
                line = line[:-1]
            short, phone, ru_full_name, phone_code = line.split(',')
            model = PhoneNumber.objects.get(short=short)
            model.phone_code = phone_code
            model.save()
    

add_phone_codes()