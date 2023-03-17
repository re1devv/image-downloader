import os, time, requests, re
from bs4 import BeautifulSoup

class Scraping:

    def __init__(self, target_url="", search_tag_and_attribute="", download_image_pattern="", 
                    selector_image_folder_name="", download_directory="",
                    numbering=False):
        self.target_url = target_url
        self.search_tag_and_attribute = search_tag_and_attribute
        self.download_image_pattern = download_image_pattern
        self.selector_image_folder_name = selector_image_folder_name
        self.download_directory = download_directory 
        self.numbering = numbering

        self.page_content = BeautifulSoup(requests.get(self.target_url).content, "html.parser")
        self.image_folder_name = ""


        print(f"情報: `{self.target_url}`のコンテンツデータを読み込みました。")
        pass

    def get_download_contents(self) -> list:
        contents = []
        search_tag = self.search_tag_and_attribute.split(",")[0]
        search_attribute = self.search_tag_and_attribute.split(",")[1]

        for image in self.page_content.find_all(search_tag):
            src = image.get(search_attribute)
            if not self.download_image_pattern or self.download_image_pattern in src: 
                contents.append(src)

        return contents

    def download(self):
        contents = self.get_download_contents()
        if not contents: 
            print(f"情報: `{self.target_url}`にダウンロードできるものはありませんでした")
            return

        if self.selector_image_folder_name:
            self.image_folder_name = re.sub(r"[\\\/\:\*\?\"\<\>\|]", " ", self.page_content.select(self.selector_image_folder_name)[0].get_text())

        download_path = [self.download_directory] if not self.image_folder_name else [self.download_directory, self.image_folder_name]
        print(download_path)
        download_path = os.path.join(os.path.abspath(os.getcwd()), *download_path)
        if not os.path.exists(download_path): 
            os.makedirs(download_path)

        downloaded_count = 0

        for content in contents:
            image_name = content.split("/")[-1]

            if self.numbering: dp = os.path.join(download_path, str(downloaded_count) + "." + (image_name.split(".")[-1]))
            else: dp = os.path.join(download_path, image_name)

            if not os.path.exists(dp):
                request = requests.get(content)
                if request.status_code == 200:
                    with open(dp, "wb") as f:
                        f.write(request.content)

                    downloaded_count += 1
                    print(f"Download successfully => {dp}")
                else:
                    print(f"Failed to download => {dp}")

                time.sleep(1)
