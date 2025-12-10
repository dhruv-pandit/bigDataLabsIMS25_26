import json 
from kafka import KafkaConsumer

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        "votes",
        bootstrap_servers="localhost:8098",
        auto_offset_reset="earliest"
    )
    for message in consumer:
        print(json.loads(message.value))