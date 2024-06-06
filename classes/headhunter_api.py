import requests


def get_employers_info(employer_id: int) -> dict:
    """
    Загрузка информации об организациях из HeadHunter'а
    :param employer_id: ID организации
    :return: словарь с информацией об организации
    """
    response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
    employer = response.json()
    employer_info = {
        'id': employer.get('id'),
        'name': employer.get('name'),
        'area': employer.get('area').get('name'),
        'alternate_url': employer.get('alternate_url'),
        'site_url': employer.get('site_url'),
        'open_vacancies': employer.get('open_vacancies')
    }
    return employer_info


def get_employers_vacancies(employer_id: int):
    """
    Загрузка информации об имеющихся вакансиях у организаций с HH
    :param employer_id: ID организации
    :return: список с вакансиями
    """
    vacancies_list = []
    params = {'text': '', 'page': 0, 'per_page': '100', 'employer_id': employer_id}
    while params['page'] != 20:
        response = requests.get(f'https://api.hh.ru/vacancies', params=params)
        vacancies = response.json()['items']
        for vacancy in vacancies:
            vacancy_info = {
                'id': vacancy.get('id'),
                'vacancy': vacancy.get('name'),
                'published_at': vacancy.get('published_at'),
                'employment': vacancy.get('employment').get('name'),
                'schedule': vacancy.get('schedule').get('name'),
                'type': vacancy.get('type').get('name'),
                'area': vacancy.get('area').get('name')
            }
            vacancies_list.extend([vacancy_info])
        params['page'] += 1
    return vacancies_list
