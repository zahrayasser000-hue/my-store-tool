import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd
import requests
import random
import urllib.parse

st.set_page_config(page_title="ALI Engine Pro - AI Landing Pages", layout="wide", page_icon="\U0001f680")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #f8fafc;
    }
    .main-header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: 40px 20px; border-radius: 20px; text-align: center; margin-bottom: 35px; box-shadow: 0 20px 40px -10px rgba(15,23,42,0.3); border-bottom: 5px solid #3b82f6; }
    .main-header h1 { font-weight: 900; font-size: 3rem; margin-bottom: 5px; background: linear-gradient(to right, #93c5fd, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .main-header p { color: #94a3b8; font-size: 1.2rem; font-weight: 600; }
    .stButton > button { background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important; color: white !important; font-weight: 800 !important; font-size: 1.1rem !important; border: none !important; border-radius: 12px !important; padding: 15px 30px !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>ALI Growth Engine Pro \U0001f680</h1><p>منصة العمليات التسويقية المتكاملة | صور AI عالية الجودة</p></div>', unsafe_allow_html=True)


# ==========================================================
# AI Image Generation Engine (High Quality)
# ==========================================================
def get_ai_image(keyword, width=800, height=600, style="professional"):
    safe_keyword = str(keyword).strip()
    if not safe_keyword or safe_keyword.lower() == "none":
        safe_keyword = "product"
    if style == "product":
        prompt = f"professional studio product photography of {safe_keyword}, white background, high resolution, commercial quality, 8k, sharp focus, soft lighting"
    elif style == "person":
        prompt = f"professional portrait photo of {safe_keyword}, natural lighting, high quality, realistic, candid, authentic"
    elif style == "before_after":
        prompt = f"realistic before and after comparison photo of {safe_keyword}, high quality, clear difference, professional photography"
    else:
        prompt = f"professional high quality photo of {safe_keyword}, 8k, sharp, realistic, commercial photography"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model=flux"


# ==========================================================
# Auto Color Engine
# ==========================================================
AUTO_COLORS = {
    "cosmetics": {"primary": "#0f766e", "secondary": "#f0fdfa", "accent": "#eab308", "gradient1": "#0f766e", "gradient2": "#14b8a6"},
    "skincare": {"primary": "#be185d", "secondary": "#fdf2f8", "accent": "#f59e0b", "gradient1": "#be185d", "gradient2": "#ec4899"},
    "health": {"primary": "#15803d", "secondary": "#f0fdf4", "accent": "#f97316", "gradient1": "#15803d", "gradient2": "#22c55e"},
    "gadgets": {"primary": "#1e3a5f", "secondary": "#f0f4f8", "accent": "#ef4444", "gradient1": "#1e3a5f", "gradient2": "#3b82f6"},
    "fashion": {"primary": "#7c2d12", "secondary": "#fef3c7", "accent": "#d97706", "gradient1": "#7c2d12", "gradient2": "#ea580c"},
    "default": {"primary": "#1e40af", "secondary": "#eff6ff", "accent": "#f59e0b", "gradient1": "#1e40af", "gradient2": "#3b82f6"}
}

def detect_colors(product_name, category):
    text = (product_name + " " + category).lower()
    if any(w in text for w in ["cream", "كريم", "collagen", "كولاجين", "serum", "سيروم", "cosmetic", "تجميل"]):
        return AUTO_COLORS["skincare"]
    elif any(w in text for w in ["skin", "بشرة", "face", "وجه", "beauty", "جمال"]):
        return AUTO_COLORS["cosmetics"]
    elif any(w in text for w in ["health", "صحة", "vitamin", "فيتامين", "supplement", "مكمل"]):
        return AUTO_COLORS["health"]
    elif any(w in text for w in ["gadget", "جهاز", "device", "أداة", "smart", "ذكي"]):
        return AUTO_COLORS["gadgets"]
    elif any(w in text for w in ["fashion", "موضة", "clothes", "ملابس"]):
        return AUTO_COLORS["fashion"]
    elif "cosmetics" in text.lower() or "Cosmetics" in category:
        return AUTO_COLORS["cosmetics"]
    else:
        return AUTO_COLORS["default"]


# ==========================================================
# Gemini AI Functions
# ==========================================================
def get_fast_working_model(api_key):
    if 'valid_model_name' in st.session_state:
        return st.session_state.valid_model_name
    genai.configure(api_key=api_key, transport="rest")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.valid_model_name = m.name
                return m.name
    except:
        pass
    st.session_state.valid_model_name = "gemini-pro"
    return "gemini-pro"


def generate_landing_page_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
أنت خبير Copywriter لصفحات الهبوط. المنتج: "{product}". الفئة: "{category}".
النصوص بالعربية الفصحى. الحقول المنتهية بـ _search هي كلمات بالإنجليزية لتوليد صور AI.
رد بصيغة JSON صالحة:
{{
  "hero_headline": "عنوان رئيسي يخطف الانتباه",
  "hero_subheadline": "عنوان فرعي",
  "image_hero_search": "english keyword for product",
  "trust_badges": ["شحن مجاني", "الدفع عند الاستلام", "ضمان 30 يوم"],
  "problem_title": "عنوان قسم الألم",
  "problem_description": "فقرة تصف الإحباط",
  "problem_points": ["مشكلة 1", "مشكلة 2", "مشكلة 3"],
  "image_problem_search": "english keyword for problem",
  "solution_title": "عنوان الحل",
  "solution_description": "فقرة الحل",
  "image_solution_search": "english keyword for solution",
  "image_before_search": "english keyword before",
  "image_after_search": "english keyword after",
  "features": [
    {{"title": "ميزة 1", "desc": "الفائدة", "icon": "sparkles", "image_search": "keyword1"}},
    {{"title": "ميزة 2", "desc": "الفائدة", "icon": "shield", "image_search": "keyword2"}},
    {{"title": "ميزة 3", "desc": "الفائدة", "icon": "heart", "image_search": "keyword3"}},
    {{"title": "ميزة 4", "desc": "الفائدة", "icon": "check", "image_search": "keyword4"}}
  ],
  "ingredients": [
    {{"name": "مكون 1", "benefit": "فائدته", "image_search": "ingredient keyword"}},
    {{"name": "مكون 2", "benefit": "فائدته", "image_search": "ingredient keyword"}},
    {{"name": "مكون 3", "benefit": "فائدته", "image_search": "ingredient keyword"}}
  ],
  "how_to_use": ["خطوة 1", "خطوة 2", "خطوة 3"],
  "stats": [{{"number": "98%", "label": "إحصائية 1"}}, {{"number": "+5000", "label": "إحصائية 2"}}, {{"number": "4.9/5", "label": "إحصائية 3"}}],
  "reviews": [
    {{"name": "سارة م.", "rating": 5, "comment": "تعليق واقعي", "image_search": "happy arab woman selfie"}},
    {{"name": "أحمد ع.", "rating": 5, "comment": "تعليق واقعي", "image_search": "satisfied arab man"}},
    {{"name": "نورة ك.", "rating": 4, "comment": "تعليق واقعي", "image_search": "happy woman portrait"}}
  ],
  "pricing": {{"original": "399", "discounted": "199", "currency": "SAR", "discount_percent": "50%"}},
  "urgency_text": "العرض ينتهي خلال 24 ساعة!",
  "faq": [
    {{"q": "متى سألاحظ النتائج؟", "a": "إجابة"}},
    {{"q": "هل المنتج آمن؟", "a": "إجابة"}},
    {{"q": "كيف أطلب؟", "a": "إجابة"}},
    {{"q": "ما سياسة الإرجاع؟", "a": "إجابة"}}
  ],
  "guarantee_title": "ضمان استرجاع المال",
  "guarantee_text": "نص الضمان",
  "call_to_action": "اطلب الآن",
  "footer_text": "جميع الحقوق محفوظة"
}}
"""
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    tb = chr(96) * 3
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match:
        return match.group(0)
    return clean_text


def generate_deep_research(api_key, product_name, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
أنت أداة Deep Research. المنتج: "{product_name}". الفئة: "{category}".
أخرج تقريراً شاملاً بالعربية بتنسيق Markdown:
1. وثيقة شخصية العميل (Avatar Sheet)
2. وثيقة بحث السوق والمنافسين
3. وثيقة ملخص العرض (Offer Brief)
4. وثيقة المعتقدات الضرورية
5. زوايا البيع الجاهزة (PAS + FAB)
"""
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    return response.text


# ==========================================================
# HTML Builder - 15 Sections Landing Page
# ==========================================================
def build_landing_page_html(data, colors):
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]
    g1 = colors["gradient1"]
    g2 = colors["gradient2"]

    hero_img = get_ai_image(data.get('image_hero_search', 'product'), 900, 1100, 'product')
    prob_img = get_ai_image(data.get('image_problem_search', 'worried person'), 700, 500, 'person')
    sol_img = get_ai_image(data.get('image_solution_search', 'happy person'), 800, 600, 'person')
    before_img = get_ai_image(data.get('image_before_search', 'before treatment'), 500, 600, 'before_after')
    after_img = get_ai_image(data.get('image_after_search', 'after treatment'), 500, 600, 'before_after')

    # Build trust badges
    badges_html = ""
    for badge in data.get('trust_badges', []):
        badges_html += f'<span style="background:rgba(255,255,255,0.15);padding:8px 18px;border-radius:50px;font-size:0.85rem;font-weight:600;">{badge}</span> '

    # Build problem points
    problems_html = ""
    for pt in data.get('problem_points', []):
        problems_html += f'<li style="padding:8px 0;font-size:1.05rem;">\u274c {pt}</li>'

    # Build features with images
    features_html = ""
    for feat in data.get('features', [])[:4]:
        feat_img = get_ai_image(feat.get('image_search', 'feature'), 300, 300, 'product')
        features_html += f'''<div style="background:white;border-radius:16px;padding:25px;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
            <img src="{feat_img}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;margin-bottom:15px;" alt="">
            <h4 style="color:{p};font-size:1.1rem;margin-bottom:8px;">{feat.get('title','')}</h4>
            <p style="color:#64748b;font-size:0.9rem;">{feat.get('desc','')}</p>
        </div>'''

    # Build ingredients
    ingredients_html = ""
    for ing in data.get('ingredients', [])[:3]:
        ing_img = get_ai_image(ing.get('image_search', 'natural ingredient'), 250, 250, 'product')
        ingredients_html += f'''<div style="text-align:center;padding:20px;">
            <img src="{ing_img}" style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:3px solid {a};" alt="">
            <h4 style="color:{p};margin-top:12px;">{ing.get('name','')}</h4>
            <p style="color:#64748b;font-size:0.9rem;">{ing.get('benefit','')}</p>
        </div>'''

    # Build how to use
    steps_html = ""
    for i, step in enumerate(data.get('how_to_use', [])[:3], 1):
        steps_html += f'''<div style="text-align:center;padding:20px;">
            <div style="background:linear-gradient(135deg,{g1},{g2});color:white;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.3rem;margin:0 auto 12px;">{i}</div>
            <p style="font-weight:600;color:#1e293b;">{step}</p>
        </div>'''

    # Build stats
    stats_html = ""
    for stat in data.get('stats', [])[:3]:
        stats_html += f'''<div style="text-align:center;padding:20px;">
            <div style="font-size:2.5rem;font-weight:900;color:{a};">{stat.get('number','')}</div>
            <p style="color:white;font-weight:600;margin-top:5px;">{stat.get('label','')}</p>
        </div>'''

    # Build reviews
    reviews_html = ""
    for rev in data.get('reviews', [])[:3]:
        stars = '\u2b50' * int(rev.get('rating', 5))
        rev_img = get_ai_image(rev.get('image_search', 'person portrait'), 150, 150, 'person')
        reviews_html += f'''<div style="background:white;border-radius:16px;padding:25px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <img src="{rev_img}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;" alt="">
                <div><strong>{rev.get('name','')}</strong><br><span style="color:{a};">{stars}</span></div>
            </div>
            <p style="color:#475569;font-style:italic;">"{rev.get('comment','')}"</p>
            <p style="color:#22c55e;font-size:0.8rem;margin-top:8px;">\u2705 مشتري موثق</p>
        </div>'''

    # Build FAQ
    faq_html = ""
    for faq in data.get('faq', [])[:4]:
        faq_html += f'''<details style="background:white;border-radius:12px;padding:18px;margin-bottom:10px;box-shadow:0 2px 8px rgba(0,0,0,0.05);cursor:pointer;">
            <summary style="font-weight:700;color:{p};font-size:1.05rem;">{faq.get('q','')}</summary>
            <p style="color:#64748b;margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0;">{faq.get('a','')}</p>
        </details>'''

    pricing = data.get('pricing', {})
    cta = data.get('call_to_action', 'اطلب الآن')

    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Cairo',sans-serif; background:{s}; color:#1e293b; direction:rtl; scroll-behavior:smooth; }}
        img {{ max-width:100%; height:auto; }}
        .container {{ max-width:800px; margin:0 auto; padding:0 20px; }}
        .btn {{ display:inline-block; background:linear-gradient(135deg,{a},{a}dd); color:white; padding:18px 45px; border-radius:12px; font-weight:800; font-size:1.2rem; text-decoration:none; text-align:center; box-shadow:0 8px 25px {a}44; transition:all 0.3s; border:none; cursor:pointer; width:100%; max-width:400px; }}
        .btn:hover {{ transform:translateY(-3px); box-shadow:0 12px 35px {a}66; }}
        .section {{ padding:50px 20px; }}
        .section-title {{ font-size:1.8rem; font-weight:900; color:{p}; text-align:center; margin-bottom:25px; }}
    </style>
</head>
<body>

<!-- 1. Top Bar -->
<div style="background:{p};color:white;text-align:center;padding:12px;font-size:0.9rem;">
    <div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">{badges_html}</div>
</div>

<!-- 2. Hero Section -->
<section style="background:linear-gradient(135deg,{g1},{g2});color:white;padding:60px 20px;text-align:center;">
    <div class="container">
        <h1 style="font-size:2.5rem;font-weight:900;margin-bottom:15px;line-height:1.4;">{data.get('hero_headline','')}</h1>
        <p style="font-size:1.2rem;opacity:0.9;margin-bottom:25px;">{data.get('hero_subheadline','')}</p>
        <img src="{hero_img}" style="max-width:350px;border-radius:20px;box-shadow:0 20px 50px rgba(0,0,0,0.3);margin:20px auto;display:block;" alt="">
        <a href="#order" class="btn" style="margin-top:25px;">{cta}</a>
    </div>
</section>

<!-- 3. Problem Section -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">\u26a0\ufe0f {data.get('problem_title','')}</h2>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center;">
            <div>
                <p style="font-size:1.1rem;color:#475569;line-height:1.8;margin-bottom:15px;">{data.get('problem_description','')}</p>
                <ul style="list-style:none;padding:0;">{problems_html}</ul>
            </div>
            <img src="{prob_img}" style="border-radius:16px;width:100%;" alt="">
        </div>
    </div>
</section>

<!-- 4. Solution Section -->
<section class="section" style="background:linear-gradient(135deg,{g1},{g2});color:white;">
    <div class="container">
        <h2 style="font-size:1.8rem;font-weight:900;text-align:center;margin-bottom:25px;">\u2728 {data.get('solution_title','')}</h2>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center;">
            <div><p style="font-size:1.1rem;line-height:1.8;">{data.get('solution_description','')}</p></div>
            <img src="{sol_img}" style="border-radius:16px;width:100%;box-shadow:0 10px 30px rgba(0,0,0,0.2);" alt="">
        </div>
    </div>
</section>

<!-- 5. Before/After -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">تحول مذهل تلاحظه فوراً!</h2>
        <div style="display:grid;grid-template-columns:1fr 60px 1fr;gap:15px;align-items:center;text-align:center;">
            <div><img src="{before_img}" style="border-radius:16px;width:100%;border:3px solid #ef4444;" alt=""><p style="margin-top:10px;font-weight:700;color:#ef4444;">قبل</p></div>
            <div style="font-size:2rem;font-weight:900;color:{a};">\u27a1</div>
            <div><img src="{after_img}" style="border-radius:16px;width:100%;border:3px solid #22c55e;" alt=""><p style="margin-top:10px;font-weight:700;color:#22c55e;">بعد</p></div>
        </div>
    </div>
</section>

<!-- 6. Features Section -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">لماذا هذا المنتج مختلف؟</h2>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">{features_html}</div>
    </div>
</section>

<!-- 7. Ingredients/Components -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">السر في مكوناتنا</h2>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">{ingredients_html}</div>
    </div>
</section>

<!-- 8. How To Use -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">كيف تستخدمه؟</h2>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">{steps_html}</div>
    </div>
</section>

<!-- 9. Stats Section -->
<section style="background:linear-gradient(135deg,{g1},{g2});padding:40px 20px;">
    <div class="container">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">{stats_html}</div>
    </div>
</section>

<!-- 10. Video Section -->
<section class="section" style="background:{s};">
    <div class="container" style="text-align:center;">
        <h2 class="section-title">شاهد تجارب عملائنا</h2>
        <div style="background:#1e293b;border-radius:16px;padding:60px;color:white;">
            <p style="font-size:3rem;">\u25b6\ufe0f</p>
            <p style="margin-top:10px;opacity:0.7;">ضع رابط فيديو يوتيوب هنا</p>
        </div>
    </div>
</section>

<!-- 11. Reviews -->
<section class="section" style="background:white;">
    <div class="container">
        <h2 class="section-title">آراء العملاء</h2>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">{reviews_html}</div>
    </div>
</section>

<!-- 12. Pricing -->
<section id="order" class="section" style="background:linear-gradient(135deg,{g1},{g2});color:white;text-align:center;">
    <div class="container">
        <h2 style="font-size:1.8rem;font-weight:900;margin-bottom:20px;">احصل عليه الآن!</h2>
        <div style="background:white;border-radius:20px;padding:30px;display:inline-block;">
            <p style="color:#94a3b8;text-decoration:line-through;font-size:1.3rem;">{pricing.get('original','')} {pricing.get('currency','')}</p>
            <p style="color:{p};font-size:2.5rem;font-weight:900;">{pricing.get('discounted','')} {pricing.get('currency','')}</p>
            <p style="background:{a};color:white;display:inline-block;padding:5px 15px;border-radius:50px;font-weight:700;margin-top:10px;">خصم {pricing.get('discount_percent','')}</p>
        </div>
        <p style="margin-top:15px;font-size:1.1rem;font-weight:600;color:#fbbf24;">{data.get('urgency_text','')}</p>
        <a href="#" class="btn" style="margin-top:20px;display:inline-block;">{cta}</a>
    </div>
</section>

<!-- 13. FAQ -->
<section class="section" style="background:{s};">
    <div class="container">
        <h2 class="section-title">\u2753 الأسئلة الشائعة</h2>
        {faq_html}
    </div>
</section>

<!-- 14. Guarantee -->
<section class="section" style="background:white;text-align:center;">
    <div class="container">
        <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:2px solid #22c55e;border-radius:20px;padding:40px;">
            <p style="font-size:3rem;">\U0001f6e1</p>
            <h3 style="color:#15803d;font-size:1.5rem;margin:15px 0;">{data.get('guarantee_title','')}</h3>
            <p style="color:#475569;font-size:1.05rem;">{data.get('guarantee_text','')}</p>
        </div>
    </div>
</section>

<!-- 15. Footer CTA -->
<section style="background:{p};color:white;padding:40px 20px;text-align:center;">
    <div class="container">
        <h2 style="font-size:1.5rem;font-weight:900;margin-bottom:15px;">لا تفوت هذا العرض!</h2>
        <a href="#order" class="btn" style="display:inline-block;">{cta}</a>
        <p style="margin-top:20px;opacity:0.6;font-size:0.85rem;">{data.get('footer_text','')}</p>
    </div>
</section>

</body>
</html>'''
    return html


# ==========================================================
# UI - Sidebar and Main
# ==========================================================
with st.sidebar:
    st.header("⚙️ الإعدادات العامة")
    global_api_key = st.text_input("🔑 Gemini API Key", type="password")
    global_product_name = st.text_area("📦 تفاصيل واسم المنتج", placeholder="مثال: كريم كولاجين كوري للبشرة")
    global_category = st.selectbox("📦 فئة المنتج", ["💄 مستحضرات تجميل وعناية (Cosmetics)", "⚙️ أدوات وأجهزة ذكية (Gadgets)"])
    st.markdown("---")
    st.header("🛠️ اختر الأداة")
    app_mode = st.radio("قائمة التحكم:", ["🏗️ منشئ صفحات الهبوط", "🔍 بحث السوق المعمق (SOP-1)", "💰 حاسبة التعادل المالي (Matrix)"])
    st.markdown("---")

if app_mode == "🏗️ منشئ صفحات الهبوط":
    start_btn = st.button("🚀 توليد صفحة الهبوط (15 قسم + صور AI)")
    if start_btn:
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال المفتاح واسم المنتج.")
        else:
            with st.spinner("🤖 جاري بناء صفحة الهبوط بـ 15 قسم + صور AI عالية الجودة..."):
                try:
                    raw_json = generate_landing_page_json(global_api_key, global_product_name, global_category)
                    parsed_data = json.loads(raw_json)
                    auto_colors = detect_colors(global_product_name, global_category)
                    st.session_state.final_page = build_landing_page_html(parsed_data, auto_colors)
                    st.success("🎉 اكتمل البناء! 15 قسم + صور AI + ألوان تلقائية")
                except Exception as e:
                    st.error(f"🛑 خطأ: {str(e)}")
    if 'final_page' in st.session_state:
        tab1, tab2 = st.tabs(["📱 المعاينة البصرية", "💻 كود HTML"])
        with tab1:
            components.html(st.session_state.final_page, height=2500, scrolling=True)
        with tab2:
            st.code(st.session_state.final_page, language="html")

elif app_mode == "🔍 بحث السوق المعمق (SOP-1)":
    st.markdown("### 🔍 البحث المعمق في السوق")
    if st.button("🧠 استخراج وثائق البيع"):
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال المفتاح واسم المنتج.")
        else:
            with st.spinner("🕵️‍♂️ جاري البحث..."):
                try:
                    result = generate_deep_research(global_api_key, global_product_name, global_category)
                    st.session_state.research_output = result
                    st.success("✅ اكتمل البحث!")
                except Exception as e:
                    st.error(f"🛑 {str(e)}")
    if 'research_output' in st.session_state:
        st.markdown(st.session_state.research_output)

elif app_mode == "💰 حاسبة التعادل المالي (Matrix)":
    st.markdown("### 💰 حاسبة نقطة التعادل")
    COUNTRIES = {
        "السعودية": {"currency": "SAR", "P": 199.0, "C": 85.0, "CPL": 25.0},
        "الإمارات": {"currency": "AED", "P": 149.0, "C": 60.0, "CPL": 30.0},
        "الكويت": {"currency": "KWD", "P": 19.0, "C": 8.0, "CPL": 2.5},
        "المغرب": {"currency": "MAD", "P": 299.0, "C": 120.0, "CPL": 40.0},
        "مصر": {"currency": "EGP", "P": 500.0, "C": 200.0, "CPL": 50.0},
        "أخرى": {"currency": "USD", "P": 50.0, "C": 20.0, "CPL": 5.0},
    }
    sel = st.selectbox("🌍 الدولة:", list(COUNTRIES.keys()))
    d = COUNTRIES[sel]
    c1, c2, c3 = st.columns(3)
    P = c1.number_input(f"سعر البيع [{d['currency']}]", value=d["P"])
    C = c2.number_input(f"التكلفة [{d['currency']}]", value=d["C"])
    CPL = c3.number_input(f"CPL [{d['currency']}]", value=d["CPL"])
    c4, c5 = st.columns(2)
    CR = c4.slider("CR %", 10, 100, 60) / 100
    DR = c5.slider("DR %", 10, 100, 55) / 100
    margin = P - C
    max_cpl = margin * CR * DR
    profit = max_cpl - CPL
    m1, m2, m3 = st.columns(3)
    m1.metric("هامش الربح", f"{margin:.2f} {d['currency']}")
    m2.metric("أقصى CPL", f"{max_cpl:.2f} {d['currency']}")
    if profit >= 0:
        m3.metric("الحالة", "✅ رابح", f"+{profit:.2f}")
    else:
        m3.metric("الحالة", "🚨 خاسر", f"{profit:.2f}")
