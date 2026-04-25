from openai import OpenAI
import csv
import time

API_KEY = "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"  

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

PROMPT = """
Ты — анализатор отзывов на протеин. Проанализируй отзыв и верни ТОЛЬКО JSON без пояснений.
Формат: {"sentiment": "positive|negative|neutral", "topic": "тема"}
Темы: taste, solubility, effectiveness, packaging, price, digestion, delivery.
"""

reviews = []
with open("reviews.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        reviews.append(row[list(row.keys())[0]])

print(f"Найдено отзывов: {len(reviews)}")

results = []
for i, review in enumerate(reviews, 1):
    print(f"\nОбработка {i}/{len(reviews)}: {review[:50]}...")
    
    if i > 1:
        time.sleep(2) 
    
    try:
        response = client.chat.completions.create(
            model="openrouter/free", 
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": review}
            ],
            temperature=0
        )
        analysis = response.choices[0].message.content
        print(f"  Ответ: {analysis}")
        results.append({"review": review, "analysis": analysis})
        
    except Exception as e:
        print(f"  Ошибка: {e}")
        results.append({"review": review, "analysis": f"ERROR: {e}"})

with open("output_results.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["review", "analysis"])
    writer.writeheader()
    writer.writerows(results)

print("\nГотово! Результат в файле output_results.csv")