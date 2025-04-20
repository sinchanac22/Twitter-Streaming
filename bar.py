import matplotlib.pyplot as plt

# Real data from your tweets table
sentiments = ["negative", "positive", "neutral"]
counts = [20428, 5315, 6962]

# Create bar chart
plt.bar(sentiments, counts, color=['red', 'green', 'gray'])
plt.title("Tweet Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")

# Save to OneDrive
plt.savefig('/mnt/c/Users/sinch/OneDrive/Documents/tweet_sentiment_chart.png')

# Show the chart
plt.show()
