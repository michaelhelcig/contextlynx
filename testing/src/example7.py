from transformers import pipeline

# Define more general categories
general_categories = [
    "Technology", "Environment", "Transportation", "Health",
    "Science", "Culture", "History", "Business", "Education",
    "Politics", "Entertainment", "Sports", "Economics", "Cars", "Elon Musk"
]

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification")

def extract_categories(text, candidate_labels, top_n=3):
    # Classify the text into the candidate categories
    result = classifier(text, candidate_labels)
    
    # Extract categories and scores
    categories = result['labels']
    scores = result['scores']
    
    # Combine categories with their scores
    category_scores = dict(zip(categories, scores))
    
    # Sort categories by score in descending order and select the top_n
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:top_n]
    
    return top_categories

# Example usage
text = "The new electric vehicles are driving innovation in the automotive industry and contributing to environmental sustainability."
top_n = 3  # Number of top categories to extract

# Extract the top categories for the text
top_categories = extract_categories(text, general_categories, top_n)

# Output the results
print("Text:", text)
print("Top Categories:")
for category, score in top_categories:
    print(f"{category}: {score:.4f}")
