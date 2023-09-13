from requests import get
from json import loads
import openai
from openpyxl import load_workbook
import pandas as pd
from tqdm import tqdm

openaiKey = input("OpenAI API Key Giriniz: ")
url = input("URL: ")
excel_name = input("Excel dosya ismi giriniz: ")

print('Tüm yorumları çekmek için 0 bas')
Range = int(input("Kaç yorum çekmek istiyorsun: "))

itemId = url.split("-p-")[-1].split("?")[0]

pageCount = 0
commentList = []

# if data["isSuccess"] == True:
while True:
    url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{itemId}?page={pageCount}"

    data = loads(get(url).text)
    if len(commentList) >= Range and Range != 0 or pageCount > 100:
        break

    commentList.extend(data["result"]["productReviews"]["content"])

    totalPages = 100 if data["result"]["productReviews"]["totalPages"] > 100 else data["result"]["productReviews"][
        "totalPages"]
    print(f"[{pageCount}/{totalPages}] işleniyor\t\t\t", end="\r")
    if len(data["result"]["productReviews"]["content"]) == 30:
        pageCount += 1
    else:
        break

commentList = commentList[:Range] if Range > 0 else commentList
comments = [a["comment"] for a in commentList]

print(f"Çekilen yorum sayısı: {len(comments)}")

# Sentiment Analysis
openai.api_key = openaiKey
sentiments = []


def gpt3_chat(comment, index):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"[{index + 1}/{len(comments)}] Analyze the comments for sentiment, and express the emotion of each "
               f"comment in a single word, starting with a capital letter: 'Positive', 'Negative', or 'Neut"
               f"ral'.\n{comment}\nSentiment Analysis:",
        max_tokens=50,
        temperature=0.7
    )

    sentiment = response.choices[0].text.strip()
    sentiments.append(sentiment)


for index, comment in tqdm(comments):
    gpt3_chat(comment, index)
excel_comp = excel_name + ".xlsx"

df = pd.DataFrame({'Yorumlar': comments, 'Duygu Analizi': sentiments})
with pd.ExcelWriter(excel_comp) as writer:
    df.to_excel(writer, sheet_name='yorumlar', index=False)

book = load_workbook(excel_comp)
ws = book['yorumlar']
ws.column_dimensions['A'].width = 100
ws.column_dimensions['B'].width = 20
book.save(excel_comp)

print("\nBaşarıyla excel'e aktarıldı")
