import pika
import pymysql
import time

db=pymysql.connect(
	host='host.docker.internal', 
	user='root', 
	password='coleadonis23#J', 
	db='ims'
	)

cursor=db.cursor()

def connect_to_rabbitmq():
	connection=None
	while connection is None:
		try:
			connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
			channel=connection.channel()
			channel.queue_declare('stock_management_queue')
			print("Connected to rabbitmq")
			return connection, channel
		except pika.exceptions.AMQPConnectionError:
			print("Failed, retrying in 5sec")
			time.sleep(5)


connection, channel=connect_to_rabbitmq()

def callback(ch, method, properties, body):
	stock_data=eval(body)
	print(f"Received stock update data: {stock_data}")
	query="update items set quantity = %s where id = %s"
	values=(stock_data["quantity"], stock_data["item_id"])
	cursor.execute(query, values)
	db.commit()
	print("Stock updated successfully")

channel.basic_consume(queue='stock_management_queue', on_message_callback=callback, auto_ack=True)
print("Stock management queue ready, waiting for requests")
channel.start_consuming()