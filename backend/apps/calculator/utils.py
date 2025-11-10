# import torch
# from transformers import pipeline, BitsAndBytesConfig, AutoProcessor, LlavaForConditionalGeneration
# from PIL import Image

# # quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
# quantization_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.float16
# )


# model_id = "llava-hf/llava-1.5-7b-hf"
# processor = AutoProcessor.from_pretrained(model_id)
# model = LlavaForConditionalGeneration.from_pretrained(model_id, quantization_config=quantization_config, device_map="auto")
# # pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})

# def analyze_image(image: Image):
#     prompt = "USER: <image>\nAnalyze the equation or expression in this image, and return answer in format: {expr: given equation in LaTeX format, result: calculated answer}"

#     inputs = processor(prompt, images=[image], padding=True, return_tensors="pt").to("cuda")
#     for k, v in inputs.items():
#         print(k,v.shape)

#     output = model.generate(**inputs, max_new_tokens=20)
#     generated_text = processor.batch_decode(output, skip_special_tokens=True)
#     for text in generated_text:
#         print(text.split("ASSISTANT:")[-1])

import google.generativeai as genai
import ast
import json
from PIL import Image
from constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
    f"You have been given an image with some mathematical expressions, equations, or graphical problems, and you need to solve them. "
    f"Note: Use the PEMDAS rule for solving mathematical expressions. PEMDAS stands for the Priority Order: Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right). "
    f"For example: "
    f"Q. 2 + 3 * 4 → (3 * 4) = 12, 2 + 12 = 14. "
    f"Q. 2 + 3 + 5 * 4 - 8 / 2 → 5 * 4 = 20, 8 / 2 = 4, 2 + 3 = 5, 5 + 20 = 25, 25 - 4 = 21. "
    f"You may encounter FIVE TYPES of mathematical inputs in the image (only one case applies at a time): "

    # CASE 1
    f"1. **Simple Expressions:** e.g., 2 + 2, 3 * 4, 7 - 8, etc. Solve and return as: "
    f"[{{'expr': given expression, 'result': calculated answer}}]. "

    # CASE 2
    f"2. **Set of Equations:** e.g., x^2 + 2x + 1 = 0, 3y + 4x = 0. Solve for each variable and return as: "
    f"[{{'expr': 'x', 'result': 2, 'assign': True}}, {{'expr': 'y', 'result': 5, 'assign': True}}]. Include one dictionary per variable. "

    # CASE 3 (revised)
    f"3. **Variable Assignment and Derivation:** e.g., x = 4, y = x + 9, z = y - 2, etc. "
    f"In such cases, first check if the expression depends on any previously assigned variable (from earlier lines or from the provided dictionary). "
    f"Then substitute those values and evaluate the result numerically. For example, if x = 4 and y = x + 9, then y = 13. "
    f"Return all such results as a list of dicts, each with this format: "
    f"{{'expr': variable_name, 'result': value, 'assign': True}}. "

    # CASE 4 (you had skipped it accidentally)
    f"4. **Graphical or Word Problems:** These are visual or contextual problems, e.g., trigonometry drawings, distance/time, or physics-based setups. "
    f"Return a single dictionary as: [{{'expr': interpreted_equation, 'result': numeric_answer}}]. "

    # CASE 5
    f"5. **Abstract or Conceptual Images:** The image might represent an abstract concept such as love, jealousy, or invention. "
    f"Return in the same format as others, where 'expr' is your interpretation and 'result' is the inferred concept. "

    # FINAL RULES
    f"Always substitute any variable already stored in the following dictionary before solving: {dict_of_vars_str}. "
    f"Use numeric substitution over symbolic output — never return 'y = x + 9' if x is known; return the evaluated value (e.g., y = 13). "
    f"Return only a Python-parsable list of dictionaries — no text, markdown, or commentary. "
    f"Properly quote all keys and string values for valid parsing with Python's ast.literal_eval."
)

    response = model.generate_content([prompt, img])
    print(response.text)
    answers = []
    try:
        answers = ast.literal_eval(response.text)
    except Exception as e:
        print(f"Error in parsing response from Gemini API: {e}")
    print('returned answer ', answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers