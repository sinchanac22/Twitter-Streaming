import psycopg2

# Replace with your actual database credentials
conn = psycopg2.connect(
    dbname="twitter_data",
    user="postgres",
    password="Sinchana@2004",  # 🔒 Replace this
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Example insert — change this to use real tweet data later
cur.execute("INSERT INTO tweets (user_name, tweet) VALUES (%s, %s)", ("Alice", "Hello Kafka!"))

conn.commit()
conn.close()
