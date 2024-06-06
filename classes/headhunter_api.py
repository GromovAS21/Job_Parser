import requests


def get_employers_info(employer_id: list) -> list[dict]:
    """
    Загрузка информации об организациях из HeadHunter'а
    :param employer_id: ID организации
    :return: список организаций
    """
    employer_info = []
    for employer in employer_id:
        response = requests.get(f'https://api.hh.ru/employers/{employer}')
        employer = response.json()
        info = [{
            'id': employer.get('id'),
            'name': employer.get('name'),
            'area': employer.get('area').get('name'),
            'alternate_url': employer.get('alternate_url'),
            'site_url': employer.get('site_url'),
            'open_vacancies': employer.get('open_vacancies')
        }]
        employer_info.extend(info)
    return employer_info
