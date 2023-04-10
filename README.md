# Proje Hakkında Bilgi
Bu proje, Trendyol'da yer alan bir ürünün URL'si ve kullanıcının istediği yorum sayısı girilerek, OpenAI API'si kullanılarak yorumların duygu analizinin yapıldığı bir Python programıdır. Bu program, kullanıcının istediği sayıda yorumu çeker ve her yorumun pozitif, negatif veya nötr olup olmadığını belirler. Sonuçlar bir Excel dosyasına yazdırılır ve bu dosya kolayca incelenebilir. Bu proje, kullanıcılara Trendyol'da bir ürün hakkında daha fazla bilgi edinme imkanı sunar ve bir ürünün popülerliği hakkında fikir edinmelerine yardımcı olabilir.

Projeyi kullanmak için, öncelikle OpenAI API anahtarına ihtiyacınız olacaktır. Anahtarı almak için OpenAI web sitesine kaydolmanız gerekmektedir. Daha sonra, projeyi GitHub'dan indirip çalıştırabilirsiniz. Kullanıcı arayüzü basittir. URL ve yorum sayısı gibi gerekli bilgileri girmeniz yeterlidir. Sonuçlar bir Excel dosyasına yazdırılacaktır ve bu dosya kullanıcı tarafından incelenebilir.

## Kurulum Adımları ve Gereksinimler

Python 3

pip

## Programı İndirip Çalıştırma 

```
git clone https://github.com/Spyzah/Comments-Semantic-Analysis.git
cd CommentsSemanticAnalysis
pip install -r requirements.txt
python TrendyolSemanticAnalysis.py
```

### Kullanılan Kütüphaneler


[Pandas](https://github.com/pandas-dev/pandas)

[requests](https://github.com/psf/requests)

[Json](https://github.com/dpranke/pyjson5)

[OpenAi](https://github.com/openai/openai-python)



