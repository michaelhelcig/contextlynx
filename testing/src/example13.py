from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

def load_model(model_name="EleutherAI/gpt-j-6B"):
    """
    Load a local LLM model and tokenizer using transformers.
    
    Args:
    - model_name (str): The model identifier from the Hugging Face model hub.
    
    Returns:
    - pipeline: A text-generation pipeline.
    """
    print(f"Loading model: {model_name}... This may take a while.")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True)
    text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return text_generator

def extract_topics(text, existing_topics, text_generator, max_length=100):
    """
    Extract new topics from a given text and compare them with existing topics.
    
    Args:
    - text (str): The input text for topic extraction.
    - existing_topics (list): A list of existing topics to match against.
    - text_generator (pipeline): The text-generation pipeline for the LLM.
    - max_length (int): Maximum length of generated text.

    Returns:
    - dict: A dictionary with 'new_topics' and 'matched_topics'.
    """
    # Create a prompt for topic extraction
    prompt = f"Extract the main topics from the following text:\n\n{text}\n\nTopics should be returned as a comma-separated list."
    
    # Generate response using the LLM
    response = text_generator(prompt, max_length=max_length, do_sample=True, top_k=50)[0]["generated_text"]
    
    # Extract generated topics from response
    extracted_text = response.split("\n")[-1]  # Get last line which contains topics
    extracted_topics = [topic.strip() for topic in extracted_text.split(",")]

    # Determine new and matched topics
    matched_topics = [topic for topic in extracted_topics if topic in existing_topics]
    new_topics = [topic for topic in extracted_topics if topic not in existing_topics]

    return {"new_topics": new_topics, "matched_topics": matched_topics}

def main():
    # Load the model
    text_generator = load_model()

    # Example text and existing topics
    text = "Machine learning is a subset of artificial intelligence that focuses on training computers to learn from data. Deep learning is a specialized branch of machine learning."
    existing_topics = ["artificial intelligence", "neural networks", "deep learning"]

    # Extract topics using the local LLM
    result = extract_topics(text, existing_topics, text_generator)

    print("Matched Topics:", result["matched_topics"])
    print("New Topics:", result["new_topics"])

if __name__ == "__main__":
    main()
