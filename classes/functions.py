from typing import Any
import psycopg2
import requests


def get_employers_and_vacancies_info(employers_id: list[int]) -> list[dict[str, Any]]:
    """
    Загрузка информации об организациях и имеющихся у них вакансий из HeadHunter'а
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
        while params['page'] != 1:  # Изменяемый параметр, в зависимости от объема выводимых вакансий
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


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц employers, vacancies
    :param database_name: название создаваемой базы
    :param params: Настройки базы данных
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE employers (
                id_employer INT UNIQUE PRIMARY KEY,
                employer_name VARCHAR(50) NOT NULL,
                area VARCHAR(50),
                employer_page VARCHAR(100),
                employer_website VARCHAR(100),
                open_vacancies INT
                );
            ''')
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE vacancies (
                id_vacancy INT UNIQUE PRIMARY KEY,
                id_employer INT REFERENCES employers(id_employer),
                vacancy_name VARCHAR(255) NOT NULL,
                published_at DATE,
                employment VARCHAR(50),
                schedule VARCHAR(50),
                type VARCHAR(50),
                area VARCHAR(50)
                );
            ''')
    conn.close()






