from flask import Flask, render_template, request, jsonify, session, json, redirect, url_for

app = Flask(__name__)

# テキストファイルからリンク先URLと画像URLを抽出する関数
def scrape_images_and_links():
    image_links = []
    link = None
    image_url = None
    other_text = []

    with open('image_links.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            # リンク先URLを取得
            if line.startswith("リンク先:"):
                if link and image_url:
                    image_links.append({
                        'image_url': image_url,
                        'link': link,
                        'other_text': "\n".join(other_text)
                    })

                link = line.replace("リンク先:", "").strip()
                other_text = []  # リンクが新しくなったら、other_textをリセット
            # 画像URLを取得
            elif line.startswith("画像:"):
                image_url = line.replace("画像:", "").strip()
            # その他のテキスト情報を収集
            else:
                other_text.append(line.strip())

        # 最後のリンクと画像URLの情報を保存
        if link and image_url:
            image_links.append({
                'image_url': image_url,
                'link': link,
                'other_text': "\n".join(other_text)
            })

    return image_links


# ホームページ（home.html）
@app.route('/')
def home():
    return render_template('home.html')


# ルートページ
@app.route('/goodslist')
def index():
    image_links = scrape_images_and_links()  # テキストファイルから画像のURLとリンクのURLを取得
    search_query = request.args.get('search', '').strip().lower()

    # 検索クエリがある場合はフィルタリング
    if search_query:
        keywords = search_query.split()
        image_links = [
            link for link in image_links
            if all(keyword in link['other_text'].lower() for keyword in keywords)
        ]


    # ページ番号を取得
    page = request.args.get('page', 1, type=int)

    # 各ページのアイテム数
    items_per_page = 36

    # 開始インデックスと終了インデックスを計算
    start = (page - 1) * items_per_page
    end = start + items_per_page

    # 現在のページに表示する画像リンク
    paginated_links = image_links[start:end]

    # 全ページ数を計算
    total_pages = (len(image_links) + items_per_page - 1) // items_per_page

    return render_template(
        'goodslist.html',
        image_links=paginated_links,
        search_query=search_query,
        current_page=page,
        total_pages=total_pages
    )


# goods2ページ
@app.route('/wishlist')
def goods2():
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
