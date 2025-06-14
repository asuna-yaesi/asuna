import re

def clean_and_filter_blocks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # URLを含むブロックごとに分割
    blocks = re.split(r'(?=リンク先: https?://)', text)

    # URLを記録するためのセット
    seen_urls = set()
    filtered_blocks = []

    # 必要な行を抽出するための正規表現
    pattern = r'リンク先:.*\n|画像:.*\n|商品名:.*\n|JANコード.*\n.*\n|発売日.*\n.*\n|ブランド名.*\n.*\n|原作名.*\n.*\n|キャラ名.*\n.*\n'
    
    # 《》や【】で囲まれた部分を削除するための正規表現
    remove_brackets_pattern = r'《[^》]*》|【[^】]*】'

    # noimage.jpg のURLを削除対象に追加
    no_image_url = 'https://img.amiami.jp/images/product/thumb300/noimage.jpg'

    # 条件に合致するサイズの正規表現
    size_pattern = r'(?:S|XS|XL|XXS|XXL|XXXL|L)'

    for block in blocks:
        # URLを取得（最初の URL を使う）
        urls = re.findall(r'https?://\S+', block)
        if urls:
            url = urls[1]

            # 商品名に「中古」が含まれる場合、この塊全体を削除
            if re.search(r'商品名:.*中古', block):
                continue  # 次のブロックへ

            # 商品名に「Tシャツ」または「パーカー」が含まれ、指定サイズが含まれる場合、この塊全体を削除
            if re.search(r'商品名:.*(?:Tシャツ|パーカー)', block) and re.search(size_pattern, block):
                continue

            # noimage.jpg の画像URLが含まれている場合、この塊全体を削除
            if no_image_url in block:
                continue

            # URLがすでに出現している場合、この塊全体を削除
            if url in seen_urls:
                continue

            # 新規URLの場合、セットに追加
            seen_urls.add(url)

            # 《》や【】で囲まれた文字とそれらの括弧を削除
            block = re.sub(remove_brackets_pattern, '', block)

            # 必要な行のみを抽出
            filtered_block = re.findall(pattern, block)

            # 抽出した行を連結（空白行が入らないように）
            filtered_block_str = ''.join(filtered_block)

            # フィルタされたブロックを保存
            if filtered_block_str:
                filtered_blocks.append(filtered_block_str)

    # フィルタリングした結果を出力ファイルに書き込む（塊と塊の間に1行空白）
    with open(output_file, 'w', encoding='utf-8') as f:
        # 最後の塊を除いて、各塊の間に1行空白行を挿入
        for i, block in enumerate(filtered_blocks):
            if i < len(filtered_blocks) - 1:
                f.write(block + '\n')  # 塊と塊の間に1行空白
            else:
                f.write(block)  # 最後の塊には空白行を挿入しない

# ファイルを読み込み、重複を削除して新しいファイルに書き込む
input_file = r"C:\Users\masaya\Desktop\図鑑アプリ\exrtact\抽出テキスト.txt"  
output_file = r"C:\Users\masaya\Desktop\図鑑アプリ\goods -\image_links.txt"
clean_and_filter_blocks(input_file, output_file)
