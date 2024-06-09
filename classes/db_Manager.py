import psycopg2


class DB_Manager:
    """
    Класс для выборки из базы данных
    """
    __slots__ = ('__db_name', '__params')

    def __init__(self, db_name, params: dict):
        """
        Инициализация класса DB_Manager
        :param db_name: название базы данных
        :param params: параметры базы данных
        """
        self.__db_name = db_name
        self.__params = params

    def get_companies_and_vacancies_count(self):
        """
        Получение списка всех компаний и количество вакансий у каждой компании
        :return:
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT employer_name, COUNT(*) FROM employers
                            JOIN vacancies USING(id_employer)
                            GROUP BY employer_name
                            """)
                print(cur.fetchall())
        conn.close()

    def get_all_vacancies(self):
        """
        Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT vacancy_name, employer_name, salary, currency, url_vacancy FROM vacancies
                            JOIN employers USING(id_employer)
                            """)
                print(cur.fetchall())
        conn.close()

    def get_avg_salary(self):
        """
        Получение средней зарплаты по вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary)::INT FROM vacancies")
                print(cur.fetchall()[0][0])
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT vacancy_name, salary FROM vacancies
                            WHERE salary > (SELECT AVG(salary) FROM vacancies)
                            ORDER BY salary DESC
                            """)
                print(cur.fetchall())
        conn.close()

    def get_vacancies_with_keyword(self, word):
        """
        Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                        SELECT * FROM vacancies
                        WHERE vacancy_name LIKE '%{word}%'
                        """)
                print(cur.fetchall())
        conn.close()
