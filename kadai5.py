import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

list = []
### main処理
def main():
    #search_keyword="高収入"
    keyword = input("検索したいキーワードを入力してください>>")
    print(keyword)
    # driverを起動
    driver=set_driver("chromedriver.exe",False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    list = []
    # ページ終了まで繰り返し取得
    while True:
        #検索結果の一番上の会社名を取得
#        name_list=driver.find_elements_by_class_name("cassetteRecruit__name")
#        copy_list=driver.find_elements_by_class_name("cassetteRecruit__copy")
#        status_list=driver.find_elements_by_class_name("labelEmploymentStatus")
        #1ページ分繰り返し
#        print("{},{},{}".format(len(copy_list),len(status_list),len(name_list)))
#        for name,copy,status in zip(name_list,copy_list,status_list):
#            print(name.text)
#            print(copy.text)
#            print(status.text)
        content_list = driver.find_elements_by_class_name("cassetteRecruit__content")
        for content in content_list:
            print(content.text)
            list.append(content.text)

        # 次のページボタンがあればクリックなければ終了
        next_page=driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page)>=1:
            next_page_link=next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            print("最終ページです。終了します。")
            break
    df = pd.DataFrame(list)
    df.to_csv("data.csv")
    

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
