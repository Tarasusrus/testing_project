import datetime
import unittest


import requests

from services import sheet


class UserAPITest(unittest.TestCase):
    base_url = 'https://reqres.in/api/users'

    def update_test_results(self, expected_result, actual_result):
        """
        Обновляет таблицу Google Sheets с результатами тестов.
        """
        test_name = f"{self.__class__.__name__}.{self._testMethodName}"
        test_method = getattr(self, self._testMethodName)
        docstring = test_method.__doc__ if test_method.__doc__ else ""  # Получаем докстринг теста

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на совпадение имени теста в первой строке
        if sheet.cell(1, 1).value != "Test Name":
            headers = ["Test Name", "Description", "Expected Result", "Actual Result", "Date"]
            sheet.insert_row(headers, index=1)

        # Вставка данных
        data = [test_name, docstring, expected_result, actual_result, current_datetime]
        sheet.insert_row(data, index=2)

    def test_get_user(self):
        """
        Тест на получение пользователя.
        """
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200, 'Ожидался статус-код 200 (OK), но получен другой статус-код.')
        self.update_test_results(200, response.status_code)

    def test_get_list_users(self):
        """
        Тест на получение списка пользователей.
        """
        response = requests.get(self.base_url + '?page=2')
        self.assertEqual(response.status_code, 200, 'Ожидался статус-код 200 (OK), но получен другой статус-код.')
        self.update_test_results(200, response.status_code)


    def test_get_single_user(self):
        """
        Тест на получение информации о конкретном пользователе.
        """
        response = requests.get(self.base_url + '/2')
        self.assertEqual(response.status_code, 200, 'Ожидался статус-код 200 (OK), но получен другой статус-код.')
        self.update_test_results(200, response.status_code)

    def test_get_single_user_not_find(self):
        """
        Тест на получение информации о несуществующем пользователе.
        """
        response = requests.get(self.base_url + '/23')
        self.assertEqual(response.status_code, 404, 'Ожидался статус-код 404 (Not Found), но получен другой статус-код.')
        self.update_test_results(404, response.status_code)

        response = requests.get(self.base_url + '/233')
        self.assertEqual(response.status_code, 404, 'Ожидался статус-код 404 (Not Found), но получен другой статус-код.')
        self.update_test_results(404, response.status_code)

        response = requests.get(self.base_url + '/0')
        self.assertEqual(response.status_code, 404, 'Ожидался статус-код 404 (Not Found), но получен другой статус-код.')
        self.update_test_results(404, response.status_code)


class TestUserRegistration(unittest.TestCase):
    base_url = 'https://reqres.in/api/users'

    def update_test_results(self, expected_result, actual_result):
        """
        Обновляет таблицу Google Sheets с результатами тестов.
        """
        test_name = f"{self.__class__.__name__}.{self._testMethodName}"
        test_method = getattr(self, self._testMethodName)
        docstring = test_method.__doc__ if test_method.__doc__ else ""  # Получаем докстринг теста

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на совпадение имени теста в первой строке
        if sheet.cell(1, 1).value != "Test Name":
            headers = ["Test Name", "Description", "Expected Result", "Actual Result", "Date"]
            sheet.insert_row(headers, index=1)

        # Вставка данных
        data = [test_name, docstring, expected_result, actual_result, current_datetime]
        sheet.insert_row(data, index=2)

    def test_successful_registration(self):
        """
        Тест на успешную регистрацию нового пользователя.
        """
        data = {
            "name": "morpheus",
            "job": "leader"
        }
        response = requests.post(self.base_url, json=data)
        expected_result = 201
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 201 (Created), но получен другой статус-код.')
        self.assertIn("name", response.json(), 'Ответ сервера не содержит поле "name".')
        self.assertIn("job", response.json(), 'Ответ сервера не содержит поле "job".')
        self.assertIn("id", response.json(), 'Ответ сервера не содержит поле "id".')
        self.assertIn("createdAt", response.json(), 'Ответ сервера не содержит поле "createdAt".')

    def test_empty_request(self):
        """
        Тест на отправку пустого запроса.
        """
        response = requests.post(self.base_url, json={})
        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 400 (Bad Request), но получен другой статус-код.')

    def test_duplicate_registration(self):
        """
        Тест на попытку повторной регистрации с теми же данными.
        """
        data = {
            "name": "morpheus",
            "job": "leader"
        }
        # Первая регистрация
        response1 = requests.post(self.base_url, json=data)
        # Повторная регистрация
        response2 = requests.post(self.base_url, json=data)

        expected_result = 409
        actual_result = response2.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 409 (Conflict) из-за попытки повторной регистрации, но получен другой статус-код.')

    def test_long_name_and_job(self):
        """
        Тест на отправку запроса с очень длинными данными имени и работы.
        """
        data = {
            "name": "a" * 10000,
            "job": "b" * 10000
        }
        response = requests.post(self.base_url, json=data)

        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 400 (Bad Request) из-за длинных данных имени и работы, но получен другой статус-код.')


class TestUserUpdate(unittest.TestCase):
    base_url = 'https://reqres.in/api'
    user_id = 2

    def update_test_results(self, expected_result, actual_result):
        """
        Обновляет таблицу Google Sheets с результатами тестов.
        """
        test_name = f"{self.__class__.__name__}.{self._testMethodName}"
        test_method = getattr(self, self._testMethodName)
        docstring = test_method.__doc__ if test_method.__doc__ else ""  # Получаем докстринг теста

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на совпадение имени теста в первой строке
        if sheet.cell(1, 1).value != "Test Name":
            headers = ["Test Name", "Description", "Expected Result", "Actual Result", "Date"]
            sheet.insert_row(headers, index=1)

        # Вставка данных
        data = [test_name, docstring, expected_result, actual_result, current_datetime]
        sheet.insert_row(data, index=2)

    def test_successful_update(self):
        """
        Тест на успешное обновление данных пользователя.
        """
        data = {
            "name": "morpheus",
            "job": "zion resident"
        }
        response = requests.put(f"{self.base_url}/users/{self.user_id}", json=data)
        expected_result = 200
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (OK), '
                         f'но получен статус-код {actual_result}.')
        self.assertIn("name", response.json(), 'Ответ сервера не содержит поле "name".')
        self.assertIn("job", response.json(), 'Ответ сервера не содержит поле "job".')
        self.assertIn("updatedAt", response.json(), 'Ответ сервера не содержит поле "updatedAt".')

    def test_update_with_empty_data(self):
        """
        Тест на обновление пользователя с пустыми данными.
        """
        response = requests.put(f"{self.base_url}/users/{self.user_id}", json={})
        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 400 (Bad Request), '
                         'но получен другой статус-код.')

    def test_update_with_long_data(self):
        """
        Тест на обновление пользователя с очень длинными данными имени и работы.
        """
        data = {
            "name": "a" * 10000,
            "job": "b" * 10000
        }
        response = requests.put(f"{self.base_url}/users/{self.user_id}", json=data)
        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         'Ожидался статус-код 400 (Bad Request) из-за длинных данных имени и работы, '
                         'но получен другой статус-код.')


class TestUserPatch(unittest.TestCase):
    base_url = 'https://reqres.in/api'
    user_id = 2

    def update_test_results(self, expected_result, actual_result):
        """
        Обновляет таблицу Google Sheets с результатами тестов.
        """
        test_name = f"{self.__class__.__name__}.{self._testMethodName}"
        test_method = getattr(self, self._testMethodName)
        docstring = test_method.__doc__ if test_method.__doc__ else ""  # Получаем докстринг теста

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на совпадение имени теста в первой строке
        if sheet.cell(1, 1).value != "Test Name":
            headers = ["Test Name", "Description", "Expected Result", "Actual Result", "Date"]
            sheet.insert_row(headers, index=1)

        # Вставка данных
        data = [test_name, docstring, expected_result, actual_result, current_datetime]
        sheet.insert_row(data, index=2)

    def test_successful_update(self):
        """
        Тест на успешное обновление данных пользователя.
        """
        data = {
            "name": "morpheus",
            "job": "zion resident"
        }
        response = requests.patch(f"{self.base_url}/users/{self.user_id}", json=data)
        expected_result = 200
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (OK), но получен статус-код {actual_result}.')
        self.assertIn("name", response.json(), 'Ответ сервера не содержит поле "name".')
        self.assertIn("job", response.json(), 'Ответ сервера не содержит поле "job".')
        self.assertIn("updatedAt", response.json(), 'Ответ сервера не содержит поле "updatedAt".')

    def test_update_with_empty_data(self):
        """
        Тест на обновление пользователя с пустыми данными.
        """
        response = requests.patch(f"{self.base_url}/users/{self.user_id}", json={})
        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (Bad Request) из-за отсутствия данных, '
                         f'но получен статус-код {actual_result}. Ответ сервера: {response.json()}')

    def test_update_with_long_data(self):
        """
        Тест на обновление пользователя с длинными данными.
        """
        data = {
            "name": "a" * 10000,
            "job": "b" * 10000
        }
        response = requests.patch(f"{self.base_url}/users/{self.user_id}", json=data)
        expected_result = 400
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (Bad Request) из-за длинных данных, '
                         f'но получен статус-код {actual_result}.')


class TestUserDelete(unittest.TestCase):
    base_url = 'https://reqres.in/api'
    user_id = 2
    nonexistent_user_id = 10000

    import datetime

    def update_test_results(self, expected_result, actual_result):
        """
        Обновляет таблицу Google Sheets с результатами тестов.
        """
        test_name = f"{self.__class__.__name__}.{self._testMethodName}"
        test_method = getattr(self, self._testMethodName)
        docstring = test_method.__doc__ if test_method.__doc__ else ""  # Получаем докстринг теста

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на совпадение имени теста в первой строке
        if sheet.cell(1, 1).value != "Test Name":
            headers = ["Test Name", "Description", "Expected Result", "Actual Result", "Date"]
            sheet.insert_row(headers, index=1)

        # Вставка данных
        data = [test_name, docstring, expected_result, actual_result, current_datetime]
        sheet.insert_row(data, index=2)

    def test_delete_user(self):
        """
        Тест на удаление пользователя.
        """
        response = requests.delete(f"{self.base_url}/users/{self.user_id}")
        expected_result = 204
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (No Content), но получен статус-код {actual_result}.')

    def test_delete_nonexistent_user(self):
        """
        Тест на попытку удаления несуществующего пользователя.
        """

        response = requests.delete(f"{self.base_url}/users/{self.nonexistent_user_id}")
        expected_result = 404
        actual_result = response.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (Not Found), но получен статус-код {actual_result}.')

    def test_delete_user_twice(self):
        """
        Тест на попытку удаления одного и того же пользователя дважды.
        """
        response1 = requests.delete(f"{self.base_url}/users/{self.user_id}")
        response2 = requests.delete(f"{self.base_url}/users/{self.user_id}")

        expected_result = 404
        actual_result = response2.status_code

        self.update_test_results(expected_result, actual_result)

        self.assertEqual(actual_result, expected_result,
                         f'Ожидался статус-код {expected_result} (Not Found) из-за попытки удаления уже удаленного пользователя, '
                         f'но получен статус-код {actual_result}.')
