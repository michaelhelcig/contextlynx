from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from difflib import get_close_matches

# Initialize the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def get_llm_response(prompt):
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors='pt', truncation=True)
    
    # Generate the output using the model
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs['input_ids'],
            max_length=500,
            num_return_sequences=1
        )
    
    # Decode the output
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def generate_prompt(text, existing_categories):
    prompt = f"""
    Given the following text:

    "{text}"

    Extract relevant categories or topics that represent the main themes or subjects discussed in the text. Provide a list of these categories.

    Then, match each extracted category to the most appropriate existing category from the list below. If a category does not fit any existing category, you can label it as 'Other'.

    Existing Categories:
    {', '.join(existing_categories)}

    Provide the matched categories in the following format:

    Extracted Categories:
    - Category1: ExistingCategory1
    - Category2: ExistingCategory2
    - ...

    Where each extracted category is mapped to one of the existing categories.
    """
    return prompt

def map_to_existing_categories(extracted_categories, existing_categories):
    category_mapping = {}
    for category in extracted_categories:
        match = get_close_matches(category, existing_categories, n=1, cutoff=0.6)
        if match:
            category_mapping[category] = match[0]
        else:
            category_mapping[category] = 'Other'
    return category_mapping

def main():
    # Define existing categories
    existing_categories = [
        "Technology", "Environment", "Business", "Health", "History",
        "Education", "Culture", "Science", "Arts", "Politics"
    ]

    # Example text
    text = """
    The rapid advancement in technology has led to new innovations in fields such as artificial intelligence and machine learning.
    Environmental issues like climate change and pollution are becoming increasingly urgent. Companies like Tesla and Google are leading the way in developing new technologies.
    """

    # Generate prompt and get LLM response
    prompt = generate_prompt(text, existing_categories)


    response = get_llm_response(prompt)

    
    print("Response from LLM:")
    print(response)

    exit()

    # Extract categories from LLM response
    extracted_lines = [line.strip() for line in response.split('\n') if line.startswith('-')]
    extracted_categories = [line.split(':')[0].strip() for line in extracted_lines]

    # Map to existing categories
    mapped_categories = map_to_existing_categories(extracted_categories, existing_categories)
    
    print("Mapped Categories:")
    for extracted, mapped in mapped_categories.items():
        print(f"{extracted}: {mapped}")

if __name__ == "__main__":
    main()
