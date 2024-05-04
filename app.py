from json import loads

import pandas as pd
from openai import OpenAI
from openpyxl import load_workbook
from requests import get
from tqdm import tqdm

openaiKey = input("Enter OpenAI API Key: ")
url = input("Trendyol Product URL: ")
excel_name = input("Enter Excel file name to save: ")

print("Enter 0 to withdraw all comments.")
Range = int(input("How many comments do you want to attract: "))

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

print(f"Number of comments attracted: {len(comments)}")

# Sentiment Analysis
client = OpenAI(
    api_key=openaiKey,
)
sentiments = []


def gpt3_chat(comment, index):
    response = client.completions.create(
        model="gpt-3.5-turbo",
        prompt=f"[{index + 1}/{len(comments)}] Analyze the comments for sentiment, and express the emotion of each "
               f"comment in a single word, starting with a capital letter: 'Positive', 'Negative', or 'Neut"
               f"ral'.\n{comment}\nSentiment Analysis:",
        max_tokens=50,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    sentiment = response.choices[0].text.strip()
    sentiments.append(sentiment)


for index, comment in tqdm(enumerate(comments)):
    gpt3_chat(comment, index)

excel_comp = excel_name + ".xlsx"

df = pd.DataFrame({'Comments': comments, 'Sentiment Analysis': sentiments})
with pd.ExcelWriter(excel_comp) as writer:
    df.to_excel(writer, sheet_name='Comments', index=False)

book = load_workbook(excel_comp)
ws = book['Comments']
ws.column_dimensions['A'].width = 100
ws.column_dimensions['B'].width = 20
book.save(excel_comp)

print("\nSuccessfully exported to excel!")
