import time 
import json 
import random 
from datetime import datetime
from data_generator import generate_scotsmen_message, generate_bagpipe_message
from kafka import KafkaProducer

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:8098'],
    value_serializer=serializer
)


if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    while True:
        # Generate a message
        monty_python_message = generate_scotsmen_message()
        bagpipe_message = generate_bagpipe_message()
        
        # Send it to our 'scotsmen' topic
        print(f'Producing message @ {datetime.now()} | Message = {str(monty_python_message)}')
        producer.send('scotsmen', monty_python_message)
        
        
        # Send the message to our 'bagpipe' topic
        print(f'Producing message @ {datetime.now()} | Message = {str(bagpipe_message)}')
        producer.send('bagpipe', bagpipe_message)
        
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 11)
        time.sleep(time_to_sleep)