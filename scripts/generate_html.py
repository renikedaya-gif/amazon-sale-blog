"""商品データからHTMLブログを生成するスクリプト"""
import configparser
import json
import os
from datetime import datetime
from collections import defaultdict


def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
    config.read(config_path, encoding="utf-8")
    return config


def get_discount_tier(rate):
    """割引率からティア名を返す"""
    if rate >= 50:
        return ("超お得 50%以上OFF", "tier-50", "🔥")
    elif rate >= 30:
        return ("お得 30〜49%OFF", "tier-30", "⚡")
    elif rate >= 20:
        return ("まあまあ 20〜29%OFF", "tier-20", "✨")
    else:
        return ("お知らせ 10〜19%OFF", "tier-10", "💡")


def format_price(price):
    return f"¥{price:,}"


def render_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    stars = "★" * full + "⭐" * half + "☆" * empty
    return stars


def generate_html(products, config):
    blog_title = config["blog"].get("title", "Amazon お買い得情報まとめ")
    blog_subtitle = config["blog"].get("subtitle", "リアルタイム更新！今日のセール商品を紹介")
    updated_at = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # カテゴリ別・割引率別に整理
    by_category = defaultdict(list)
    by_tier = defaultdict(list)
    for p in products:
        by_category[p["category"]].append(p)
        tier_name, _, _ = get_discount_tier(p["discount_rate"])
        by_tier[tier_name].append(p)

    # カテゴリ一覧（ソート済み）
    categories = sorted(by_category.keys())

    # 割引率ランキングTop10
    top10 = sorted(products, key=lambda x: x["discount_rate"], reverse=True)[:10]

    # カテゴリタブのHTML生成
    tab_buttons_html = '<button class="tab-btn active" data-tab="all">すべて</button>\n'
    tab_buttons_html += '<button class="tab-btn" data-tab="ranking">🏆 ランキング</button>\n'
    for cat in categories:
        tab_buttons_html += f'<button class="tab-btn" data-tab="{cat}">{cat}</button>\n'

    # 商品カードHTML生成
    def product_card(p):
        tier_name, tier_class, icon = get_discount_tier(p["discount_rate"])
        stars = render_stars(p["rating"])
        badge = p.get("badge", f"{p['discount_rate']}%OFF")
        return f"""
        <div class="product-card {tier_class}" data-category="{p['category']}" data-discount="{p['discount_rate']}">
          <div class="card-badge">{badge}</div>
          <div class="discount-badge">{icon} {p['discount_rate']}%OFF</div>
          <a href="{p['url']}" target="_blank" rel="nofollow noopener">
            <div class="product-image">
              <img src="{p['image']}" alt="{p['title']}" loading="lazy">
            </div>
            <div class="product-info">
              <h3 class="product-title">{p['title']}</h3>
              <div class="price-block">
                <span class="original-price">{format_price(p['original_price'])}</span>
                <span class="sale-price">{format_price(p['sale_price'])}</span>
                <span class="discount-tag">-{p['discount_rate']}%</span>
              </div>
              <div class="savings">
                <span>節約額: <strong>{format_price(p['original_price'] - p['sale_price'])}</strong></span>
              </div>
              <div class="rating">
                <span class="stars">{stars}</span>
                <span class="rating-value">{p['rating']}</span>
                <span class="reviews">({p['reviews']:,}件)</span>
              </div>
              <div class="buy-btn">Amazonで見る →</div>
            </div>
          </a>
        </div>"""

    # 全商品グリッド
    all_cards = "\n".join(product_card(p) for p in products)

    # ランキングカード
    ranking_cards = "\n".join(
        f'<div class="rank-item">'
        f'<span class="rank-num">#{i+1}</span>'
        f'<div class="rank-content">'
        f'<a href="{p["url"]}" target="_blank" rel="nofollow noopener">'
        f'<span class="rank-title">{p["title"][:40]}...</span>'
        f'<span class="rank-discount">{p["discount_rate"]}%OFF</span>'
        f'</a></div></div>'
        for i, p in enumerate(top10)
    )

    # カテゴリ別統計
    stats_html = ""
    for cat in categories:
        items = by_category[cat]
        avg_discount = sum(p["discount_rate"] for p in items) // len(items)
        max_discount = max(p["discount_rate"] for p in items)
        stats_html += f"""
        <div class="stat-card" onclick="filterCategory('{cat}')">
          <div class="stat-icon">{get_category_icon(cat)}</div>
          <div class="stat-name">{cat}</div>
          <div class="stat-count">{len(items)}件</div>
          <div class="stat-discount">最大 <strong>{max_discount}%</strong>OFF</div>
        </div>"""

    # 割引率フィルターボタン
    tier_filters = """
        <button class="filter-btn active" data-min="0">すべて</button>
        <button class="filter-btn" data-min="50">🔥 50%以上</button>
        <button class="filter-btn" data-min="30">⚡ 30%以上</button>
        <button class="filter-btn" data-min="20">✨ 20%以上</button>
        <button class="filter-btn" data-min="10">💡 10%以上</button>
    """

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{blog_title}</title>
  <meta name="description" content="{blog_subtitle}">
  <link rel="stylesheet" href="style.css">
</head>
<body>

<!-- ヘッダー -->
<header class="site-header">
  <div class="header-inner">
    <div class="header-logo">
      <span class="logo-icon">🛒</span>
      <div>
        <h1 class="site-title">{blog_title}</h1>
        <p class="site-subtitle">{blog_subtitle}</p>
      </div>
    </div>
    <div class="header-meta">
      <div class="update-time">
        <span class="pulse"></span>
        最終更新: <strong id="updated-at">{updated_at}</strong>
      </div>
      <div class="total-count">
        <strong>{len(products)}</strong> 件のセール商品
      </div>
    </div>
  </div>
</header>

<!-- カテゴリ統計 -->
<section class="stats-section">
  <div class="container">
    <h2 class="section-title">📊 ジャンル別セール概要</h2>
    <div class="stats-grid">
      {stats_html}
    </div>
  </div>
</section>

<!-- メインコンテンツ -->
<main class="container">

  <!-- タブナビゲーション -->
  <div class="tabs-wrapper">
    <div class="tabs" id="category-tabs">
      {tab_buttons_html}
    </div>
  </div>

  <!-- 割引率フィルター -->
  <div class="filter-bar" id="discount-filters">
    <span class="filter-label">割引率で絞り込み:</span>
    {tier_filters}
    <div class="sort-select">
      <select id="sort-order" onchange="sortProducts()">
        <option value="discount">割引率が高い順</option>
        <option value="price-low">価格が安い順</option>
        <option value="price-high">価格が高い順</option>
        <option value="rating">評価が高い順</option>
      </select>
    </div>
  </div>

  <!-- ランキングパネル -->
  <div class="tab-content" id="tab-ranking" style="display:none">
    <h2 class="section-title">🏆 割引率ランキング TOP10</h2>
    <div class="ranking-list">
      {ranking_cards}
    </div>
  </div>

  <!-- 商品グリッド -->
  <div class="products-grid" id="products-grid">
    {all_cards}
  </div>

  <div class="no-results" id="no-results" style="display:none">
    <p>条件に合う商品が見つかりませんでした</p>
  </div>

</main>

<!-- フッター -->
<footer class="site-footer">
  <div class="container">
    <p>※ このページはAmazonアソシエイトプログラムに参加しています</p>
    <p>※ 価格は変動する場合があります。購入前にAmazonで最新価格をご確認ください</p>
    <p>最終更新: {updated_at}</p>
  </div>
</footer>

<script>
// --- タブ切り替え ---
function filterCategory(cat) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const btn = [...document.querySelectorAll('.tab-btn')].find(b => b.dataset.tab === cat);
  if (btn) btn.classList.add('active');
  applyFilters();
}}

document.querySelectorAll('.tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const tab = btn.dataset.tab;
    const rankingPanel = document.getElementById('tab-ranking');
    const grid = document.getElementById('products-grid');
    const filterBar = document.getElementById('discount-filters');

    if (tab === 'ranking') {{
      rankingPanel.style.display = 'block';
      grid.style.display = 'none';
      filterBar.style.display = 'none';
    }} else {{
      rankingPanel.style.display = 'none';
      grid.style.display = 'grid';
      filterBar.style.display = 'flex';
      applyFilters();
    }}
  }});
}});

// --- 割引率フィルター ---
document.querySelectorAll('.filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    applyFilters();
  }});
}});

function applyFilters() {{
  const activeTab = document.querySelector('.tab-btn.active')?.dataset.tab || 'all';
  const minDiscount = parseInt(document.querySelector('.filter-btn.active')?.dataset.min || 0);
  const cards = document.querySelectorAll('.product-card');
  let visible = 0;

  cards.forEach(card => {{
    const cat = card.dataset.category;
    const discount = parseInt(card.dataset.discount);
    const catMatch = activeTab === 'all' || cat === activeTab;
    const discountMatch = discount >= minDiscount;
    if (catMatch && discountMatch) {{
      card.style.display = 'block';
      visible++;
    }} else {{
      card.style.display = 'none';
    }}
  }});

  document.getElementById('no-results').style.display = visible === 0 ? 'block' : 'none';
}}

// --- ソート ---
function sortProducts() {{
  const order = document.getElementById('sort-order').value;
  const grid = document.getElementById('products-grid');
  const cards = [...grid.querySelectorAll('.product-card')];

  cards.sort((a, b) => {{
    if (order === 'discount') return parseInt(b.dataset.discount) - parseInt(a.dataset.discount);
    if (order === 'price-low') return getPriceFromCard(a) - getPriceFromCard(b);
    if (order === 'price-high') return getPriceFromCard(b) - getPriceFromCard(a);
    if (order === 'rating') return getRatingFromCard(b) - getRatingFromCard(a);
    return 0;
  }});

  cards.forEach(c => grid.appendChild(c));
}}

function getPriceFromCard(card) {{
  const price = card.querySelector('.sale-price')?.textContent.replace(/[¥,]/g, '') || '0';
  return parseInt(price);
}}

function getRatingFromCard(card) {{
  const r = card.querySelector('.rating-value')?.textContent || '0';
  return parseFloat(r);
}}

// カウントダウンタイマー（次回更新まで）
function updateCountdown() {{
  const now = new Date();
  const next = new Date(now);
  next.setHours(next.getHours() + 1, 0, 0, 0);
  const diff = next - now;
  const min = Math.floor(diff / 60000);
  const sec = Math.floor((diff % 60000) / 1000);
  const el = document.getElementById('countdown');
  if (el) el.textContent = `次回更新まで ${{min}}分${{sec}}秒`;
  setTimeout(updateCountdown, 1000);
}}
updateCountdown();
</script>

</body>
</html>"""
    return html


def get_category_icon(cat):
    icons = {
        "家電・カメラ": "📷",
        "パソコン・周辺機器": "💻",
        "ゲーム": "🎮",
        "キッチン・日用品": "🍳",
        "スポーツ・アウトドア": "⛺",
        "ファッション": "👗",
        "本・雑誌": "📚",
        "ビューティー・ヘルスケア": "💄",
    }
    return icons.get(cat, "🛒")


if __name__ == "__main__":
    import sys
    config = load_config()

    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "products.json")
    with open(data_path, encoding="utf-8") as f:
        products = json.load(f)

    html = generate_html(products, config)

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config["output"]["html_file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML生成完了: {out_path}")
