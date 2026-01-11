# app.py
from flask import Flask, jsonify, request
from flasgger import Swagger
from data import tickets

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """
    Получение списка всех билетов
    ---
    responses:
      200:
        description: Список билетов успешно получен
    """
    return jsonify({"tickets": tickets})

@app.route('/api/tickets/<string:city>', methods=['GET'])
def get_tickets_by_city(city):
    """
    Получение стоимости билетов до конкретного города
    ---
    parameters:
      - name: city
        in: path
        type: string
        required: true
        description: Название города
    responses:
      200:
        description: Список билетов до указанного города
      404:
        description: Город не найден
    """
    result = [t for t in tickets if t['destination'].lower() == city.lower()]
    if not result:
        return jsonify({"error": "City not found"}), 404
    return jsonify(result)

@app.route('/api/tickets', methods=['POST'])
def add_ticket():
    """
    Добавление новой информации о стоимости билета
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Ticket
          required:
            - destination
            - transport
            - price
          properties:
            destination:
              type: string
            transport:
              type: string
            price:
              type: integer
    responses:
      201:
        description: Билет успешно добавлен
    """
    new_ticket = request.json
    new_ticket['id'] = len(tickets) + 1
    tickets.append(new_ticket)
    return jsonify(new_ticket), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)