from django.db import models
import json
import math

class SessionStorage:
    """Класс является контейнером и содержит необходимые методы для записи и извлечения данных из пользовательских
    сессий"""

    def set_start_values(self, request, extrasenses_keys):
        # Метод устанавливает стартовое значение атрибутов внутри сессии
        del request.session['user_story']
        del request.session['extrasenses_stories']
        del request.session['extrasenses_answers']
        del request.session['extrasenses_data']

        # Список загаданных слов пользователя
        user_story = []
        # Словари для хранения истории ответов экстрасенсов, текущих ответов и рейтингов
        extrasenses_stories = {}
        extrasenses_answers = {}
        extrasenses_data = {}

        for key in extrasenses_keys:

            extrasenses_stories[key] = []
            extrasenses_answers[key] = None
            extrasenses_data[key] = [0, 0, 0.5, 0]

        request.session['extrasenses_stories'] = json.dumps(extrasenses_stories)
        request.session['extrasenses_answers'] = json.dumps(extrasenses_answers)
        request.session['extrasenses_data'] = json.dumps(extrasenses_data)
        request.session['user_story'] = json.dumps(user_story)


    def get_context(self, request):
        # Метод возвращает данные из сессии

        context = {
            'user_story': json.loads(request.session['user_story']),
            'extrasenses_stories': json.loads(request.session['extrasenses_stories']),
            'extrasenses_answers': json.loads(request.session['extrasenses_answers']),
            'extrasenses_data': json.loads(request.session['extrasenses_data']),
        }

        return context


    def update_extrasens_answers(self, request, key, answer):
        # Метод обновляет ответы экстрасенсов в сессии

        extrasenses_answers = json.loads(request.session['extrasenses_answers'])
        extrasenses_answers[key] = answer
        request.session['extrasenses_answers'] = json.dumps(extrasenses_answers)


    def update_user_story(self, request, put_up_number):
        # Метод обновляет историю ответов пользователя

        user_story = json.loads(request.session['user_story'])
        request.session['user_story'] = json.dumps(user_story + [put_up_number])


    def update_extrasens_story(self, request, key):

        answers = json.loads(request.session['extrasenses_answers'])
        extrasenses_stories = json.loads(request.session['extrasenses_stories'])
        extrasenses_stories[key] = extrasenses_stories[key] + [answers[key]]

        request.session['extrasenses_stories'] = json.dumps(extrasenses_stories)


    def update_extrasens_data(self, request, key, put_up_number):

        answers = json.loads(request.session['extrasenses_answers'])
        extrasenses_data = json.loads(request.session['extrasenses_data'])
        extrasens_data = extrasenses_data[key]
        extrasens_data[0] += 1

        if int(put_up_number) == answers[key]:
            extrasens_data[1] += 1
            extrasens_data[3] += 1
        else:
            extrasens_data[3] -= 1

        raiting = self.set_raiting(extrasens_data[3])
        extrasens_data[2] = raiting

        extrasenses_data[key] = extrasens_data
        request.session['extrasenses_data'] = json.dumps(extrasenses_data)


    def set_raiting(self, score):

        score = -1 * score
        raiting = round(1/(1+math.exp(score)), 3)
        return raiting













