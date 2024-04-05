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
			channel.queue_declare('item_creation_queue')
			print("Connected to rabbitmq")
			return connection, channel
		except pika.exceptions.AMQPConnectionError:
			print("Failed, retrying in 5sec")
			time.sleep(5)


connection, channel=connect_to_rabbitmq()

def callback(ch, method, properties, body):
	item_data=eval(body)
	print(f"Received item creation request: {item_data}")
	query="insert into items (name, description, price, quantity) values (%s, %s, %s, %s)"
	values=(item_data["name"], item_data["description"], item_data["price"], item_data["quantity"])
	cursor.execute(query, values)
	db.commit()
	print("Item created successfully")

channel.basic_consume(queue="item_creation_queue", on_message_callback=callback, auto_ack=True)
print("Waiting for item creation requests")
channel.start_consuming()

