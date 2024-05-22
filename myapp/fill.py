from myapp.models import *
import random
from faker import Faker
fake = Faker('ru_RU')

class Data():
    def main(self):
        symptom_name = [
            "Головная боль",
            "Тошнота",
            "Боль в груди",
            "Высокая температура",
            "Кашель",
            "Озноб",
            "Боли в животе",
            "Слабость",
            "Затрудненное дыхание",
            "Потеря аппетита",
        ]
        
        result_name = [
            "Нормальные показатели крови и мочи.",
            "Повышенный холестерин.",
            "Наличие инфекции.",
            "Пониженные уровни витаминов или минералов.",
            "Патологии щитовидной железы.",
            "Диабет.",
            "Опухоли или новообразования.",
            "Анемия.",
            "Повышенное давление.",
            "Заболевания органов пищеварительной системы.",
            ]
        
        for _ in range(100000):
            Workers.objects.create(
                name=fake.name(),
                status=random.choice(['фельдшер', 'медсестра', 'водитель']),
                info=WorkersInfo.objects.create(
                    startwork=fake.date(),
                )
            )
            
        for _ in range(100):
            Cars.objects.create(
                type = random.choice(['реанимация', 'обычная']),
                number = fake.bothify(text='???###'),
                mark = fake.bothify(text='???###'),
            )
            
        for i in range(100):
            Brigade.objects.create(
                feldsher = random.choice(Workers.objects.filter(status='фельдшер')),
                med = random.choice(Workers.objects.filter(status='медсестра')),
                driver = random.choice(Workers.objects.filter(status='водитель')),
                car = random.choice(Cars.objects.all()),
                worktimestart = fake.time(),
                worktimeend = fake.time(),
                number = i+1,
            )
            
        for _ in range(100):
            Report.objects.create(
                symptom =  random.choice(symptom_name),
                name = fake.name(),
                adress = fake.address(),
                brigade = random.choice(Brigade.objects.all()),
                result = random.choice(['умер', 'везем в больницу', 'оказано лечение']),
                timestart = fake.time(),
                year = random.randint(2000, 2024),
            )
            
        for _ in range(100):
            RelutsInsepctions.objects.create(
                person = random.choice(Report.objects.all()),
                result = random.choice(result_name),
            )