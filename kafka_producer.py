from kafka import KafkaProducer
import pandas as pd
import json
import time

# Load dataset
df = pd.read_csv('Tweets.csv')  # Ensure the path is correct

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Sending tweets to Kafka...\n")

# Stream tweets
for i, (_, row) in enumerate(df.iterrows()):
    tweet = {
    "tweet_id": row['tweet_id'],
    "user": row['name'],
    "airline": row['airline'],
    "sentiment": row['airline_sentiment'],
    "text": row['text'],
    "timestamp": row['tweet_created']
}

    producer.send('tweets_topic', value=tweet)

    # Only print first 50 messages
    if i < 50:
        print(f"Sent tweet ID: {tweet['tweet_id']}")

    time.sleep(0.1)  # Simulate stream speed
