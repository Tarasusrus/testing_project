# Импортируем FastAPI и HTTPException из модуля fastapi
from fastapi import FastAPI, HTTPException

# Создаем экземпляр FastAPI
app = FastAPI()


# Определяем обработчик POST-запроса для маршрута "/calculate/"
@app.post('/calculate/')
async def calculate_numbers(num_1: int, num_2: int):
    try:
        # Вычисляем сумму двух чисел, переданных в параметрах запроса
        result = num_1 + num_2
        # Возвращаем результат в формате JSON
        return {'result': result}
    except Exception as e:
        # Если возникла ошибка во время вычислений, выбрасываем исключение HTTPException
        # с кодом состояния 500 (внутренняя ошибка сервера) и детальным сообщением об ошибке
        raise HTTPException(status_code=500, detail=str(e))
