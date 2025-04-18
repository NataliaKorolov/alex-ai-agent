import PyPDF2
import os
import ast
from openai import OpenAI

# Load OpenAI client
client_for_pdf_parsing = OpenAI(api_key=os.getenv("OPENAI_API_KEY_FOR_PDF_PARSING"))

def read_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_services_from_pdf_text(pdf_text):
    extract_prompt = f"""
You are a helpful assistant reading a salon price list.

From the following PDF text, extract ONLY the names of services (no prices), as a clean Python list. 

Here is the text:
---
{pdf_text}
---
Return just the list like: [\"Lash Lift\", \"Volume Fill\", \"Lash Removal\"]
"""

    response = client_for_pdf_parsing.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from text."},
            {"role": "user", "content": extract_prompt}
        ]
    )

    return ast.literal_eval(response.choices[0].message.content)

# Example usage:
if __name__ == "__main__":
    pdf_text = read_pdf("Delightful_Lashes_Price_List.pdf")
    services = extract_services_from_pdf_text(pdf_text)
    print("Extracted services:", services)
