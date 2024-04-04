from flask import Flask, request, render_template
import pika
import time

app=Flask(__name__)

def connect_to_rabbitmq():
    connection=None
    while connection is None:
        try: 
            connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel=connection.channel()
            channel.queue_declare(queue='health_check_queue')
            channel.queue_declare(queue='item_creation_queue')
            channel.queue_declare(queue='order_processing_queue')
            channel.queue_declare(queue='stock_management_queue')
            print("Connected to rabbitmq")
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect, retrying in 5 sec")
            time.sleep(5)
    return connection, channel

connection, channel=connect_to_rabbitmq()

@app.route('/') 
def home():
    return render_template('producer.html')

@app.route('/health_check', methods=['GET'])
def health_check():
    channel.basic_publish(exchange='', routing_key='health_check_queue',  body='Health check request')
    return 'Health check request sent'

@app.route('/items', methods=['POST'])
def create_item():
    data={
        'name': request.form["name"], 
        'description:': request.form["description"], 
        'price': float(request.form["price"])
    }
    channel.basic_publish(exchange='', routing_key='item_creation_queue', body=str(data))
    return 'Item creation request sent'

@app.route('/stock', methods=['PUT'])
def stock_update():
    data = {
        'item_id': int(request.form["item_id"]), 
        'quantity': int(request.form["quantity"])
    }
    channel.basic_publish(exchange='', routing_key='stock_management_queue', body=str(data))
    return 'Stock update request sent'

@app.route('/orders', methods=['POST'])
def order_process():
    items = {
        'item_id': int(request.form["item[0][item_id]"]), 
        'quantity': int(request.form["item[0][quantity]"])
    }
    data = {
        'items': items,
        'customer_name': request.form["customer_name"], 
        'shipping_address': request.form["shipping_address"]
    }
    channel.basic_publish(exchange='', routing_key='order_processing_queue', body=str(data))
    return 'Order request sent'
    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)