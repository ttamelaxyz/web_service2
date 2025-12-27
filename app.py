# app.py - Основное приложение Flask с REST API и Swagger-документацией
import os
from flask import Flask, render_template, jsonify
from flask_restx import Api, Resource, fields, reqparse
from data import get_all_tickets, get_ticket_by_id, add_new_ticket, update_ticket, delete_ticket, get_statistics

app = Flask(__name__)

# Конфигурация для Render
PORT = int(os.environ.get('PORT', 5000))

# Инициализация API с Swagger
api = Api(app, 
          version='1.0', 
          title='API стоимости билетов',
          description='Документация REST API для управления данными о стоимости билетов между городами',
          doc='/api/docs/',  # Swagger доступен по /api/docs/
          prefix='/api'  #все API эндпоинты будут иметь префикс
          )

#пространство имен для нашего API
ns = api.namespace('tickets', description='Операции с билетами')

#модель данных для билета
ticket_model = api.model('Ticket', {
    'id': fields.Integer(readOnly=True, description='Уникальный идентификатор билета'),
    'departure_city': fields.String(required=True, description='Город отправления'),
    'destination_city': fields.String(required=True, description='Город назначения'),
    'transport_type': fields.String(required=True, description='Тип транспорта (поезд, самолет, автобус)'),
    'ticket_price': fields.Float(required=True, description='Стоимость билета в рублях'),
    'travel_time': fields.Float(required=True, description='Время в пути в часах'),
    'carrier': fields.String(required=True, description='Перевозчик')
})

# Парсер для обработки query-параметров сортировки и фильтрации
ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('sort_by', type=str, help='Поле для сортировки (например, ticket_price)')
ticket_parser.add_argument('order', type=str, choices=['asc', 'desc'], default='asc', help='Порядок сортировки: asc (по возрастанию) или desc (по убыванию)')
ticket_parser.add_argument('transport_type', type=str, help='Фильтрация по типу транспорта')

# Главная страница
@app.route('/')
def home():
    """Главная страница с информацией об API"""
    return render_template('index.html')

#простой эндпоинт для проверки здоровья
@app.route('/health')
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'healthy',
        'service': 'Ticket API',
        'version': '1.0'
    })

#Эндпоинт: Получить список всех билетов с возможностью сортировки и фильтрации
@ns.route('/')
class TicketList(Resource):
    @ns.expect(ticket_parser)  # Документируем возможные query-параметры
    @ns.marshal_list_with(ticket_model)  # Указываем, как форматировать ответ
    def get(self):
        """Получить список всех билетов. Доступна сортировка и фильтрация."""
        args = ticket_parser.parse_args()
        tickets = get_all_tickets()
        
        # Применяем фильтрацию
        if args['transport_type']:
            tickets = [t for t in tickets if t['transport_type'] == args['transport_type']]
        
        # Применяем сортировку
        if args['sort_by']:
            reverse_order = (args['order'] == 'desc')
            try:
                tickets = sorted(tickets, key=lambda x: x[args['sort_by']], reverse=reverse_order)
            except KeyError:
                # Если переданное поле для сортировки не существует, игнорируем сортировку
                pass
        return tickets

    @ns.expect(ticket_model)  # Ожидаем данные в формате ticket_model
    @ns.marshal_with(ticket_model, code=201)  # Возвращаем созданный объект с кодом 201
    def post(self):
        """Добавить новый билет."""
        data = api.payload
        new_ticket = add_new_ticket(data)
        return new_ticket, 201

#Эндпоинт: Работа с конкретным билетом по его ID
@ns.route('/<int:ticket_id>')
@ns.response(404, 'Билет с указанным ID не найден')
@ns.param('ticket_id', 'Уникальный идентификатор билета')
class TicketResource(Resource):
    @ns.marshal_with(ticket_model)
    def get(self, ticket_id):
        """Получить информацию о билете по его ID."""
        ticket = get_ticket_by_id(ticket_id)
        if ticket is None:
            api.abort(404, f"Билет с ID {ticket_id} не найден")
        return ticket

    @ns.expect(ticket_model, validate=False)  # validate=False позволяет обновлять частично
    @ns.marshal_with(ticket_model)
    def put(self, ticket_id):
        """Полностью обновить информацию о билете по ID."""
        ticket = get_ticket_by_id(ticket_id)
        if ticket is None:
            api.abort(404, f"Билет с ID {ticket_id} не найден")
        data = api.payload
        updated_ticket = update_ticket(ticket_id, data)
        return updated_ticket

    @ns.response(204, 'Билет успешно удален')
    def delete(self, ticket_id):
        """Удалить билет по ID."""
        success = delete_ticket(ticket_id)
        if not success:
            api.abort(404, f"Билет с ID {ticket_id} не найден")
        return '', 204

# Эндпоинт: Получить статистику по билетам
@ns.route('/statistics')
class TicketStatistics(Resource):
    def get(self):
        """Получить агрегированную статистику: мин., макс. и среднюю цену и время в пути."""
        stats = get_statistics()
        if stats is None:
            return {"message": "Нет данных для расчета статистики"}, 404
        return stats

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)