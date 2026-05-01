from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import json
import re
import numpy as np
from PIL import Image

# シルエットの形を決める画像をインポート
mask = np.array(Image.open("icon.png"))

# tweets.jsの読み込み
with open("tweets.js", "r", encoding="utf-8") as f:
    data = f.read()

# tweets.jsの整形（Json化）
json_str = re.sub(r"window\.YTD\.tweets\.part0\s*=\s*", "", data)# URLの除外
json_str = json_str.strip().rstrip(";")
tweets = json.loads(json_str)

#jsonからテキスト抽出
texts = []

for t in tweets:
    tweet = t["tweet"]
    texts.append(tweet["full_text"])


t = Tokenizer()
s = []

# 除外するワードリスト
stopwords = {
    "の","に","は","を","た","が","で","て","と","し","れ","さ",
    "ある","する","いる","こと","これ","それ","あれ","ん"
}

for text in texts:
    text = re.sub(r'https?://\S+', '', text)
    for token in t.tokenize(text):
        p = token.part_of_speech.split(",")
        surface = token.surface
        if "名詞" in p and surface not in stopwords:
            s.append(token.surface)

wc = WordCloud(
            width=640,
            height=480,
            #フォントはファイルパスで指定
            font_path="/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
            mask=mask,
            background_color="white"
            )


wc.generate(" ".join(s))
wc.to_file('word-cloud.png')