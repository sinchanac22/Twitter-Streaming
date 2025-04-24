# 📄 Twitter Sentiment Analysis Pipeline - README

This project demonstrates a data pipeline using **Kafka**, **Spark Streaming**, and **PostgreSQL** to process and analyze Twitter sentiment data from a CSV dataset.

---

## 📁 Project Structure

```
├── kafka_producer.py        # Sends tweets from CSV to Kafka
├── kafka_consumer.py        # Consumes tweets from Kafka and prints first 50
├── spark_streaming.py       # Processes tweets from Kafka using Spark
├── save_to_postgres.py      # Saves tweets to PostgreSQL database
├── Tweets.csv               # Sample tweet dataset (14,873 records)
├── top_words_chart.png      # Bar chart for top words (batch)
├── tweet_sentiment_chart.png # Sentiment distribution chart
└── README.md                # This file
```

---

## 🛠️ Prerequisites
- Python 3.8+
- Kafka and Zookeeper
- Apache Spark 3.5+
- PostgreSQL
- Python packages:
  ```bash
  pip install kafka-python pandas matplotlib psycopg2-binary
  ```
- Spark Kafka connector (auto-installed via `--packages`)

---

## 🚀 Step-by-Step Setup
cd /mnt/c/Users/sinch/Downloads/kafka_2.13-3.6.1

### 1. Start Kafka and Zookeeper
```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties

# Create Kafka topic
bin/kafka-topics.sh --create --topic tweets_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 2. Run Kafka Producer (send tweets)
```bash
cd /mnt/c/Users/sinch/OneDrive/Documents/dbt
python3 kafka_producer.py
```
*Streams tweets (with a delay) to Kafka topic `tweets_topic`. Only prints the first 50 lines.*

### 3. Run Kafka Consumer (debug/logging)
```bash
python3 kafka_consumer.py
```
*Reads tweets from Kafka and prints the first 50.*

### 4. Run Spark Streaming (real-time processing)
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark_streaming.py
```
*Streams from Kafka, splits tweets into words, and prints word count (top 50).*  


### 5. Setup PostgreSQL Database
```bash
sudo -u postgres psql

-- In psql:
CREATE DATABASE twitter_data;
\c twitter_data
CREATE TABLE tweets (
  id SERIAL PRIMARY KEY,
  tweet_id TEXT,
  user_name TEXT,
  airline TEXT,
  sentiment TEXT,
  text TEXT,
  timestamp TEXT
);
\q
```

### 6. Run PostgreSQL Saver
```bash
python3 save_to_postgres.py
```
*Consumes Kafka messages and saves tweets into `twitter_data.tweets`. Prints only first 50 lines.*

### 7. Query in PostgreSQL
```bash
psql -U postgres -h localhost -d twitter_data

-- Run queries:
SELECT COUNT(*) FROM tweets;
SELECT sentiment, COUNT(*) FROM tweets GROUP BY sentiment;
```

---

## 📊 Visualization Scripts
### A. Bar Chart of Top Words (from batch DB query)
```python
# bar.py
import matplotlib.pyplot as plt
words = ["delay", "flight", "cancelled", "late", "United"]
counts = [15, 13, 11, 10, 9]
plt.bar(words, counts, color='skyblue')
plt.title("Top 5 Words in Tweets (Batch Query)")
plt.savefig("top_words_chart.png")
plt.show()
```

### B. Sentiment Distribution Chart
```python
sentiments = ["negative", "positive", "neutral"]
counts = [20428, 5315, 6962]
plt.bar(sentiments, counts, color=["red", "green", "gray"])
plt.title("Tweet Sentiment Distribution")
plt.savefig("tweet_sentiment_chart.png")
plt.show()
```


#top airlienes
SELECT airline, COUNT(*) AS total
FROM tweets
GROUP BY airline
ORDER BY total DESC;

#sentiment distribution
SELECT sentiment, COUNT(*) AS total
FROM tweets
GROUP BY sentiment;

#most active users
SELECT user_name, COUNT(*) AS tweet_count
FROM tweets
GROUP BY user_name
ORDER BY tweet_count DESC
LIMIT 10;

#top repeated tweets
SELECT * FROM tweets LIMIT 5;

SELECT text, COUNT(*) AS count
FROM tweets
GROUP BY text
ORDER BY count DESC
LIMIT 10;



---

File Name                 	Purpose
kafka_producer.py      	Sends tweets to Kafka
kafka_consumer.py    	Reads tweets from Kafka
spark_streaming.py	   Processes tweets and counts words
save_to_postgres.py   	Stores tweet data in PostgreSQL
batch_analysis.sql	    SQL query for batch processing
report.pdf or .pptx    	Evaluation of streaming vs batch


## 📌 Notes
- Spark output is real-time and updates every few seconds.
- Batch (PostgreSQL) queries are much faster for historical data.
- All printed outputs are limited to first 50 for demonstration.
- Tested with ~14,873 tweets from `Tweets.csv`.

---

## ✅ Final Deliverables
- Scripts: Kafka Producer, Consumer, Spark, PostgreSQL Ingestor
- Visual Charts (PNG)
- SQL Queries + Output
- Performance Comparison (Streaming vs Batch)
- Final Report (see `twitter_kafka_report`)

---

## 🙋 Need Help?
Feel free to open an issue or contact the project author.

> Built with ❤️ by Sinchana

