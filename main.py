import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

if __name__ == '__main__':

    DSN = 'postgresql://postgres:postgres@localhost:5432/netology_db'
    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)
    session = Session()
    create_tables(engine)
    with open('test_data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    while True:
        response = input('Введите имя издателя: \n')
        for item in session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale). \
                join(Publisher).join(Stock).join(Sale).join(Shop). \
                filter(Publisher.name == response):
            print(f'{item.title} | {item.name} | '
                  f'{str(item.price * item.count)} | {item.date_sale}')

    session.close()