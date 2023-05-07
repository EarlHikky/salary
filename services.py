import requests

from itertools import count


class HeadHunter:
    AREA = 1  # Moscow
    PERIOD = 30  # Days
    PROFESSIONAL_ROLE = 96  # 'Programmer, developer'
    PER_PAGE = 100
    HH_API_URL = 'https://api.hh.ru/vacancies/'

    @classmethod
    def get_vacancies(cls, language):
        """Get all vacancies for a language from the HeadHunter"""
        params = {'professional_role': cls.PROFESSIONAL_ROLE, 'area': cls.AREA, 'text': language,
                  'period': cls.PERIOD,
                  'per_page': cls.PER_PAGE}
        vacancies_roster = []
        for page in count(0):
            params['page'] = page
            vacancies, available_vacancies_check, vacancies_found = get_response(cls.HH_API_URL, {}, params)
            vacancies_roster.extend(vacancies)
            if page >= available_vacancies_check - 1:
                break
        return vacancies_roster, vacancies_found


class SuperJob:
    TOWN = 4  # Moscow
    PROFESSION = 48  # 'Programmer, developer'
    PER_PAGE = 100
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_vacancies(self, language):
        """Get all vacancies for a language from the SuperJob"""
        vacancies_roster = []
        headers = {'X-Api-App-Id': self.api_key}
        params = {'catalogues': self.PROFESSION, 'keyword': language, 'town': self.TOWN,
                  'count': self.PER_PAGE}
        for page in count(0):
            params['page'] = page
            vacancies, available_vacancies_check, vacancies_found = get_response(self.SJ_API_URL, headers, params)
            vacancies_roster.extend(vacancies)
            if not available_vacancies_check:
                break
        return vacancies_roster, vacancies_found


def get_response(url, headers, params):
    """Get a response from a service"""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    raw_vacancies = response.json()
    vacancies = raw_vacancies.get('items') or raw_vacancies.get('objects')
    vacancies_found = raw_vacancies.get('total') or raw_vacancies.get('found') or 0
    available_vacancies_check = raw_vacancies.get('pages') or raw_vacancies.get('more')
    return vacancies, available_vacancies_check, vacancies_found
