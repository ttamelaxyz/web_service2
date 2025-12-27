# data.py - Имитация хранилища данных для билетов

#изначально набор данных
tickets = [
    {"id": 1, "departure_city": "Москва", "destination_city": "Санкт-Петербург", 
     "transport_type": "поезд", "ticket_price": 2500.0, "travel_time": 4.5, "carrier": "РЖД"},
    {"id": 2, "departure_city": "Москва", "destination_city": "Казань", 
     "transport_type": "самолет", "ticket_price": 5000.0, "travel_time": 1.5, "carrier": "Аэрофлот"},
    {"id": 3, "departure_city": "Новосибирск", "destination_city": "Томск", 
     "transport_type": "автобус", "ticket_price": 800.0, "travel_time": 4.0, "carrier": "СибАвто"},
    {"id": 4, "departure_city": "Екатеринбург", "destination_city": "Челябинск", 
     "transport_type": "автобус", "ticket_price": 600.0, "travel_time": 2.5, "carrier": "УралТранс"},
    {"id": 5, "departure_city": "Сочи", "destination_city": "Краснодар", 
     "transport_type": "поезд", "ticket_price": 1200.0, "travel_time": 3.0, "carrier": "РЖД"},
]

#функции для работы с данными
def get_all_tickets():
    """Возвращает все билеты."""
    return tickets

def get_ticket_by_id(ticket_id):
    """Возвращает билет по его ID или None, если не найден."""
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            return ticket
    return None

def add_new_ticket(ticket_data):
    """Добавляет новый билет. Генерирует новый ID."""
    if not tickets:
        new_id = 1
    else:
        new_id = max(ticket['id'] for ticket in tickets) + 1
    
    # Создаем полный объект билета
    new_ticket = {
        'id': new_id,
        'departure_city': ticket_data.get('departure_city', 'Не указан'),
        'destination_city': ticket_data.get('destination_city', 'Не указан'),
        'transport_type': ticket_data.get('transport_type', 'Не указан'),
        'ticket_price': float(ticket_data.get('ticket_price', 0.0)),
        'travel_time': float(ticket_data.get('travel_time', 0.0)),
        'carrier': ticket_data.get('carrier', 'Не указан')
    }
    
    tickets.append(new_ticket)
    return new_ticket

def update_ticket(ticket_id, updated_data):
    """Обновляет данные билета по ID."""
    ticket = get_ticket_by_id(ticket_id)
    if ticket:
        # Обновляем только переданные поля, кроме ID
        for key, value in updated_data.items():
            if key != 'id' and key in ticket:
                if key in ['ticket_price', 'travel_time']:
                    ticket[key] = float(value)
                else:
                    ticket[key] = value
        return ticket
    return None

def delete_ticket(ticket_id):
    """Удаляет билет по ID. Возвращает True если удалён, False если не найден."""
    global tickets
    for i, ticket in enumerate(tickets):
        if ticket['id'] == ticket_id:
            del tickets[i]
            return True
    return False

def get_statistics():
    """Рассчитывает статистику по числовым полям."""
    if not tickets:
        return None
    
    prices = [t['ticket_price'] for t in tickets]
    times = [t['travel_time'] for t in tickets]
    
    stats = {
        'ticket_price': {
            'min': min(prices),
            'max': max(prices),
            'avg': round(sum(prices) / len(prices), 2),
            'total': len(prices)
        },
        'travel_time': {
            'min': min(times),
            'max': max(times),
            'avg': round(sum(times) / len(times), 2),
            'total': len(times)
        },
        'transport_types': {
            ttype: len([t for t in tickets if t['transport_type'] == ttype])
            for ttype in set(t['transport_type'] for t in tickets)
        },
        'total_tickets': len(tickets)
    }
    return stats