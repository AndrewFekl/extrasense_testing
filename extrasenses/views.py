from django.shortcuts import render, redirect
from django.views.generic.base import View
from .subject_area_methods import Extrasens, RandomForecast, OnlyNewRandomForecast
from .models import SessionStorage


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

        # Создаем объект для записи и получения данных из сессий
        self.session_storage = SessionStorage()


    def get(self, request):

        context = self.session_storage.get_context(request)
        context.update({'guess_trigger': self.guess_trigger, 'extrasenses': self.extrasenses})

        return render(request, 'extrasenses/extrasenses.html', context)


    def post(self, request):
        # После нажатия кнопки Угадать без передачи параметра из поля ответа
        if not 'put_up_number' in request.POST:

            for key, extrasens in self.extrasenses.items():

                answer = extrasens.guess_number()
                self.session_storage.update_extrasens_answers(request, key, answer)

            self.guess_trigger = False

            context = self.session_storage.get_context(request)
            context.update({'guess_trigger': self.guess_trigger, 'extrasenses': self.extrasenses})

            return render(request, 'extrasenses/extrasenses.html', context)

        # Когда из формы передается загаданное число
        put_up_number = request.POST['put_up_number']
        # Обновляем историю загаданных чисел пользователя
        self.session_storage.update_user_story(request, put_up_number)

        # Обновляем историю ответов и статистику экстрасенсов
        for key, extrasens in self.extrasenses.items():

            self.session_storage.update_extrasens_story(request, key)

            self.session_storage.update_extrasens_data(request, key, put_up_number)

            self.session_storage.update_extrasens_answers(request, key, None)

        self.guess_trigger = True

        context = self.session_storage.get_context(request)
        context.update({'guess_trigger': self.guess_trigger, 'extrasenses': self.extrasenses})

        return render(request, 'extrasenses/extrasenses.html', context)


def MainView(request):
    # Представление отображает главную страницу и устанавливает начальные значения в сессии

    extrasenses = {'1': Extrasens('John'), '2': Extrasens('Moana', OnlyNewRandomForecast())}
    extrasenses_keys = extrasenses.keys()

    session_storage = SessionStorage()
    session_storage.set_start_values(request, extrasenses_keys)

    return render(request, 'extrasenses/main_page.html')


class ResultsView(View):
    # Представление возвращает статистику работы экстрасенсов и тестировщика

    def __init__(self, *args, **kwargs):
        super(ResultsView, self).__init__(*args, **kwargs)

        # Инициируем словарь объектов экстрасенсов
        self.extrasenses = {'1': Extrasens('John'), '2': Extrasens('Moana', OnlyNewRandomForecast())}

        # Создаем объект для записи и получения данных из сессий
        self.session_storage = SessionStorage()

    def get(self, request):
        context = self.session_storage.get_context(request)
        context.update({'extrasenses': self.extrasenses})

        return render(request, 'extrasenses/results_page.html', context)



























