"""Amazon PA API からセール商品を取得するスクリプト"""
import configparser
import json
import os
import sys

# PA APIライブラリ（pip install paapi5-python-sdk）
try:
    from paapi5_python_sdk.api.default_api import DefaultApi
    from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
    from paapi5_python_sdk.models.partner_type import PartnerType
    from paapi5_python_sdk.rest import ApiException
    PAAPI_AVAILABLE = True
except ImportError:
    PAAPI_AVAILABLE = False

# カテゴリとPA APIのSearchIndex対応表
CATEGORIES = {
    "家電・カメラ": "Electronics",
    "パソコン・周辺機器": "Computers",
    "ゲーム": "VideoGames",
    "キッチン・日用品": "Kitchen",
    "スポーツ・アウトドア": "SportingGoods",
    "ファッション": "Fashion",
    "本・雑誌": "Books",
    "ビューティー・ヘルスケア": "Beauty",
}


def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
    config.read(config_path, encoding="utf-8")
    return config


def fetch_deals_from_paapi(config):
    """PA APIからセール商品を取得"""
    if not PAAPI_AVAILABLE:
        print("[ERROR] paapi5-python-sdk がインストールされていません")
        print("  pip install paapi5-python-sdk を実行してください")
        return []

    access_key = config["amazon"]["access_key"]
    secret_key = config["amazon"]["secret_key"]
    partner_tag = config["amazon"]["partner_tag"]
    max_items = int(config["settings"].get("max_items_per_category", 10))
    min_discount = int(config["settings"].get("min_discount_rate", 10))

    if access_key == "YOUR_ACCESS_KEY":
        print("[ERROR] config.ini にPA APIの認証情報を設定してください")
        return []

    api = DefaultApi(
        access_key=access_key,
        secret_key=secret_key,
        host="webservices.amazon.co.jp",
        region="us-west-2",
    )

    all_products = []
    for category_name, search_index in CATEGORIES.items():
        try:
            request = SearchItemsRequest(
                partner_tag=partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords="セール 割引",
                search_index=search_index,
                item_count=max_items,
                resources=[
                    "Images.Primary.Medium",
                    "ItemInfo.Title",
                    "Offers.Listings.Price",
                    "Offers.Listings.SavingBasis",
                    "Offers.Summaries.LowestPrice",
                    "CustomerReviews.Count",
                    "CustomerReviews.StarRating",
                ],
            )
            response = api.search_items(request)

            if response.search_result and response.search_result.items:
                for item in response.search_result.items:
                    product = _parse_item(item, category_name, partner_tag)
                    if product and product["discount_rate"] >= min_discount:
                        all_products.append(product)

        except ApiException as e:
            print(f"[WARN] {category_name} の取得に失敗: {e}")

    return all_products


def _parse_item(item, category, partner_tag):
    """PA APIのアイテムを辞書に変換"""
    try:
        title = item.item_info.title.display_value if item.item_info else "不明"
        asin = item.asin
        url = f"https://www.amazon.co.jp/dp/{asin}?tag={partner_tag}"

        image = ""
        if item.images and item.images.primary and item.images.primary.medium:
            image = item.images.primary.medium.url

        original_price = 0
        sale_price = 0
        if item.offers and item.offers.listings:
            listing = item.offers.listings[0]
            if listing.price:
                sale_price = listing.price.amount or 0
            if listing.saving_basis:
                original_price = listing.saving_basis.amount or sale_price

        if original_price == 0 or sale_price == 0:
            return None

        discount_rate = round((1 - sale_price / original_price) * 100)
        if discount_rate <= 0:
            return None

        rating = 0
        reviews = 0
        if item.customer_reviews:
            rating = item.customer_reviews.star_rating.value if item.customer_reviews.star_rating else 0
            reviews = item.customer_reviews.count or 0

        return {
            "id": asin,
            "title": title,
            "category": category,
            "image": image,
            "original_price": int(original_price),
            "sale_price": int(sale_price),
            "url": url,
            "rating": float(rating),
            "reviews": int(reviews),
            "discount_rate": discount_rate,
            "badge": f"{discount_rate}%OFF",
        }
    except Exception:
        return None


if __name__ == "__main__":
    config = load_config()
    products = fetch_deals_from_paapi(config)
    print(json.dumps(products, ensure_ascii=False, indent=2))
