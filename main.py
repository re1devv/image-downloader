import sys, os
import scraping

target_url = input("ダウンロードしたい画像があるページのURL\n> ")
download_directory = input("ダウンロード先のディレクトリ名を指定してください。\nこのプロジェクトのルートディレクトリ上にディレクトリが存在しない場合は自動的に生成されます。\n(download) > ")
search_tag_and_attribute = input("検索するタグと属性の名前を入力してください。\nタグと属性は「,」で区切って指定してください。\n(img,src) > ")
download_image_pattern = input("検索する画像のパターンを入力してください。\n検索したタグの属性から値を取得し、このパターンに一致（または部分一致）する画像のみをダウンロードします。\nなお、正規表現によるチェックは行われません。\nパターンを省略した場合は、検索したタグと属性から取得できるものをダウンロードします\n> ")
selector_image_folder_name = input("指定URLページ内にある任意の要素内のテキストをダウンロードした画像を格納するフォルダの名前にできます。\n抽出したいテキストがある要素へのCSSセレクタを入力してください。\nテキストが取得できた場合は「./ダウンロード先のディレクトリ/特定の要素から取得したフォルダ名」に画像ファイルがダウンロードされます。\nセレクタの指定がない場合は「./ダウンロード先のディレクトリ」直下に画像ファイルがダウンロードされます。\n(title) > ")
numbering = input("ダウンロードした画像をナンバリングして保存するかどうか\n(y) > ")

if not target_url: sys.exit(("\n" * 3) + "エラー: ダウンロードしたい画像があるページのURLを入力してください。")
if not download_directory: download_directory = "download"
if not search_tag_and_attribute: search_tag_and_attribute = "img,src"
if not selector_image_folder_name: selector_image_folder_name = "title"
if not numbering: numbering = "y"

target_url = target_url.split(",")

print(f"情報: {str(len(target_url))}点のページから画像をダウンロードします。")
for tu in target_url:
    sc = scraping.Scraping(tu, search_tag_and_attribute, download_image_pattern, selector_image_folder_name, download_directory, numbering == "y")
    contents_count = sc.get_download_contents()

    if not contents_count:
        sys.exit(("\n" * 3) + "エラー: ダウンロードできる画像がありませんでした")

    print("=" * 20)
    print(f"情報: `{tu}`にある画像を{str(len(contents_count))}点ダウンロードします。")
    print("=" * 20)

    sc.download()

print("情報: すべてのダウンロードが完了しました。")
