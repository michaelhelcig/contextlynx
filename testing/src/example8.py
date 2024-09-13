from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')

# Sample text
texts = [
    "The new advancements in technology are revolutionizing the transportation and health industries.",
    "Recent scientific breakthroughs in environmental studies are noteworthy.",
    "Elon Musk's innovations in space travel and electric vehicles are significant.",
    "The impact of climate change on agriculture and economy is a growing concern."
]

# Preprocess the text
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(texts)

# Perform K-Means clustering
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)

# Print cluster centers
print("Cluster centers:")
for i, center in enumerate(kmeans.cluster_centers_):
    print(f"Cluster {i}: {', '.join([vectorizer.get_feature_names_out()[index] for index in center.argsort()[-10:]])}")

# Assign texts to clusters
labels = kmeans.labels_
for i, label in enumerate(labels):
    print(f"Text {i} is in cluster {label}")
