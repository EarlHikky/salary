import os
from collections import defaultdict

from dotenv import load_dotenv
from terminaltables import DoubleTable

from salary import get_average_salary
from services import SuperJob, HeadHunter

LANGUAGES = [
    'JavaScript', 'Java', 'Python', 'Ruby',
    'PHP', 'C++', 'C#', 'C', 'Go', 'Scala',
]


class Stats:
    def __init__(self, service, languages=None):
        if languages is None:
            languages = LANGUAGES
        self.service = service
        self.vacancies_stats = defaultdict(dict)
        self.languages = languages

    def get_stats(self):
        for language in self.languages:
            vacancies, vacancies_found = self.service.get_vacancies(language)
            average_salary, vacancies_processed = get_average_salary(vacancies)
            self.vacancies_stats[language]['vacancies_found'] = vacancies_found
            self.vacancies_stats[language]['vacancies_processed'] = vacancies_processed
            self.vacancies_stats[language]['average_salary'] = average_salary
        return dict(self.vacancies_stats)


class Table:
    TABLE_HEADERS = 'Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата'

    def __init__(self, title, values):
        self.title = title
        self.table_values = [[*self.TABLE_HEADERS], *[[k, *v.values()] for k, v in values.items()]]

    def draw_table(self):
        print(DoubleTable(self.table_values, self.title).table)


def main():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    hh_vacancies_stats = Stats(HeadHunter()).get_stats()
    Table('+HeadHunter Moscow+', hh_vacancies_stats).draw_table()
    try:
        if not os.path.exists(env_path):
            raise FileNotFoundError
        load_dotenv(env_path)
        api_key = os.environ.get('SJ_SECRET_KEY')
        sj_vacancies_stats = Stats(SuperJob(api_key)).get_stats()
        Table('+SuperJob Moscow+', sj_vacancies_stats).draw_table()
    except FileNotFoundError:
        print('.env does not exist')


if __name__ == '__main__':
    main()
