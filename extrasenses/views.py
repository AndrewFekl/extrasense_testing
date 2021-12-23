from django.shortcuts import render, redirect
from django.views.generic.base import View

class Extrasens:
    def __init__(self, name):
        self.name = name
        self.attempts = 0
        self.coincidence = 0
        self.raiting = 0
        self.current_answer = None

    def guess_number(self):
        self.current_answer = '5'




class ExtrasensesView(View):
    """Класс, моделирующий тестирование экстрасенсорных способностей. При вызове метода GET отображает приглашение
    число и нулевые рейтинги экстрасенсов. При вызове метода POST будут отображаться ответы экстрасенсов,
    обновляться статистика и рейтинги экстрасенсов. В зависимости от установки триггера guess_trigger будет чередаватся
    показ результатов и приглашение загадать число"""

    def __init__(self, *args, **kwargs):
        super(ExtrasensesView, self).__init__(*args, **kwargs)
        # триггер режима страницы. Если True - требуется загадать слово. Если False - ввести ответ.
        self.guess_trigger = True
        # список загаданных слов пользователя
        self.user_story = []
        # словарь для хранения истории ответов экстрасенсов
        self.extrasenses = {'1': Extrasens('John'), '2': Extrasens('Moana')}
        self.extrasenses_stories = {'1': [], '2': []}


    def get(self, request):
        context = {'guess_trigger': self.guess_trigger, 'user_story': self.user_story,
                   'extrasenses': self.extrasenses, 'extrasenses_stories': self.extrasenses_stories}
        #self.guess_trigger = False
        return render(request, 'extrasenses/extrasenses.html', context)

    def post(self, request):

        if not 'put_up_number' in request.POST:
            for extrasens in self.extrasenses.values():
                extrasens.guess_number()
            self.guess_trigger = False
            context = {'guess_trigger': self.guess_trigger, 'user_story': self.user_story,
                       'extrasenses': self.extrasenses, 'extrasenses_stories': self.extrasenses_stories}

            return render(request, 'extrasenses/extrasenses.html', context)



        if 'put_up_number' in request.POST:
            number = request.POST['put_up_number']
            for key, extrasens in self.extrasenses.items():
                answer = extrasens.current_answer
                extrasens.attempts += 1
                if number == answer:
                    extrasens.coincidence += 1
                if extrasens.attempts != 0:
                    extrasens.raiting = extrasens.coincidence / extrasens.attempts * 100
                self.extrasenses_stories.update({key: self.extrasenses_stories[key].append(answer)})
                extrasens.current_answer = None
            self.user_story.append(number)
            self.guess_trigger = True

            context = {'guess_trigger': self.guess_trigger, 'user_story': self.user_story,
                       'extrasenses': self.extrasenses, 'extrasenses_stories': self.extrasenses_stories}
            return render(request, 'extrasenses/extrasenses.html', context)












# Create your views here.
