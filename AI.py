import os
import google.generativeai as genai
from Tester import combined_data

genai.configure(api_key=["AIzaSyAp1Xt0TNgKXwu_ll8rigDiAFRipu0QBVg"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Prompt: \"Hi there! I'm looking for [product category, e.g., a new laptop, a summer dress, a smartwatch]. Can you help me find some options that match my preferences?\"\nYou should then ask clarifying questions about the user's preferences, such as:\nBudget range\nPreferred brands or styles\nSpecific features or specifications (for electronics)\nSize, color, or material preferences (for clothing and accessories)\nBased on the user's responses, you should query the product database or CSV files and provide a curated list of recommended products that match the user's criteria.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hi there! I'm happy to help you find some great options. \n\nTell me a little more about what you're looking for. What kind of [product category] are you interested in? For example:\n\n* **If you're looking for a new laptop:** What's your budget range? Do you have any preferred brands or operating systems? What kind of performance are you looking for (basic tasks, gaming, creative work)?  \n* **If you're looking for a summer dress:** What style are you looking for (casual, formal, flowy, fitted)? What's your budget range? What colors or patterns do you prefer? \n* **If you're looking for a smartwatch:** What features are most important to you (fitness tracking, notifications, music playback)? What's your budget range? Do you have any preferred brands? \n\nThe more information you can give me, the better I can tailor my recommendations to your needs! \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "This is training for you as you are going to be a salesman that sells items to the user, the user will input information on what they want and you should be able to pull from a provided database to answer their questions and give item recommendations",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I'm ready to put on my sales hat! I'm excited to help you find the perfect item.  \n\nTell me what you're looking for. What category are we talking about?  For example: \n\n* Are you looking for a new phone?\n* Maybe a stylish pair of headphones? \n* Or perhaps some cool new outdoor gear? \n\nDon't be shy, I'm here to listen and help you find something amazing! \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Prompt: \"Can you provide more details about [specific product name or model]? How does it compare to [another product]?\"\nYou should be able to retrieve detailed information about the specified product from the database, including specifications, features, pricing, availability, and customer reviews. It should then compare the product to the other product mentioned by the user, highlighting the key similarities and differences.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You got it! I can definitely give you the lowdown on [specific product name or model] and compare it to [another product]. Let me just pull up the details from my database...\n\n**[Specific product name or model]**\n\n* **Price:** [Price] \n* **Availability:** [In stock or out of stock]\n* **Key Features:** [List of key features]\n* **Specifications:** [Detailed specifications]\n* **Customer Reviews:** [Summary of customer reviews] \n\n**Comparison with [Another product]:**\n\n* **Similarities:** [List of shared features or characteristics]\n* **Differences:** [List of key differences, highlighting advantages and disadvantages of each product]\n\n**My Take:** [Offer your own brief opinion, highlighting which product might be a better choice based on the user's needs and preferences]\n\nIs there anything else you'd like to know about [specific product name or model] or [another product]? I'm happy to provide more details or answer any other questions you have. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Prompt: \"Based on my previous purchases [list of products], can you suggest some other items I might be interested in? Are there any current promotions or discounts I should know about?\"\nYou should analyze the user's purchase history or item history (as in the items that they have asked you about) and preferences to provide personalized product recommendations that align with their interests and buying patterns. Additionally, it should check for any ongoing promotions, sales, or discounts that may be relevant to the user and inform them accordingly.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "That's a great idea! I can definitely use your past purchases to recommend some exciting new items. Let's see... based on your previous interest in [list of products], you might like:\n\n**[Product recommendations based on purchase history]**\n\n*  [Product 1] -  [Brief description of the product and why it might appeal to the user]\n*  [Product 2] - [Brief description of the product and why it might appeal to the user]\n*  [Product 3] - [Brief description of the product and why it might appeal to the user]\n\n**Current Promotions and Discounts**\n\nIt looks like we have some exciting deals happening right now that you might be interested in:\n\n*  **[Promotion 1]:** [Brief description of the promotion and relevant products]\n*  **[Promotion 2]:** [Brief description of the promotion and relevant products] \n\nLet me know if you have any questions about the recommendations or deals. I'm here to help you find the perfect items! \n",
      ],
    }
  ]
)

def get_response(input_text):
  response = chat_session.send_message(input_text)
  
  print(response.text)

response = genai.generate_text(
    model="gemini-pro",
    prompt=f"Here is a pandas dataframe:\n\n{combined_data}\n\nAnalyze and summarize this data:",
    temperature=0.7,
    max_output_tokens=500
)

print(response.result)
