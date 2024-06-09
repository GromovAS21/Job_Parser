from classes.db_Manager import DB_Manager
from fnc.functions import get_employers_and_vacancies_info, create_database, save_data_in_database
from fnc.config import config


def main():
    """
    Запуск скрипта программы
    """
    # ID организаций для выгрузки информации по ним
    employers_id = [1740, 78638, 3529, 4181, 740, 80, 39305, 907345, 49357, 1942330]
    data = get_employers_and_vacancies_info(employers_id)
    db_name = 'headhunter'
    params = config()
    create_database(db_name, params)
    save_data_in_database(db_name, params, data)

    # Код для проверки работоспособности методов класса
    # db_manager = DB_Manager(db_name, params)
    # db_manager.get_companies_and_vacancies_count()
    # db_manager.get_all_vacancies()
    # db_manager.get_avg_salary()
    # db_manager.get_vacancies_with_higher_salary()
    # keyword = input("Введите слово: ")
    # db_manager.get_vacancies_with_keyword(keyword)


if __name__ == '__main__':
    main()