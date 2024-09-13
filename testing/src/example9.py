import gensim
from gensim import corpora
from gensim.models import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Define and preprocess the text data
existing_notes_texts = [
    "Cars revolutionized transportation, providing speed and convenience. They enable personal mobility, connect distant places, and have become integral to modern life. However, they also contribute to traffic congestion and pollution, highlighting the need for sustainable alternatives and innovations in automotive technology.",
    "Gardens offer a sanctuary of peace and beauty, fostering relaxation and connection with nature. They provide spaces for growing food, supporting wildlife, and improving mental well-being. A well-designed garden can transform any environment, enhancing quality of life and promoting ecological balance.",
    "Self-driving technology promises to reshape transportation by enabling vehicles to navigate and make decisions autonomously. This innovation aims to increase safety, reduce traffic congestion, and enhance efficiency. While still developing, self-driving cars have the potential to transform how we travel and interact with our environment.",
    "SwiftUI is a user interface toolkit by Apple designed for building modern, responsive applications across all Apple platforms. It simplifies UI development with a declarative syntax, allowing developers to create dynamic, adaptable interfaces. SwiftUI integrates seamlessly with Swift, enhancing productivity and streamlining code management.",
    "Ruby on Rails is a full-stack web application framework written in Ruby. It follows the convention over configuration principle, which streamlines development by providing default structures and patterns. Rails supports rapid development, scalability, and a rich ecosystem, making it a popular choice for building robust web applications.",
    "Brussels, the capital of Belgium, is a vibrant city known for its rich history and cultural diversity. It serves as the headquarters for the European Union, influencing international politics and economics. Brussels offers stunning architecture, renowned cuisine, and a lively arts scene, making it a dynamic destination.",
    "Ruby on Rails is a comprehensive web application framework built using Ruby. It adheres to the principle of convention over configuration, simplifying development by offering predefined structures and conventions. Rails promotes rapid development and scalability, coupled with a vibrant ecosystem, making it a favored option for creating powerful and maintainable web applications.",
    "Trees are vital to our planet, offering oxygen, shade, and beauty. They support diverse ecosystems, improve air quality, and combat climate change. Protecting trees is crucial for a healthier Earth.",
    "Jordan Peterson is a Canadian clinical psychologist, professor of psychology, and public intellectual who has gained international recognition for his views on a wide range of topics, including psychology, philosophy, politics, and cultural issues. Born on June 12, 1962, in Alberta, Canada, Peterson earned his B.A. in Political Science from the University of Alberta and his Ph.D. in Clinical Psychology from McGill University. He has been a professor at the University of Toronto since 1998, where he has taught a variety of courses related to psychology and personality.Peterson first garnered significant attention with the publication of his book, Maps of Meaning: The Architecture of Belief (1999). In this work, he explores the relationship between belief systems, mythology, and the structure of meaning in human life. The book delves into the psychological and philosophical underpinnings of how individuals and societies create and interpret meaning, drawing on a range of sources from cognitive science to ancient mythological narratives.His prominence increased dramatically in 2016 with the release of 12 Rules for Life: An Antidote to Chaos. This book combines personal anecdotes, psychological research, and philosophical insights to offer practical advice for living a more meaningful and disciplined life. It addresses topics such as responsibility, personal development, and the pursuit of meaning, and has resonated with a wide audience, leading to significant commercial success. 12 Rules for Life became a bestseller and has been translated into multiple languages, further solidifying Peterson’s status as a significant public figure.Peterson's rise to fame also coincided with his vocal opposition to certain aspects of political correctness and identity politics. His criticism of Canada's Bill C-16, which proposed adding gender identity and gender expression to the list of prohibited grounds for discrimination, brought him substantial media attention. Peterson argued that the bill could infringe upon free speech rights and compel speech in a way that could be problematic. His stance on this issue positioned him as a controversial figure in debates about free speech and social policy.In addition to his academic and literary work, Peterson has been an active public speaker and commentator. He frequently discusses topics related to psychology, self-help, and cultural criticism, often engaging in debates with individuals from various ideological backgrounds. His public lectures and interviews have garnered millions of views, and he has cultivated a significant following on social media platforms.However, Peterson’s career has not been without controversy. Critics accuse him of promoting regressive social views and undermining progressive movements, while his supporters view him as a defender of individual freedoms and traditional values. His critics argue that his approach can sometimes oversimplify complex social issues, while his supporters appreciate his commitment to addressing what they see as important cultural and psychological problems.In recent years, Peterson has faced personal challenges, including health issues and a highly publicized battle with addiction. Despite these struggles, he has continued to engage with his audience and contribute to public discourse. Overall, Jordan Peterson remains a polarizing and influential figure. His work spans the intersection of psychology, philosophy, and cultural criticism, and he continues to be a significant voice in contemporary debates on meaning, responsibility, and societal values."
]

# Preprocess the text
stop_words = set(stopwords.words('english'))
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return tokens

processed_texts = [preprocess(text) for text in existing_notes_texts]

# Create dictionary and corpus for LDA
dictionary = corpora.Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]

# Build LDA model
lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# Extract topics with a threshold
def format_topics(lda_model, corpus, threshold=0.1, num_words=10):
    formatted_topics = []
    for idx, topic in lda_model.print_topics(num_words=num_words):
        words = [word.split('*')[1].strip('" ') for word in topic.split('+')]
        scores = [float(word.split('*')[0]) for word in topic.split('+')]
        filtered_words = [word for word, score in zip(words, scores) if score >= threshold]
        filtered_scores = [score for score in scores if score >= threshold]
        if filtered_words:
            formatted_topic = f"Topic {idx}:\n"
            formatted_topic += "\n".join([f"  {word} (score: {score:.3f})" for word, score in zip(filtered_words, filtered_scores)])
            formatted_topics.append(formatted_topic)
    return "\n\n".join(formatted_topics)

formatted_topics = format_topics(lda_model, corpus, threshold=0.1)
print("LDA Topics and Keywords (with threshold):\n")
print(formatted_topics)

# Extract keywords using TF-IDF with a threshold
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(existing_notes_texts)
feature_names = vectorizer.get_feature_names_out()

def get_keywords(text, vectorizer, feature_names, threshold=0.1, n=10):
    tfidf_vector = vectorizer.transform([text])
    scores = tfidf_vector.toarray()[0]
    filtered_keywords = [(feature_names[i], scores[i]) for i in range(len(scores)) if scores[i] >= threshold]
    sorted_keywords = sorted(filtered_keywords, key=lambda x: x[1], reverse=True)
    return sorted_keywords[:n]

# Print keywords for each document with threshold
print("\nKeywords for each document (with threshold):\n")
for i, text in enumerate(existing_notes_texts):
    keywords = get_keywords(text, vectorizer, feature_names, threshold=0.1)
    print(f"Document {i+1}:\n")
    for word, score in keywords:
        print(f"  {word} (score: {score:.3f})")
    print()
