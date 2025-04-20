from kafka import KafkaConsumer
import json

# Setup Kafka consumer
consumer = KafkaConsumer(
    'tweets_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='tweet_group',
    auto_offset_reset='earliest'
)

print("Listening for messages...\n")

for i, message in enumerate(consumer):
    if i < 50:
        tweet = message.value
        print(f"[{tweet.get('timestamp')}] {tweet.get('user')} ({tweet.get('airline')}) - {tweet.get('sentiment')}")
        print(f"Tweet: {tweet.get('text')}\n")

