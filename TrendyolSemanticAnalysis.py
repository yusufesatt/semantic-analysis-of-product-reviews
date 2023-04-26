from requests import get
from json import loads
import openai
from openpyxl import load_workbook
import pandas as pd

try:
    openaiKey = input("OpenAI API Key Giriniz: ")
    url = input("URL: ")
    excel_name = input("Excel dosya ismi giriniz: ")

    print('Tüm yorumları çekmek için 0 bas')
    Range = int(input("Kaç yorum çekmek istiyorsun: "))

    itemId = url.split("-p-")[-1].split("?")[0]

    pageCount = 0
    commentList = []

    #if data["isSuccess"] == True:
    while True:
        url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{itemId}?page={pageCount}"
        
        data = loads(get(url).text)
        if len(commentList) >= Range and Range != 0 or pageCount > 100:
            break

        commentList.extend(data["result"]["productReviews"]["content"])

        totalPages = 100 if data["result"]["productReviews"]["totalPages"] > 100 else data["result"]["productReviews"]["totalPages"]
        print(f"[{pageCount}/{totalPages}] işleniyor\t\t\t", end="\r")
        if len(data["result"]["productReviews"]["content"]) == 30:
            pageCount += 1
        else:
            break


    commentList = commentList[:Range] if Range > 0 else commentList
    comments = [a["comment"] for a in commentList]

    print(f"Çekilen yorum sayısı: {len(comments)}")

    # SENTİMENT ANALYSİS 

    openai.api_key = openaiKey

    sentiments = []

    def analyzeSentiment(analyzer, index):
        completion = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"[{index + 1}/{len(comments)}]bu yorumların duygu analizini yap ve sonucunu yani pozitif mi, negatif mi, nötr mü oldugunu yaz.\n{comment}\nDuygu Analizi:",
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7,
        )

        sentiment = completion.choices[0].text.strip()
        sentiments.append(sentiment)
        print(f"\r[{index + 1}/{len(comments)}] Yorum duygu analizi tamamlandı.",end='')

    for index, comment in enumerate(comments):
        sentiment = analyzeSentiment(comment, index)

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
except:
    print("Girdiğiniz OpenAI API Key veya Ürün Url'si hatalı girilmiştir.")
