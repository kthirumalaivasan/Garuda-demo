# import json
# from googletrans import Translator

# # Paths to files
# input_file_path = "datasets/ollama_training.json"
# tamil_output_path = "datasets/tamil.json"
# thanglish_output_path = "datasets/thanglish.json"
# hindi_output_path = "datasets/hindi.json"

# # Initialize the Google Translator
# translator = Translator()

# # Function to translate text
# def translate_text(text, lang_code):
#     try:
#         translatedText = translator.translate(text, lang_code).text
#         print(f"Translation Done")
#         return translatedText
#     except Exception as e:
#         print(f"Error translating '{text}' to '{lang_code}': {e}")
#         return text  # Fallback to original text if translation fails

# # Load the existing dataset
# with open(input_file_path, "r", encoding="utf-8") as file:
#     data = json.load(file)

# # Prepare Tamil, Thanglish, and Hindi datasets
# tamil_data = []
# thanglish_data = []
# hindi_data = []

# for item in data:
#     prompt = item["prompt"]
#     completion = item["completion"]

#     # Translate to Tamil
#     prompt_tamil = translate_text(prompt, "ta")  # 'ta' is the language code for Tamil
#     completion_tamil = translate_text(completion, "ta")
#     tamil_data.append({"prompt": prompt_tamil, "completion": completion_tamil})

#     # Translate to Thanglish (Tamil in Latin script)
#     # prompt_thanglish = translate_text(prompt, "ta-Latn")  # 'ta-Latn' for Thanglish
#     # completion_thanglish = translate_text(completion, "ta-Latn")
#     # thanglish_data.append({"prompt": prompt_thanglish, "completion": completion_thanglish})

#     # Translate to Hindi
#     prompt_hindi = translate_text(prompt, "hi")  # 'hi' is the language code for Hindi
#     completion_hindi = translate_text(completion, "hi")
#     hindi_data.append({"prompt": prompt_hindi, "completion": completion_hindi})

# # Save Tamil dataset
# with open(tamil_output_path, "w", encoding="utf-8") as tamil_file:
#     json.dump(tamil_data, tamil_file, ensure_ascii=False, indent=4)

# # Save Thanglish dataset
# with open(thanglish_output_path, "w", encoding="utf-8") as thanglish_file:
#     json.dump(thanglish_data, thanglish_file, ensure_ascii=False, indent=4)

# # Save Hindi dataset
# with open(hindi_output_path, "w", encoding="utf-8") as hindi_file:
#     json.dump(hindi_data, hindi_file, ensure_ascii=False, indent=4)

# print("Translation completed!")
# print(f"Tamil dataset saved to: {tamil_output_path}")
# print(f"Thanglish dataset saved to: {thanglish_output_path}")
# print(f"Hindi dataset saved to: {hindi_output_path}")


import json
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Define paths for the output files
output_paths = {
    'tamil': 'datasets/tamil.json',
    'thanglish': 'datasets/thanglish.json',
    'hindi': 'datasets/hindi.json'
}

# Function to translate the text
def translate_text(text, dest_language):
    try:
        return translator.translate(text, dest=dest_language).text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text in case of error

# Load the dataset
with open('datasets/ollama_training.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare dictionaries to store the translated data
translated_data_tamil = []
translated_data_thanglish = []
translated_data_hindi = []

# Loop through each item and translate
for item in data:
    # Translate prompt
    prompt_tamil = translate_text(item.get('prompt', ''), 'ta')
    prompt_thanglish = translate_text(item.get('prompt', ''), 'ta')  # Transliteration for Thanglish
    prompt_hindi = translate_text(item.get('prompt', ''), 'hi')

    # Translate completion if exists
    completion_tamil = translate_text(item.get('completion', ''), 'ta')
    completion_thanglish = translate_text(item.get('completion', ''), 'ta')  # Transliteration for Thanglish
    completion_hindi = translate_text(item.get('completion', ''), 'hi')

    # Append translated items to respective lists
    translated_data_tamil.append({
        'prompt': prompt_tamil,
        'completion': completion_tamil
    })
    translated_data_thanglish.append({
        'prompt': prompt_thanglish,
        'completion': completion_thanglish
    })
    translated_data_hindi.append({
        'prompt': prompt_hindi,
        'completion': completion_hindi
    })

    # Save after each translation
    with open(output_paths['tamil'], 'w', encoding='utf-8') as file:
        json.dump(translated_data_tamil, file, ensure_ascii=False, indent=4)

    with open(output_paths['thanglish'], 'w', encoding='utf-8') as file:
        json.dump(translated_data_thanglish, file, ensure_ascii=False, indent=4)

    with open(output_paths['hindi'], 'w', encoding='utf-8') as file:
        json.dump(translated_data_hindi, file, ensure_ascii=False, indent=4)

    print(f"Translated data saved for prompt: {item.get('prompt')}")

print("Translation and saving completed!")
