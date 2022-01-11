from django.shortcuts import render, redirect
from django.views.generic.base import View
from .subject_area_methods import Extrasens, RandomForecast, OnlyNewRandomForecast


class ExtrasensesView(View):
    """Класс, моделирующий тестирование экстрасенсорных способностей. При вызове метода GET отображает приглашение
    число и нулевые рейтинги экстрасенсов. При вызове метода POST будут отображаться ответы экстрасенсов,
    обновляться статистика и рейтинги экстрасенсов. В зависимости от установки триггера guess_trigger будет чередоваться
    показ результатов и приглашение загадать число"""

    def __init__(self, *args, **kwargs):
        super(ExtrasensesView, self).__init__(*args, **kwargs)

        # триггер режима страницы. Если True - требуется загадать слово. Если False - ввести ответ.
        self.guess_trigger = True

        # Инициируем словарь объектов экстрасенсов
        self.extrasenses = {'1': Extrasens('John'), '2': Extrasens('Moana', OnlyNewRandomForecast())}

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
        # После нажатия кнопки Угадать без передачи параметра из поля ответв
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

        # Когда из формы передается загаданное число
        put_up_number = request.POST['put_up_number']
        # Обновляем историю загаданных чисел пользователя
        user_story = request.session['user_story']
        request.session['user_story'] = user_story + [put_up_number]

        # Обновляем историю ответов и статистику экстрасенсов
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
























