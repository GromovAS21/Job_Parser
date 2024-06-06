import requests


def get_employers_and_vacancies_info(employers_id: list) -> list[dict]:
    """
    Загрузка информации об организациях из HeadHunter'а
    :param employers_id: ID организации
    :return: список с организациями и их вакансиями
    """
    data = []
    for employer_id in employers_id:
        response_1 = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        employer = response_1.json()
        employer_info = {
            'id': employer.get('id'),
            'name': employer.get('name'),
            'area': employer.get('area').get('name'),
            'alternate_url': employer.get('alternate_url'),
            'site_url': employer.get('site_url'),
            'open_vacancies': employer.get('open_vacancies')
        }

        vacancies_list = []
        params = {'text': '', 'page': 0, 'per_page': '100', 'employer_id': employer_id}
        while params['page'] != 1:
            response_2 = requests.get(f'https://api.hh.ru/vacancies', params=params)
            vacancies = response_2.json()['items']
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
                vacancies_list.append(vacancy_info)
            params['page'] += 1
        data.append({
            'employer': employer_info,
            'vacancies': vacancies_list
        })
    return data
