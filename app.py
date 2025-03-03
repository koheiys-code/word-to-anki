"""
[name] app.py
[purpose] word to csv for anki
[reference]
    https://docs.streamlit.io/develop/api-reference

written by Dr.K, 2024/4/28
"""
import datetime

import pytz
import streamlit as st

from utils import file_to_table, table_to_csv


ICON_PATH = "images/icon.png"


'''
# wordファイルをanki用のCSVファイルに変換します
## 前提
* 教科書などの暗記事項をwordファイルにまとめます
* それを自動で[anki](https://apps.ankiweb.net/)用のCSVファイルに変換します
* ankiカードのフィールドは"Front", "Back", "Title", "Page"です
* Front: カードの表
* Back: カードの裏
* Title: 教科書名などを想定
* Page: ページ番号
## 使用方法
### まずは以下のようなwordファイルを作成します
example.docx
'''

word_example = '''p.1
このサイトを開発したのは誰か答えよ。
Dr.K

p.3
このサイトの開発者のブログURLを答えよ。
https://doctor-k.net

p.5
このサイトのコードはどこで見られるか答えよ。
https://github.com/doctor-k-code
'''
st.code(word_example)

'''
* ページ番号、カードの表、カードの裏の順番で記載し、それぞれ改行して下さい
* 改行が不適切だと"段落数が一致しません"というメッセージが表示されます
* 図については対応していませんので適当な文字で埋めて、後からankiへの登録の際に実際の図を挿入してください
* 簡単な例で一度試してみることをおすすめします
### 教科書名などのタイトルを入力してwordファイルをアップロードします
'''

title = st.text_input("タイトル")

uploaded_files = st.file_uploader(
    "wordファイルをアップロード", type="docx", accept_multiple_files=True)

if st.button("実行"):
    if not title:
        st.write("**タイトル**を入力して下さい")
    else:
        time_stamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        time_stamp = time_stamp.strftime('%m%d%H%M')
        table = None
        for uploaded_file in uploaded_files:
            table = file_to_table(uploaded_file, table=table, title=title)
        st.dataframe(table)

        result_csv = table_to_csv(table)
        file_name = '_'.join(['for_anki', time_stamp+'.csv'])
        st.download_button(label="CSVファイルをダウンロード", data=result_csv, file_name=file_name)

'''
### CSVファイルをダウンロードしたらPC版のankiで登録をします
1. ankiを起動する
2. （初めての方のみ）「ツール>ノートタイプを管理>追加」からノートタイプを追加する
3. （初めての方のみ）"基本"のノートタイプを複製して、"教科書"という名前で登録する
4. （初めての方のみ）"教科書"のフィールドを"Front", "Back", "Title", "Page"にする
5. （初めての方のみ）"教科書"のカードの"裏面のテンプレート"を以下に変更する
'''

back_temp = '''{{FrontSide}}

<hr id=answer>

{{Back}}

<div class = "ref">
{{Title}} {{Page}}
</div>
'''
st.code(back_temp)

'''
6. 「ファイル>読み込む」でダウンロードしたCSVファイルを選択する
7. ノートタイプ"教科書"でCSVファイルを読み込む
8. 正しく暗記カードが作成されているかを確認する
'''

st.divider()
'''
### このサイトの製作者
* [ブログ](https://doctor-k.net)をやっています
* 作成したコードは[こちら](https://github.com/doctor-k-code)から
'''
st.image(ICON_PATH, width=200, caption="駆け出し医師Dr.K")
