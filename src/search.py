from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    timeout=None,
    max_retries=2,
)
messages = [
    (
        "system",
        "以下の情報は開催するイベント情報です。この情報からイベント名、開催場所の住所、開催日時、料金形態を抽出してください。リンクがある場合はそのリンクも辿って探してください。記載されていない場合は出力しないでください。",
    ),
    (
        "human",
        """会場: 神田明神境内本殿横特設会場
会費: 入場無料

※時間は予想です

#大分 #栄 #関 #境 #肉 #屋台 #レア #ジョン #カキ #酸 #踊り #日本酒 #地 #ビール #結 #ステーキ


https://zeppin-yatai.com/kanda/

https://japan-attractions.jp/ja/alcohol/zeppin-kandamyojin/"),
""",
    ),
    (
        "human",
        "リンク: https://zeppin-yatai.com/kanda/",
    ),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
