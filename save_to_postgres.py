from kafka import KafkaConsumer
import psycopg2
import json

# Set up Kafka consumer
consumer = KafkaConsumer(
    'tweets_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='postgres_writer',
    auto_offset_reset='earliest'
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="twitter_data",
    user="postgres",
    password="Sinchana@2004",     # Replace with your password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

print("Saving tweets to PostgreSQL...\n")

for i, message in enumerate(consumer):
    tweet = message.value
    try:
        cur.execute(
            "INSERT INTO tweets (tweet_id, user_name, airline, sentiment, text, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                tweet.get("tweet_id"),
                tweet.get("user"),
                tweet.get("airline"),
                tweet.get("sentiment"),
                tweet.get("text"),
                tweet.get("timestamp")
            )
        )
        conn.commit()
        if i < 50:
            print("RAW TWEET:", tweet)
    except Exception as e:
        print(f"❌ Error saving tweet: {e}")
        conn.rollback()

# Close connection (optional if you plan to exit after some time)
# cur.close()
# conn.close()
