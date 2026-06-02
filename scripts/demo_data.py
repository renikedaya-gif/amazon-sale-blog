"""デモ用サンプルデータ生成（実在するAmazon商品）"""
import base64
import urllib.parse

PARTNER_TAG = "salematome0d-22"


def amz(asin=None, keyword=None):
    """アフィリエイトリンク生成"""
    if asin:
        return f"https://www.amazon.co.jp/dp/{asin}?tag={PARTNER_TAG}"
    q = urllib.parse.quote(keyword)
    return f"https://www.amazon.co.jp/s?k={q}&tag={PARTNER_TAG}"


def svg_img(emoji, bg="#1a1a2e", accent="#e94560"):
    """SVG画像をBase64エンコードしてdata URIで返す（外部依存なし・必ず表示される）"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg}"/>
      <stop offset="100%" style="stop-color:{accent};stop-opacity:0.3"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" fill="url(#g)" rx="16"/>
  <text x="100" y="115" font-size="90" text-anchor="middle" dominant-baseline="middle">{emoji}</text>
</svg>"""
    encoded = base64.b64encode(svg.encode("utf-8")).decode()
    return f"data:image/svg+xml;base64,{encoded}"


DEMO_PRODUCTS = [
    # 家電・カメラ
    {
        "id": "B0D78JK314",
        "title": "Anker PowerCore 10000 モバイルバッテリー 10000mAh 大容量 コンパクト",
        "category": "家電・カメラ",
        "image": svg_img("📱", "#1a1a2e", "#e94560"),
        "original_price": 3990,
        "sale_price": 1990,
        "url": amz("B0D78JK314"),
        "rating": 4.5,
        "reviews": 15420,
        "badge": "タイムセール",
    },
    {
        "id": "B09Z2QYYD1",
        "title": "Sony WH-1000XM5 ワイヤレスノイズキャンセリングヘッドフォン ブラック",
        "category": "家電・カメラ",
        "image": svg_img("🎧", "#1a1a2e", "#e94560"),
        "original_price": 59400,
        "sale_price": 38500,
        "url": amz("B09Z2QYYD1"),
        "rating": 4.7,
        "reviews": 8930,
        "badge": "週末セール",
    },
    {
        "id": "B0CBKQZXT7",
        "title": "Sony WF-1000XM5 完全ワイヤレスノイズキャンセリングイヤホン",
        "category": "家電・カメラ",
        "image": svg_img("🔊", "#1a1a2e", "#e94560"),
        "original_price": 49500,
        "sale_price": 32800,
        "url": amz("B0CBKQZXT7"),
        "rating": 4.4,
        "reviews": 12100,
        "badge": "Amazonセール",
    },
    # パソコン・周辺機器
    {
        "id": "B09HM94VDS",
        "title": "Logicool MX MASTER 3S ワイヤレスマウス 高性能 静音クリック",
        "category": "パソコン・周辺機器",
        "image": svg_img("🖱️", "#0f3460", "#e94560"),
        "original_price": 16500,
        "sale_price": 9800,
        "url": amz("B09HM94VDS"),
        "rating": 4.8,
        "reviews": 5670,
        "badge": "特価",
    },
    {
        "id": "B08QBJ2YMG",
        "title": "Samsung 870 EVO 1TB 2.5インチ SATA SSD",
        "category": "パソコン・周辺機器",
        "image": svg_img("💾", "#0f3460", "#e94560"),
        "original_price": 19800,
        "sale_price": 8980,
        "url": amz("B08QBJ2YMG"),
        "rating": 4.6,
        "reviews": 12300,
        "badge": "数量限定",
    },
    {
        "id": None,
        "title": "ASUS 24インチ FHDゲーミングモニター 144Hz IPS VG249Q",
        "category": "パソコン・周辺機器",
        "image": svg_img("🖥️", "#0f3460", "#e94560"),
        "original_price": 34800,
        "sale_price": 19800,
        "url": amz(keyword="ASUS 24インチ ゲーミングモニター 144Hz"),
        "rating": 4.4,
        "reviews": 3210,
        "badge": "タイムセール",
    },
    # ゲーム
    {
        "id": None,
        "title": "ゼルダの伝説 ティアーズ オブ ザ キングダム Nintendo Switch",
        "category": "ゲーム",
        "image": svg_img("🎮", "#16213e", "#e94560"),
        "original_price": 8778,
        "sale_price": 5500,
        "url": amz(keyword="ゼルダの伝説 ティアーズオブザキングダム Switch"),
        "rating": 4.9,
        "reviews": 45600,
        "badge": "セール",
    },
    {
        "id": None,
        "title": "スーパーマリオブラザーズ ワンダー Nintendo Switch",
        "category": "ゲーム",
        "image": svg_img("🕹️", "#16213e", "#e94560"),
        "original_price": 6578,
        "sale_price": 4480,
        "url": amz(keyword="スーパーマリオブラザーズ ワンダー Switch"),
        "rating": 4.8,
        "reviews": 28900,
        "badge": "ポイントUP",
    },
    # キッチン・日用品
    {
        "id": None,
        "title": "Instant Pot Duo 電気圧力鍋 6L 7-in-1 多機能クッカー",
        "category": "キッチン・日用品",
        "image": svg_img("🍳", "#1a1a2e", "#00b4d8"),
        "original_price": 14800,
        "sale_price": 7980,
        "url": amz(keyword="Instant Pot 電気圧力鍋 6L"),
        "rating": 4.5,
        "reviews": 9870,
        "badge": "タイムセール",
    },
    {
        "id": None,
        "title": "Dyson V12 Detect Slim コードレスクリーナー",
        "category": "キッチン・日用品",
        "image": svg_img("🧹", "#1a1a2e", "#00b4d8"),
        "original_price": 94800,
        "sale_price": 64800,
        "url": amz(keyword="Dyson V12 Detect Slim コードレス"),
        "rating": 4.7,
        "reviews": 3450,
        "badge": "数量限定",
    },
    # スポーツ・アウトドア
    {
        "id": None,
        "title": "Garmin Forerunner 255 GPSスマートウォッチ ランニング",
        "category": "スポーツ・アウトドア",
        "image": svg_img("⌚", "#0f3460", "#00b4d8"),
        "original_price": 49800,
        "sale_price": 32800,
        "url": amz(keyword="Garmin Forerunner 255 GPS ランニングウォッチ"),
        "rating": 4.6,
        "reviews": 2340,
        "badge": "特価",
    },
    {
        "id": None,
        "title": "Coleman ツーリングドーム ST ソロキャンプ 2人用テント",
        "category": "スポーツ・アウトドア",
        "image": svg_img("⛺", "#0f3460", "#00b4d8"),
        "original_price": 29800,
        "sale_price": 17800,
        "url": amz(keyword="Coleman ツーリングドーム ST テント"),
        "rating": 4.4,
        "reviews": 1890,
        "badge": "シーズンセール",
    },
    # ファッション
    {
        "id": None,
        "title": "Columbia 防水マウンテンパーカー アウトドアジャケット",
        "category": "ファッション",
        "image": svg_img("🧥", "#16213e", "#00b4d8"),
        "original_price": 22000,
        "sale_price": 11000,
        "url": amz(keyword="Columbia マウンテンパーカー 防水 メンズ"),
        "rating": 4.3,
        "reviews": 670,
        "badge": "50%OFF",
    },
    # 本・雑誌
    {
        "id": None,
        "title": "Kindle Paperwhite (16GB) 6.8インチディスプレイ 広告なし",
        "category": "本・雑誌",
        "image": svg_img("📚", "#1a1a2e", "#e94560"),
        "original_price": 22980,
        "sale_price": 14980,
        "url": amz(keyword="Kindle Paperwhite 16GB 広告なし"),
        "rating": 4.6,
        "reviews": 45600,
        "badge": "期間限定",
    },
    # ビューティー・ヘルスケア
    {
        "id": None,
        "title": "Oral-B iO Series 6 電動歯ブラシ スマート音波振動",
        "category": "ビューティー・ヘルスケア",
        "image": svg_img("🪥", "#0f3460", "#e94560"),
        "original_price": 24200,
        "sale_price": 12980,
        "url": amz(keyword="Oral-B iO Series 6 電動歯ブラシ"),
        "rating": 4.5,
        "reviews": 4320,
        "badge": "タイムセール",
    },
]


def get_demo_products():
    """デモ商品データを返す（割引率を自動計算）"""
    products = []
    for p in DEMO_PRODUCTS:
        discount = round((1 - p["sale_price"] / p["original_price"]) * 100)
        item = {**p, "discount_rate": discount}
        if item["id"] is None:
            item["id"] = "srch_" + str(abs(hash(item["title"])) % 100000000)
        products.append(item)
    products.sort(key=lambda x: x["discount_rate"], reverse=True)
    return products
