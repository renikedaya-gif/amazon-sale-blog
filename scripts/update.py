"""メイン更新スクリプト - データ取得 & HTML生成を実行"""
import configparser
import json
import os
import sys
from datetime import datetime

# スクリプトのあるディレクトリを基準にパスを解決
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))


def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "config.ini"), encoding="utf-8")
    return config


def run():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 更新開始...")
    config = load_config()

    demo_mode = config["settings"].getboolean("demo_mode", True)

    if demo_mode:
        print("[INFO] デモモードで実行中（config.ini の demo_mode=false にするとPA API使用）")
        from demo_data import get_demo_products
        products = get_demo_products()
    else:
        print("[INFO] Amazon PA API からデータを取得中...")
        from fetch_amazon import fetch_deals_from_paapi
        products = fetch_deals_from_paapi(config)
        if not products:
            print("[WARN] PA APIからデータを取得できませんでした。デモデータを使用します")
            from demo_data import get_demo_products
            products = get_demo_products()

    # データ保存
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    data_path = os.path.join(data_dir, "products.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(products)} 件の商品データを保存: {data_path}")

    # HTML生成
    from generate_html import generate_html
    html = generate_html(products, config)

    out_path = os.path.join(BASE_DIR, config["output"]["html_file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTMLを生成: {out_path}")

    # ログ記録
    log_path = os.path.join(BASE_DIR, "update.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {len(products)}件更新\n")

    print(f"[完了] ブログを更新しました！")
    return True


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
