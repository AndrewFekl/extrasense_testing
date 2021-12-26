from django.shortcuts import render, redirect
from django.views.generic.base import View

class Extrasens:
    def __init__(self, name):
        self.name = name

    def guess_number(self):
        return 5




class ExtrasensesView(View):
    """Класс, моделирующий тестирование экстрасенсорных способностей. При вызове метода GET отображает приглашение
    число и нулевые рейтинги экстрасенсов. При вызове метода POST будут отображаться ответы экстрасенсов,
    обновляться статистика и рейтинги экстрасенсов. В зависимости от установки триггера guess_trigger будет чередаватся
    показ результатов и приглашение загадать число"""

    def __init__(self, *args, **kwargs):
        super(ExtrasensesView, self).__init__(*args, **kwargs)

        # триггер режима страницы. Если True - требуется загадать слово. Если False - ввести ответ.
        self.guess_trigger = True

        # Словарь объектов экстрасенсов
        self.extrasenses = {'1': Extrasens('John'), '2': Extrasens('Moana')}



    def get(self, request):
        # список загаданных слов пользователя
        request.session['user_story'] = []
        # словари для хранения истории ответов экстрасенсов, текущих ответов и рейтингов
        request.session['extrasenses_stories'] = {}
        request.session['extrasenses_answers'] = {}
        request.session['extrasenses_data'] = {}

        for key in self.extrasenses.keys():
            extrasenses_stories = request.session['extrasenses_stories']
            extrasenses_stories[key] = []
            request.session['extrasenses_stories'] = extrasenses_stories

            extrasenses_answers = request.session['extrasenses_answers']
            extrasenses_answers[key] = None
            request.session['extrasenses_answers'] = extrasenses_answers

            extrasenses_data = request.session['extrasenses_data']
            extrasenses_data[key] = [0, 0, 0]
            request.session['extrasenses_data'] = extrasenses_data


        context = {'guess_trigger': self.guess_trigger,
                   'extrasenses': self.extrasenses,
                   'user_story': request.session['user_story'],
                   'extrasenses_stories': request.session['extrasenses_stories'],
                   'extrasenses_answers': request.session['extrasenses_answers'],
                   'extrasenses_data': request.session['extrasenses_data']
                   }

        return render(request, 'extrasenses/extrasenses.html', context)

    def post(self, request):

        if not 'put_up_number' in request.POST:
            for key, extrasens in self.extrasenses.items():
                extrasenses_answers = request.session['extrasenses_answers']
                answer = extrasens.guess_number()
                extrasenses_answers[key] = answer
                request.session['extrasenses_answers'] = extrasenses_answers
            self.guess_trigger = False
            context = {'guess_trigger': self.guess_trigger,
                   'extrasenses': self.extrasenses,
                   'user_story': request.session['user_story'],
                   'extrasenses_stories': request.session['extrasenses_stories'],
                   'extrasenses_answers': request.session['extrasenses_answers'],
                   'extrasenses_data': request.session['extrasenses_data']
                   }

            return render(request, 'extrasenses/extrasenses.html', context)

        put_up_number = request.POST['put_up_number']
        user_story = request.session['user_story']
        request.session['user_story'] = user_story + [put_up_number]

        for key, extrasens in self.extrasenses.items():
            answer = request.session['extrasenses_answers'][key]
            request.session['extrasenses_data'][key][0] += 1
            if int(put_up_number) == answer:
                request.session['extrasenses_data'][key][1] += 1
            if request.session['extrasenses_data'][key][0] != 0:
                raiting = request.session['extrasenses_data'][key][1] / request.session['extrasenses_data'][key][0] * 100
                raiting = round(raiting, 2)
                request.session['extrasenses_data'][key][2] = raiting
            request.session['extrasenses_stories'][key].append(answer)
            request.session['extrasenses_answers'][key] = None

        self.guess_trigger = True

        context = {'guess_trigger': self.guess_trigger,
                   'extrasenses': self.extrasenses,
                   'user_story': request.session['user_story'],
                   'extrasenses_stories': request.session['extrasenses_stories'],
                   'extrasenses_answers': request.session['extrasenses_answers'],
                   'extrasenses_data': request.session['extrasenses_data']
                   }
        return render(request, 'extrasenses/extrasenses.html', context)

def session_test(request):

    if request.method == 'GET':
        request.session['test_value'] = 'Сука драная'
        request.session['test_list'] = ['a', 'b', 'c']
        request.session['test_dict'] = {'1': 'one', '2': ['two', 'three']}


    if request.method == 'POST':
        request.session['test_value'] = request.POST['aught']

    return render(request, 'extrasenses/test.html', {'test_value': request.session['test_value'],
                  'test_list': request.session['test_list'], 'test_dict': request.session['test_dict']})

class SessionTestView(View):

    def get(self, request):
        request.session['test_value'] = 'Сука драная'
        request.session['test_list'] = []
        request.session['test_dict'] = {'1': 'one', '2': ['two', 'three']}

        return render(request, 'extrasenses/test.html', {'test_value': request.session['test_value'],
                                                         'test_list': request.session['test_list'],
                                                         'test_dict': request.session['test_dict'],
                                                         'dict_keys': ['1', '2']})
    def post(self, request):
        answer = request.POST.get('aught', 'not found')
        current_list = request.session['test_list']
        request.session['test_list'] = current_list + [answer]

        return render(request, 'extrasenses/test.html', {'test_value': request.session['test_value'],
                                                         'test_list': request.session['test_list'],
                                                         'test_dict': request.session['test_dict'],

                                                         'dict_keys': ['1', '2']})























