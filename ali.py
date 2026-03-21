import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd
import requests
import random
import urllib.parse
import base64
import time

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

st.markdown('<div class="main-header"><h1>ALI Growth Engine Pro \U0001f680</h1><p>\u0645\u0646\u0635\u0629 \u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a \u0627\u0644\u062a\u0633\u0648\u064a\u0642\u064a\u0629 \u0627\u0644\u0645\u062a\u0643\u0627\u0645\u0644\u0629 | \u0635\u0648\u0631 AI \u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062c\u0648\u062f\u0629</p></div>', unsafe_allow_html=True)

def get_ai_image(keyword, width=800, height=600, style="professional"):
    safe_keyword = str(keyword).strip()
    if not safe_keyword or safe_keyword.lower() == "none":
        safe_keyword = "product"
    prompts = {
        "product": f"{safe_keyword} product photo white background studio",
        "person": f"{safe_keyword} portrait natural light realistic",
        "before_after": f"realistic before and after comparison photo of {safe_keyword}, high quality, clear difference, professional photography",
        "lifestyle": f"lifestyle photography of person using {safe_keyword}, natural setting, warm lighting, authentic, high quality, 8k",
        "ingredient": f"close up macro photography of {safe_keyword}, natural organic ingredient, studio lighting, white background, 8k, detailed texture",
        "dimensions": f"product dimensions diagram of {safe_keyword}, measurement overlay, clean white background, professional product photo with size reference, 8k",
        "gif_step": f"step by step tutorial photo showing how to use {safe_keyword}, clean hands demonstration, bright lighting, instructional photography, 8k",
        "problem": f"frustrated person experiencing problem related to {safe_keyword}, worried expression, dramatic lighting, realistic, high quality, 8k",
        "solution": f"happy satisfied person after using {safe_keyword}, bright smile, positive mood, natural lighting, high quality, 8k",
        "feature": f"detailed highlight of {safe_keyword}, clean modern aesthetic, studio lighting, detailed close up, commercial photography, 8k",
        "review": f"customer selfie with {safe_keyword}, casual setting, smartphone photo style, realistic, genuine smile, 8k",
    }
    prompt = prompts.get(style, f"{safe_keyword} high quality realistic photo")
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&nofeed=true&model=flux&seed={seed}"

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
    if any(w in text for w in ["cream", "\u0643\u0631\u064a\u0645", "collagen", "\u0643\u0648\u0644\u0627\u062c\u064a\u0646", "serum", "\u0633\u064a\u0631\u0648\u0645", "cosmetic", "\u062a\u062c\u0645\u064a\u0644"]):
        return AUTO_COLORS["skincare"]
    elif any(w in text for w in ["skin", "\u0628\u0634\u0631\u0629", "face", "\u0648\u062c\u0647", "beauty", "\u062c\u0645\u0627\u0644"]):
        return AUTO_COLORS["cosmetics"]
    elif any(w in text for w in ["health", "\u0635\u062d\u0629", "vitamin", "\u0641\u064a\u062a\u0627\u0645\u064a\u0646", "supplement", "\u0645\u0643\u0645\u0644"]):
        return AUTO_COLORS["health"]
    elif any(w in text for w in ["gadget", "\u062c\u0647\u0627\u0632", "device", "\u0623\u062f\u0627\u0629", "smart", "\u0630\u0643\u064a"]):
        return AUTO_COLORS["gadgets"]
    elif any(w in text for w in ["fashion", "\u0645\u0648\u0636\u0629", "clothes", "\u0645\u0644\u0627\u0628\u0633"]):
        return AUTO_COLORS["fashion"]
    elif "cosmetics" in text.lower() or "Cosmetics" in category:
        return AUTO_COLORS["cosmetics"]
    else:
        return AUTO_COLORS["default"]

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
\u0623\u0646\u062a \u062e\u0628\u064a\u0631 Copywriter \u0644\u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637.
\u0627\u0644\u0645\u0646\u062a\u062c: "{product}". \u0627\u0644\u0641\u0626\u0629: "{category}".
\u0627\u0644\u0646\u0635\u0648\u0635 \u0628\u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u0627\u0644\u0641\u0635\u062d\u0649.
\u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0645\u0646\u062a\u0647\u064a\u0629 \u0628\u0640 _search \u0647\u064a \u0643\u0644\u0645\u0627\u062a \u0628\u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629 \u0644\u062a\u0648\u0644\u064a\u062f \u0635\u0648\u0631 AI \u062a\u0643\u0648\u0646 \u0645\u0646\u0627\u0633\u0628\u0629 \u0644\u0644\u0646\u0635 \u0627\u0644\u0645\u062c\u0627\u0648\u0631.
\u0631\u062f \u0628\u0635\u064a\u063a\u0629 JSON \u0635\u0627\u0644\u062d\u0629:
{{
    "hero_headline": "\u0639\u0646\u0648\u0627\u0646 \u0631\u0626\u064a\u0633\u064a \u064a\u062e\u0637\u0641 \u0627\u0644\u0627\u0646\u062a\u0628\u0627\u0647",
    "hero_subheadline": "\u0639\u0646\u0648\u0627\u0646 \u0641\u0631\u0639\u064a",
    "image_hero_search": "english keyword for product photo",
    "image_hero_lifestyle_search": "english keyword lifestyle photo of person using product",
    "image_hero_closeup_search": "english keyword close up detail of product",
    "trust_badges": ["\u0634\u062d\u0646 \u0645\u062c\u0627\u0646\u064a", "\u0627\u0644\u062f\u0641\u0639 \u0639\u0646\u062f \u0627\u0644\u0627\u0633\u062a\u0644\u0627\u0645", "\u0636\u0645\u0627\u0646 30 \u064a\u0648\u0645"],
    "social_proof_number": "+12,000",
    "social_proof_text": "\u0639\u0645\u064a\u0644 \u0633\u0639\u064a\u062f",
    "problem_title": "\u0639\u0646\u0648\u0627\u0646 \u0642\u0633\u0645 \u0627\u0644\u0623\u0644\u0645",
    "problem_description": "\u0641\u0642\u0631\u0629 \u062a\u0635\u0641 \u0627\u0644\u0625\u062d\u0628\u0627\u0637",
    "problem_points": ["\u0645\u0634\u0643\u0644\u0629 1", "\u0645\u0634\u0643\u0644\u0629 2", "\u0645\u0634\u0643\u0644\u0629 3"],
    "image_problem_search": "english keyword for problem visual matching the problem text",
    "image_problem_2_search": "english keyword second problem visual",
    "solution_title": "\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u062d\u0644",
    "solution_description": "\u0641\u0642\u0631\u0629 \u0627\u0644\u062d\u0644",
    "image_solution_search": "english keyword for solution matching solution text",
    "image_solution_2_search": "english keyword second solution visual",
    "image_before_search": "english keyword before",
    "image_after_search": "english keyword after",
    "features": [
        {{"title": "\u0645\u064a\u0632\u0629 1", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "sparkles", "image_search": "keyword matching this feature"}},
        {{"title": "\u0645\u064a\u0632\u0629 2", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "shield", "image_search": "keyword2"}},
        {{"title": "\u0645\u064a\u0632\u0629 3", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "heart", "image_search": "keyword3"}},
        {{"title": "\u0645\u064a\u0632\u0629 4", "desc": "\u0627\u0644\u0641\u0627\u0626\u062f\u0629", "icon": "check", "image_search": "keyword4"}}
    ],
    "ingredients": [
        {{"name": "\u0645\u0643\u0648\u0646 1", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}},
        {{"name": "\u0645\u0643\u0648\u0646 2", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}},
        {{"name": "\u0645\u0643\u0648\u0646 3", "benefit": "\u0641\u0627\u0626\u062f\u062a\u0647", "image_search": "ingredient keyword"}}
    ],
    "how_to_use": ["\u062e\u0637\u0648\u0629 1", "\u062e\u0637\u0648\u0629 2", "\u062e\u0637\u0648\u0629 3"],
    "how_to_use_images": ["step 1 keyword", "step 2 keyword", "step 3 keyword"],
    "dimensions": {{"height": "15 cm", "width": "8 cm", "weight": "200g", "volume": "50ml", "image_search": "product with ruler measurement"}},
    "stats": [{{"number": "98%", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 1"}}, {{"number": "+5000", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 2"}}, {{"number": "4.9/5", "label": "\u0625\u062d\u0635\u0627\u0626\u064a\u0629 3"}}],
    "reviews": [
        {{"name": "\u0633\u0627\u0631\u0629 \u0645.", "rating": 5, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "happy arab woman selfie"}},
        {{"name": "\u0623\u062d\u0645\u062f \u0639.", "rating": 5, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "satisfied arab man"}},
        {{"name": "\u0646\u0648\u0631\u0629 \u0643.", "rating": 4, "comment": "\u062a\u0639\u0644\u064a\u0642 \u0648\u0627\u0642\u0639\u064a", "image_search": "happy woman portrait"}}
    ],
    "pricing": {{"original": "399", "discounted": "199", "currency": "SAR", "discount_percent": "50%"}},
    "urgency_text": "\u0627\u0644\u0639\u0631\u0636 \u064a\u0646\u062a\u0647\u064a \u062e\u0644\u0627\u0644 24 \u0633\u0627\u0639\u0629!",
    "countdown_hours": 24,
    "faq": [
        {{"q": "\u0645\u062a\u0649 \u0633\u0623\u0644\u0627\u062d\u0638 \u0627\u0644\u0646\u062a\u0627\u0626\u062c\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0647\u0644 \u0627\u0644\u0645\u0646\u062a\u062c \u0622\u0645\u0646\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0643\u064a\u0641 \u0623\u0637\u0644\u0628\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}},
        {{"q": "\u0645\u0627 \u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u0625\u0631\u062c\u0627\u0639\u061f", "a": "\u0625\u062c\u0627\u0628\u0629"}}
    ],
    "guarantee_title": "\u0636\u0645\u0627\u0646 \u0627\u0633\u062a\u0631\u062c\u0627\u0639 \u0627\u0644\u0645\u0627\u0644",
    "guarantee_text": "\u0646\u0635 \u0627\u0644\u0636\u0645\u0627\u0646",
    "call_to_action": "\u0627\u0637\u0644\u0628 \u0627\u0644\u0622\u0646",
    "footer_text": "\u062c\u0645\u064a\u0639 \u0627\u0644\u062d\u0642\u0648\u0642 \u0645\u062d\u0641\u0648\u0638\u0629"
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
\u0623\u0646\u062a \u0623\u062f\u0627\u0629 Deep Research.
\u0627\u0644\u0645\u0646\u062a\u062c: "{product_name}". \u0627\u0644\u0641\u0626\u0629: "{category}".
\u0623\u062e\u0631\u062c \u062a\u0642\u0631\u064a\u0631\u0627\u064b \u0634\u0627\u0645\u0644\u0627\u064b \u0628\u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u0628\u062a\u0646\u0633\u064a\u0642 Markdown:
1. \u0648\u062b\u064a\u0642\u0629 \u0634\u062e\u0635\u064a\u0629 \u0627\u0644\u0639\u0645\u064a\u0644 (Avatar Sheet)
2. \u0648\u062b\u064a\u0642\u0629 \u0628\u062d\u062b \u0627\u0644\u0633\u0648\u0642 \u0648\u0627\u0644\u0645\u0646\u0627\u0641\u0633\u064a\u0646
3. \u0648\u062b\u064a\u0642\u0629 \u0645\u0644\u062e\u0635 \u0627\u0644\u0639\u0631\u0636 (Offer Brief)
4. \u0648\u062b\u064a\u0642\u0629 \u0627\u0644\u0645\u0639\u062a\u0642\u062f\u0627\u062a \u0627\u0644\u0636\u0631\u0648\u0631\u064a\u0629
5. \u0632\u0648\u0627\u064a\u0627 \u0627\u0644\u0628\u064a\u0639 \u0627\u0644\u062c\u0627\u0647\u0632\u0629 (PAS + FAB)
"""
    response = model.generate_content(prompt, request_options={"timeout": 60.0})
    return response.text

def build_landing_page_html(data, colors):
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]
    g1 = colors["gradient1"]
    g2 = colors["gradient2"]

    hero_img = get_ai_image(data.get('image_hero_search', 'product'), 500, 500, 'product')
    hero_lifestyle = get_ai_image(data.get('image_hero_lifestyle_search', 'person using product'), 400, 300, 'lifestyle')
    prob_img = get_ai_image(data.get('image_problem_search', 'worried person'), 400, 300, 'problem')
    sol_img = get_ai_image(data.get('image_solution_search', 'happy person'), 400, 300, 'solution')
    before_img = get_ai_image(data.get('image_before_search', 'before treatment'), 350, 350, 'before_after')
    after_img = get_ai_image(data.get('image_after_search', 'after treatment'), 350, 350, 'before_after')

    pricing = data.get('pricing', {})
    cta = data.get('call_to_action', 'اطلب الآن')
    countdown_hours = data.get('countdown_hours', 24)

    badges = data.get('trust_badges', [])
    badges_html = ''.join(f'<div class="badge-item"><span>✅</span> {b}</div>' for b in badges)

    problems_html = ''.join(f'<div class="pain-point">❌ {pt}</div>' for pt in data.get('problem_points', []))

    features_html = ''
    for feat in data.get('features', [])[:4]:
        feat_img = get_ai_image(feat.get('image_search', 'feature'), 300, 300, 'feature')
        features_html += f'''<div class="feat-card">
            <img loading="lazy" decoding="async" src="{feat_img}" alt="{feat.get('title','')}">
            <h4>{feat.get('title','')}</h4>
            <p>{feat.get('desc','')}</p>
        </div>'''

    ingredients_html = ''
    for ing in data.get('ingredients', [])[:3]:
        ing_img = get_ai_image(ing.get('image_search', 'ingredient'), 200, 200, 'ingredient')
        ingredients_html += f'''<div class="ing-card">
            <img loading="lazy" decoding="async" src="{ing_img}" alt="{ing.get('name','')}">
            <h4>{ing.get('name','')}</h4>
            <p>{ing.get('benefit','')}</p>
        </div>'''

    reviews_html = ''
    for rev in data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        rev_img = get_ai_image(rev.get('image_search', 'person'), 80, 80, 'review')
        reviews_html += f'''<div class="review-card">
            <div class="rev-top">
                <img loading="lazy" decoding="async" src="{rev_img}" class="rev-avatar">
                <div class="rev-info"><strong>{rev.get('name','')}</strong><div class="stars">{stars}</div></div>
            </div>
            <p class="rev-text">"{rev.get('comment','')}"</p>
            <span class="verified-badge">✅ مشتري موثق</span>
        </div>'''

    faq_html = ''
    for faq in data.get('faq', [])[:4]:
        faq_html += f'''<details class="faq-item">
            <summary>▸ {faq.get('q','')}</summary>
            <p>{faq.get('a','')}</p>
        </details>'''

    steps_html = ''
    step_images = data.get('how_to_use_images', [])
    for i, step in enumerate(data.get('how_to_use', [])[:3], 1):
        step_kw = step_images[i-1] if i-1 < len(step_images) else f'step {i}'
        step_img = get_ai_image(step_kw, 300, 250, 'gif_step')
        steps_html += f'''<div class="step-card">
            <div class="step-num">{i}</div>
            <img loading="lazy" decoding="async" src="{step_img}" alt="خطوة {i}">
            <p>{step}</p>
        </div>'''

    stats_html = ''
    for stat in data.get('stats', [])[:3]:
        stats_html += f'<div class="stat-box"><div class="stat-num">{stat.get("number","")}</div><div class="stat-label">{stat.get("label","")}</div></div>'

    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
//fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Cairo',sans-serif;background:#fff;color:#1a1a2e;direction:rtl;}}
img{{max-width:100%;height:auto;display:block;}}
.topbar{{background:linear-gradient(135deg,{g1},{g2});color:#fff;text-align:center;padding:12px 10px;position:sticky;top:0;z-index:999;}}
.topbar .offer-text{{font-weight:900;font-size:1.1rem;margin-bottom:6px;}}
.topbar .timer-row{{display:flex;justify-content:center;align-items:center;gap:15px;flex-wrap:wrap;font-size:0.9rem;}}
.topbar .timer-box{{background:rgba(0,0,0,0.25);padding:6px 14px;border-radius:8px;font-weight:700;font-size:1.3rem;min-width:50px;text-align:center;}}
.topbar .trust-icons{{display:flex;justify-content:center;gap:20px;margin-top:8px;font-size:0.85rem;opacity:0.95;}}
.container{{max-width:680px;margin:0 auto;padding:0 15px;}}
.hero{{background:linear-gradient(180deg,{s} 0%,#fff 100%);padding:30px 15px 20px;text-align:center;}}
.hero h1{{font-size:1.6rem;font-weight:900;color:{p};line-height:1.4;margin-bottom:10px;}}
.hero .sub{{font-size:1rem;color:#555;margin-bottom:15px;line-height:1.6;}}
.hero-img{{border-radius:16px;margin:0 auto 15px;max-width:350px;box-shadow:0 8px 30px rgba(0,0,0,0.12);}}
.badge-row{{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:15px 0;}}
.badge-item{{background:#f0fdf4;border:1px solid #bbf7d0;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;color:#166534;}}
.social-proof{{background:{a};color:#fff;text-align:center;padding:14px;font-size:1.1rem;font-weight:700;border-radius:12px;margin:15px auto;max-width:350px;}}
.btn-cta{{display:block;background:linear-gradient(135deg,{a},#f59e0b);color:#fff;padding:16px 30px;border-radius:14px;font-weight:900;font-size:1.2rem;text-decoration:none;text-align:center;max-width:400px;margin:20px auto;box-shadow:0 6px 20px {a}55;border:none;cursor:pointer;transition:transform 0.2s;}}
.btn-cta:hover{{transform:translateY(-2px);}}
.section{{padding:35px 15px;}}
.section-title{{font-size:1.5rem;font-weight:900;color:{p};text-align:center;margin-bottom:20px;line-height:1.4;}}
.section-dark{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:35px 15px;}}
.section-dark .section-title{{color:#fff;}}
.pain-point{{background:#fef2f2;border-right:4px solid #ef4444;padding:12px 16px;margin-bottom:10px;border-radius:8px;font-size:0.95rem;color:#991b1b;}}
.solution-row{{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin-bottom:20px;}}
.solution-row img{{flex:1;min-width:200px;border-radius:14px;}}
.solution-row .text-side{{flex:1;min-width:220px;}}
.ba-section{{text-align:center;}}
.ba-grid{{display:flex;justify-content:center;align-items:center;gap:10px;flex-wrap:wrap;margin:20px 0;}}
.ba-card{{text-align:center;flex:1;min-width:140px;}}
.ba-card img{{border-radius:14px;border:3px solid #e5e7eb;margin-bottom:8px;}}
.ba-card.before img{{border-color:#ef4444;}}
.ba-card.after img{{border-color:#22c55e;}}
.ba-label{{font-weight:900;font-size:1.1rem;padding:6px 20px;border-radius:20px;display:inline-block;}}
.ba-arrow{{font-size:2rem;color:{a};font-weight:900;}}
.feat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:15px;}}
.feat-card{{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.08);text-align:center;}}
.feat-card img{{width:100%;height:160px;object-fit:cover;}}
.feat-card h4{{color:{p};padding:10px 10px 0;font-size:0.95rem;}}
.feat-card p{{padding:0 10px 12px;font-size:0.85rem;color:#666;}}
.ing-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}}
.ing-card{{text-align:center;background:{s};border-radius:14px;padding:15px 8px;}}
.ing-card img{{width:80px;height:80px;border-radius:50%;margin:0 auto 8px;object-fit:cover;}}
.ing-card h4{{font-size:0.9rem;color:{p};}}
.ing-card p{{font-size:0.8rem;color:#666;}}
.steps-grid{{display:flex;gap:15px;flex-wrap:wrap;justify-content:center;}}
.step-card{{flex:1;min-width:180px;max-width:220px;text-align:center;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.06);}}
.step-num{{background:linear-gradient(135deg,{g1},{g2});color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;margin:12px auto 8px;}}
.step-card img{{width:100%;height:130px;object-fit:cover;}}
.step-card p{{padding:10px;font-size:0.85rem;}}
.stats-row{{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin:20px 0;}}
.stat-box{{text-align:center;min-width:100px;}}
.stat-num{{font-size:1.8rem;font-weight:900;color:{a};}}
.stat-label{{font-size:0.85rem;color:rgba(255,255,255,0.85);}}
.reviews-grid{{display:flex;gap:15px;flex-wrap:wrap;justify-content:center;}}
.review-card{{background:#fff;border-radius:14px;padding:16px;min-width:200px;flex:1;max-width:300px;box-shadow:0 4px 15px rgba(0,0,0,0.06);}}
.rev-top{{display:flex;align-items:center;gap:10px;margin-bottom:10px;}}
.rev-avatar{{width:50px;height:50px;border-radius:50%;object-fit:cover;}}
.rev-info strong{{display:block;font-size:0.9rem;}}
.stars{{color:#f59e0b;font-size:0.85rem;}}
.rev-text{{font-size:0.9rem;color:#444;font-style:italic;margin-bottom:8px;}}
.verified-badge{{background:#f0fdf4;color:#166534;font-size:0.75rem;padding:3px 10px;border-radius:10px;}}
.pricing-box{{text-align:center;background:linear-gradient(135deg,{s},#fff);padding:30px 15px;border-radius:20px;margin:20px auto;max-width:400px;box-shadow:0 8px 30px rgba(0,0,0,0.1);}}
.old-price{{font-size:1.3rem;color:#999;text-decoration:line-through;}}
.new-price{{font-size:2.2rem;font-weight:900;color:{p};}}
.discount-tag{{background:#ef4444;color:#fff;padding:4px 14px;border-radius:20px;font-size:0.85rem;font-weight:700;display:inline-block;margin-top:8px;}}
.faq-item{{border-bottom:1px solid #e5e7eb;padding:14px 0;}}
.faq-item summary{{font-weight:700;cursor:pointer;font-size:1rem;color:{p};}}
.faq-item p{{padding:10px 0;color:#555;font-size:0.9rem;}}
.guarantee-box{{text-align:center;background:#f0fdf4;border:2px solid #22c55e;border-radius:16px;padding:25px;margin:20px auto;max-width:500px;}}
.final-cta{{text-align:center;background:linear-gradient(135deg,{g1},{g2});padding:40px 15px;color:#fff;}}
@media(max-width:600px){{.feat-grid{{grid-template-columns:1fr;}}.ing-grid{{grid-template-columns:1fr 1fr;}}.ba-grid{{flex-direction:column;}}}}
</style>
</head>
<body>
<!-- TOPBAR -->
<div class="topbar">
<div class="offer-text">{data.get('urgency_text','')}</div>
<div class="timer-row"><div class="timer-box" id="cd-hours">00</div><span>:</span><div class="timer-box" id="cd-mins">00</div><span>:</span><div class="timer-box" id="cd-secs">00</div></div>
<div class="trust-icons">{badges_html}</div>
</div>
<!-- HERO -->
<div class="hero">
<div class="container">
<h1>{data.get('hero_headline','')}</h1>
<p class="sub">{data.get('hero_subheadline','')}</p>
<img loading="lazy" decoding="async" src="{hero_img}" alt="product" class="hero-img">
<div class="badge-row">{badges_html}</div>
<div class="social-proof">{data.get('social_proof_number','')} {data.get('social_proof_text','')}</div>
<a href="#order" class="btn-cta">{cta} &#10140;</a>
</div>
</div>
<!-- STATS -->
<div class="section-dark"><div class="container"><div class="stats-row">{stats_html}</div></div></div>
<!-- PROBLEM -->
<div class="section"><div class="container">
<h2 class="section-title">{data.get('problem_title','')}</h2>
<div class="solution-row"><img loading="lazy" decoding="async" src="{prob_img}" alt="problem"><div class="text-side"><p>{data.get('problem_description','')}</p>{problems_html}</div></div>
</div></div>
<!-- SOLUTION -->
<div class="section" style="background:{s};"><div class="container">
<h2 class="section-title">{data.get('solution_title','')}</h2>
<div class="solution-row"><div class="text-side"><p>{data.get('solution_description','')}</p></div><img loading="lazy" decoding="async" src="{sol_img}" alt="solution"></div>
</div></div>
<!-- BEFORE AFTER -->
<div class="section ba-section"><div class="container">
<h2 class="section-title">&#10024; &#1578;&#1581;&#1608;&#1604; &#1605;&#1584;&#1607;&#1604;!</h2>
<div class="ba-grid">
<div class="ba-card before"><img loading="lazy" decoding="async" src="{before_img}" alt="before"><div class="ba-label" style="background:#fef2f2;color:#ef4444;">&#1602;&#1576;&#1604;</div></div>
<div class="ba-arrow">&#10145;</div>
<div class="ba-card after"><img loading="lazy" decoding="async" src="{after_img}" alt="after"><div class="ba-label" style="background:#f0fdf4;color:#22c55e;">&#1576;&#1593;&#1583;</div></div>
</div>
<a href="#order" class="btn-cta">{cta} &#10140;</a>
</div></div>
<!-- FEATURES -->
<div class="section"><div class="container">
<h2 class="section-title">&#1604;&#1605;&#1575;&#1584;&#1575; &#1607;&#1584;&#1575; &#1575;&#1604;&#1605;&#1606;&#1578;&#1580; &#1605;&#1582;&#1578;&#1604;&#1601;&#1567;</h2>
<div class="feat-grid">{features_html}</div>
</div></div>
<!-- INGREDIENTS -->
<div class="section" style="background:{s};"><div class="container">
<h2 class="section-title">&#1575;&#1604;&#1587;&#1585; &#1601;&#1610; &#1605;&#1603;&#1608;&#1606;&#1575;&#1578;&#1606;&#1575;</h2>
<div class="ing-grid">{ingredients_html}</div>
</div></div>
<!-- HOW TO USE -->
<div class="section"><div class="container">
<h2 class="section-title">&#1603;&#1610;&#1601; &#1578;&#1587;&#1578;&#1582;&#1583;&#1605;&#1607;&#1567;</h2>
<div class="steps-grid">{steps_html}</div>
</div></div>
<!-- REVIEWS -->
<div class="section-dark"><div class="container">
<h2 class="section-title">&#1570;&#1585;&#1575;&#1569; &#1575;&#1604;&#1593;&#1605;&#1604;&#1575;&#1569;</h2>
<div class="reviews-grid">{reviews_html}</div>
</div></div>
<!-- PRICING -->
<div class="section" id="order"><div class="container">
<div class="pricing-box">
<h2 class="section-title">&#1575;&#1581;&#1589;&#1604; &#1593;&#1604;&#1610;&#1607; &#1575;&#1604;&#1570;&#1606;!</h2>
<div class="old-price">{pricing.get('original','')} {pricing.get('currency','')}</div>
<div class="new-price">{pricing.get('discounted','')} {pricing.get('currency','')}</div>
<div class="discount-tag">&#1582;&#1589;&#1605; {pricing.get('discount_percent','')}</div>
<a href="#" class="btn-cta" style="margin-top:20px;">{cta} &#10140;</a>
</div>
</div></div>
<!-- FAQ -->
<div class="section"><div class="container">
<h2 class="section-title">&#1575;&#1604;&#1571;&#1587;&#1574;&#1604;&#1577; &#1575;&#1604;&#1588;&#1575;&#1574;&#1593;&#1577;</h2>
{faq_html}
</div></div>
<!-- GUARANTEE -->
<div class="section"><div class="container">
<div class="guarantee-box">
<h3>{data.get('guarantee_title','')}</h3>
<p>{data.get('guarantee_text','')}</p>
</div>
</div></div>
<!-- FINAL CTA -->
<div class="final-cta">
<div class="container">
<h2 style="font-size:1.5rem;margin-bottom:15px;">&#1604;&#1575; &#1578;&#1601;&#1608;&#1578; &#1607;&#1584;&#1575; &#1575;&#1604;&#1593;&#1585;&#1590;!</h2>
<a href="#order" class="btn-cta" style="background:#fff;color:{p};">{cta} &#10140;</a>
<p style="margin-top:15px;font-size:0.85rem;opacity:0.8;">{data.get('footer_text','')}</p>
</div>
</div>
<script>
(function(){{
var hrs={countdown_hours};
var key='cd_end_'+document.title;
var end=localStorage.getItem(key);
if(!end){{end=Date.now()+hrs*3600000;localStorage.setItem(key,end);}}
function tick(){{
var left=Math.max(0,end-Date.now());
var h=Math.floor(left/3600000);var m=Math.floor((left%3600000)/60000);var s=Math.floor((left%60000)/1000);
var pad=function(n){{return n<10?'0'+n:n;}};
if(document.getElementById('cd-hours')){{document.getElementById('cd-hours').textContent=pad(h);document.getElementById('cd-mins').textContent=pad(m);document.getElementById('cd-secs').textContent=pad(s);}}
if(left>0)setTimeout(tick,1000);
}}
tick();
}})();
</script>
</body></html>'''

    return html

def get_youcan_html(html):
    """Convert HTML to YouCan-compatible: inline all CSS, remove scripts/style/head"""
    import re
    # 1. Extract CSS rules from <style> block
    css_map = {}
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    if style_match:
        css_text = style_match.group(1)
        for m in re.finditer(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}', css_text):
            cls_name = m.group(1)
            rules = m.group(2).strip().replace('\n', ' ')
            css_map[cls_name] = rules
    # 2. Remove <style>, <script>, and structural tags
    clean = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<!DOCTYPE[^>]*>', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'</?(?:html|head|body)[^>]*>', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'<meta[^>]*>', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'<link[^>]*>', '', clean, flags=re.IGNORECASE)
    # 3. Inline CSS classes into style attributes
    def replace_classes(m):
        tag = m.group(0)
        cls_m = re.search(r'class="([^"]+)"', tag)
        if not cls_m:
            return tag
        classes = cls_m.group(1).split()
        inline = []
        for c in classes:
            if c in css_map:
                inline.append(css_map[c])
        # Get existing style if any
        sty_m = re.search(r'style="([^"]+)"', tag)
        if sty_m:
            inline.append(sty_m.group(1).rstrip(';'))
            tag = tag.replace(f'style="{sty_m.group(1)}"', '')
        tag = tag.replace(f'class="{cls_m.group(1)}"', '')
        if inline:
            combined = '; '.join(inline)
            tag = tag.rstrip('>').rstrip('/').rstrip() + f' style="{combined}">'
        return tag
    clean = re.sub(r'<[a-zA-Z][^>]*class="[^"]+"[^>]*/?>', replace_classes, clean)
    # 4. Fix data-src
    clean = clean.replace(' data-src="', ' src="')
    # 5. Clean up extra whitespace
    clean = re.sub(r'\n\s*\n\s*\n', '\n\n', clean)
    return clean.strip()
    
def extract_image_prompts(data):
    prompts = []
    idx = [1]
    def add(section, keyword, img_type):
        pid = f"IMG_{idx[0]:02d}_{section.upper()}"
        prompt = get_ai_image(keyword, 800, 600, img_type)
        decoded = urllib.parse.unquote(prompt.split('prompt/')[1].split('?')[0]) if 'prompt/' in prompt else keyword
        prompts.append({"id": pid, "section": section, "type": img_type, "keyword": keyword, "prompt": decoded})
        idx[0] += 1
    add("hero", data.get('image_hero_search','product'), "product")
    add("hero_lifestyle", data.get('image_hero_lifestyle_search','lifestyle'), "lifestyle")
    add("hero_closeup", data.get('image_hero_closeup_search','closeup'), "product")
    add("problem", data.get('image_problem_search','problem'), "problem")
    add("problem2", data.get('image_problem_2_search','problem2'), "problem")
    add("solution", data.get('image_solution_search','solution'), "solution")
    add("solution2", data.get('image_solution_2_search','solution2'), "lifestyle")
    add("before", data.get('image_before_search','before'), "before_after")
    add("after", data.get('image_after_search','after'), "before_after")
    dims = data.get('dimensions', {})
    add("dimensions", dims.get('image_search','dimensions'), "dimensions")
    for i, feat in enumerate(data.get('features', [])[:4], 1):
        add(f"feature_{i}", feat.get('image_search','feature'), "feature")
    for i, ing in enumerate(data.get('ingredients', [])[:3], 1):
        add(f"ingredient_{i}", ing.get('image_search','ingredient'), "ingredient")
    step_imgs = data.get('how_to_use_images', [])
    for i in range(min(3, len(step_imgs))):
        add(f"step_{i+1}", step_imgs[i], "gif_step")
    for i, rev in enumerate(data.get('reviews', [])[:3], 1):
        add(f"review_{i}", rev.get('image_search','person'), "review")
    return prompts

def generate_nb_image(api_key, prompt, aspect_ratio="1:1"):
    """Generate image using Gemini Nano Banana (image generation model)"""
    try:
        genai.configure(api_key=api_key, transport="rest")
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type='image/png'
            )
        )
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    img_data = part.inline_data.data
                    b64 = base64.b64encode(img_data).decode('utf-8')
                    mime = part.inline_data.mime_type or 'image/png'
                    return f'data:{mime};base64,{b64}'
        return None
    except Exception as e:
        st.warning(f"Image gen failed for: {prompt[:50]}... Error: {str(e)[:100]}")
        return None

def generate_all_images(api_key, prompts, progress_bar=None):
    """Generate all images from prompts list and return dict of id->data_uri"""
    results = {}
    total = len(prompts)
    for i, p in enumerate(prompts):
        if progress_bar:
            progress_bar.progress((i + 1) / total, text=f"Generating image {i+1}/{total}: {p['section']}")
        data_uri = generate_nb_image(api_key, p['prompt'])
        if data_uri:
            results[p['id']] = data_uri
        time.sleep(1)  # Rate limit
    return results

def replace_images_in_html(html, image_map, prompts):
    """Replace pollinations.ai URLs in HTML with generated image data URIs"""
    import re
    # Find all pollinations image URLs in order
    pattern = r'src="(https://image\.pollinations\.ai/[^"]*)"'
    matches = list(re.finditer(pattern, html))
    # Map prompts to their order of appearance
    # Build replacement in reverse to preserve positions
    for idx, match in enumerate(reversed(matches)):
        real_idx = len(matches) - 1 - idx
        if real_idx < len(prompts):
            pid = prompts[real_idx]['id']
            if pid in image_map:
                html = html[:match.start(1)] + image_map[pid] + html[match.end(1):]
    return html
    

# UI - Sidebar and Main
with st.sidebar:
    st.header("\u2699\ufe0f \u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a \u0627\u0644\u0639\u0627\u0645\u0629")
    global_api_key = st.text_input("\U0001f511 Gemini API Key", type="password")
    global_product_name = st.text_area("\U0001f4e6 \u062a\u0641\u0627\u0635\u064a\u0644 \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c", placeholder="\u0645\u062b\u0627\u0644: \u0643\u0631\u064a\u0645 \u0643\u0648\u0644\u0627\u062c\u064a\u0646 \u0643\u0648\u0631\u064a \u0644\u0644\u0628\u0634\u0631\u0629")
    global_category = st.selectbox("\U0001f4e6 \u0641\u0626\u0629 \u0627\u0644\u0645\u0646\u062a\u062c", ["\U0001f484 \u0645\u0633\u062a\u062d\u0636\u0631\u0627\u062a \u062a\u062c\u0645\u064a\u0644 \u0648\u0639\u0646\u0627\u064a\u0629 (Cosmetics)", "\u2699\ufe0f \u0623\u062f\u0648\u0627\u062a \u0648\u0623\u062c\u0647\u0632\u0629 \u0630\u0643\u064a\u0629 (Gadgets)"])
    st.markdown("---")
    st.header("\U0001f6e0\ufe0f \u0627\u062e\u062a\u0631 \u0627\u0644\u0623\u062f\u0627\u0629")
    app_mode = st.radio("\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u062a\u062d\u0643\u0645:", ["\U0001f3d7\ufe0f \u0645\u0646\u0634\u0626 \u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637", "\U0001f50d \u0628\u062d\u062b \u0627\u0644\u0633\u0648\u0642 \u0627\u0644\u0645\u0639\u0645\u0642 (SOP-1)", "\U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644 \u0627\u0644\u0645\u0627\u0644\u064a (Matrix)"])
    st.markdown("---")

if app_mode == "\U0001f3d7\ufe0f \u0645\u0646\u0634\u0626 \u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0647\u0628\u0648\u0637":
    start_btn = st.button("\U0001f680 \u062a\u0648\u0644\u064a\u062f \u0635\u0641\u062d\u0629 \u0627\u0644\u0647\u0628\u0648\u0637 (15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI + \u0639\u062f \u062a\u0646\u0627\u0632\u0644\u064a)")
    if start_btn:
        if not global_api_key or not global_product_name:
            st.error("\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0627\u0644\u0645\u0641\u062a\u0627\u062d \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c.")
        else:
            with st.spinner("\U0001f916 \u062c\u0627\u0631\u064a \u0628\u0646\u0627\u0621 \u0635\u0641\u062d\u0629 \u0627\u0644\u0647\u0628\u0648\u0637 \u0628\u0640 15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI + \u0639\u062f \u062a\u0646\u0627\u0632\u0644\u064a..."):
                try:
                    raw_json = generate_landing_page_json(global_api_key, global_product_name, global_category)
                    try:
                        parsed_data = json.loads(raw_json)
                    except json.JSONDecodeError:
                        fixed = re.sub(r',\s*}', '}', raw_json)
                        fixed = re.sub(r',\s*]', ']', fixed)
                        fixed = re.sub(r'(["\d])\s*\n\s*"', r'\1,\n"', fixed)
                        parsed_data = json.loads(fixed)
                    st.session_state.parsed_json = parsed_data
                    auto_colors = detect_colors(global_product_name, global_category)
                    st.session_state.final_page = build_landing_page_html(parsed_data, auto_colors)
                    st.success("\U0001f389 \u0627\u0643\u062a\u0645\u0644 \u0627\u0644\u0628\u0646\u0627\u0621! 15 \u0642\u0633\u0645 + \u0635\u0648\u0631 AI + \u0639\u062f \u062a\u0646\u0627\u0632\u0644\u064a \u062a\u0644\u0642\u0627\u0626\u064a")
                except Exception as e:
                    st.error(f"\U0001f6d1 \u062e\u0637\u0623: {str(e)}")
    if 'final_page' in st.session_state:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["\U0001f4f1 \u0627\u0644\u0645\u0639\u0627\u064a\u0646\u0629 \u0627\u0644\u0628\u0635\u0631\u064a\u0629", "\U0001f916 \u062a\u0648\u0644\u064a\u062f \u0627\u0644\u0635\u0648\u0631 AI
def generate_nb_image", "\U0001f4e5 \u062a\u062d\u0645\u064a\u0644 JSON", "\U0001f4e4 YouCan HTML", "🎨 مولد البرومبتات"])
        with tab1:
            components.html(st.session_state.final_page, height=4000, scrolling=True)
        with tab2:
            if 'parsed_json' in st.session_state:
                st.markdown("### \U0001f916 توليد الصور بالذكاء الاصطناعي")
                st.info("اضغط الزر لتوليد جميع الصور تلقائياً باستخدام Gemini وإدراجها في صفحة الهبوط")
                prompts = extract_image_prompts(st.session_state.parsed_json)
                if st.button("\U0001f680 توليد جميع الصور وإدراجها تلقائياً", key="gen_ai_imgs"):
                    if not global_api_key:
                        st.error("الرجاء إدخال مفتاح Gemini API")
                    else:
                        progress = st.progress(0)
                        status = st.empty()
                        generated = {}
                        for i, p in enumerate(prompts):
                            status.text(f"جاري توليد {p['id']}... ({i+1}/{len(prompts)})")
                            try:
                                img_data = generate_nb_image(global_api_key, p['prompt'])
                                if img_data:
                                    generated[p['id']] = img_data
                            except Exception as e:
                                st.warning(f"فشل توليد {p['id']}: {str(e)}")
                            progress.progress((i+1)/len(prompts))
                        status.text(f"تم توليد {len(generated)}/{len(prompts)} صورة!")
                        if generated:
                            st.session_state.generated_images = generated
                            st.success(f"\u2705 تم توليد {len(generated)} صورة بنجاح!")
                if 'generated_images' in st.session_state:
                    st.markdown("#### الصور المولدة:")
                    cols = st.columns(3)
                    for i, (pid, img_b64) in enumerate(st.session_state.generated_images.items()):
                        with cols[i % 3]:
                                                        st.image(img_b64, caption=pid, use_column_width=True)
                    html_with_imgs = st.session_state.final_page
                    import re as _re
                    poll_urls = _re.findall(r'https://image\.pollinations\.ai/prompt/[^"]+', html_with_imgs)
                    gen_list = list(st.session_state.generated_images.values())
                    for idx, url in enumerate(poll_urls):
                        if idx < len(gen_list):
                            html_with_imgs = html_with_imgs.replace(url, gen_list[idx], 1)
                    st.session_state.final_page_ai = html_with_imgs
                    st.success("تم إدراج الصور في كود HTML بنجاح!")
                    st.download_button("تحميل HTML مع الصور", html_with_imgs, "landing_page_with_ai_images.html", "text/html")
        with tab3:
            if 'parsed_json' in st.session_state:
                json_str = json.dumps(st.session_state.parsed_json, ensure_ascii=False, indent=2)
                st.download_button(
                    label="\U0001f4e5 \u062a\u062d\u0645\u064a\u0644 \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0635\u0641\u062d\u0629 (JSON)",
                    data=json_str,
                    file_name="landing_page_data.json",
                    mime="application/json"
                )
                st.json(st.session_state.parsed_json)
            with tab4:
                youcan_html = get_youcan_html(st.session_state.final_page)
                st.info("انسخ هذا الكود والصقه في YouCan")
                st.code(youcan_html, language="html")
                st.download_button(label="تحميل YouCan HTML", data=youcan_html, file_name="youcan.html", mime="text/html")
        with tab5:
                if 'parsed_json' in st.session_state:
                    prompts = extract_image_prompts(st.session_state.parsed_json)
                    st.markdown("### 🎨 برومبتات الصور المطلوبة")
                    st.info("استخدم هذه البرومبتات لتوليد الصور بأداتك الخاصة")
                    for p in prompts:
                        with st.expander(f"{p['id']} - {p['section']}"):
                            st.code(p['prompt'], language='text')
                            st.caption(f"Type: {p['type']} | Keyword: {p['keyword']}")
                prompt_df = pd.DataFrame(prompts)
                csv = prompt_df.to_csv(index=False)
                st.download_button('Download Prompts CSV', csv, 'image_prompts.csv', 'text/csv')
            else:
                st.warning("قم بتوليد صفحة هبوط أولاً")                
    st.markdown("### \U0001f50d \u0627\u0644\u0628\u062d\u062b \u0627\u0644\u0645\u0639\u0645\u0642 \u0641\u064a \u0627\u0644\u0633\u0648\u0642")
    if st.button("\U0001f9e0 \u0627\u0633\u062a\u062e\u0631\u0627\u062c \u0648\u062b\u0627\u0626\u0642 \u0627\u0644\u0628\u064a\u0639"):
        if not global_api_key or not global_product_name:
            st.error("\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0627\u0644\u0645\u0641\u062a\u0627\u062d \u0648\u0627\u0633\u0645 \u0627\u0644\u0645\u0646\u062a\u062c.")
        else:
            with st.spinner("\U0001f575\ufe0f\u200d\u2642\ufe0f \u062c\u0627\u0631\u064a \u0627\u0644\u0628\u062d\u062b..."):
                try:
                    result = generate_deep_research(global_api_key, global_product_name, global_category)
                    st.session_state.research_output = result
                    st.success("\u2705 \u0627\u0643\u062a\u0645\u0644 \u0627\u0644\u0628\u062d\u062b!")
                except Exception as e:
                    st.error(f"\U0001f6d1 {str(e)}")
    if 'research_output' in st.session_state:
        st.markdown(st.session_state.research_output)

elif app_mode == "\U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644 \u0627\u0644\u0645\u0627\u0644\u064a (Matrix)":
    st.markdown("### \U0001f4b0 \u062d\u0627\u0633\u0628\u0629 \u0646\u0642\u0637\u0629 \u0627\u0644\u062a\u0639\u0627\u062f\u0644")
    COUNTRIES = {
        "\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629": {"currency": "SAR", "P": 199.0, "C": 85.0, "CPL": 25.0},
        "\u0627\u0644\u0625\u0645\u0627\u0631\u0627\u062a": {"currency": "AED", "P": 149.0, "C": 60.0, "CPL": 30.0},
        "\u0627\u0644\u0643\u0648\u064a\u062a": {"currency": "KWD", "P": 19.0, "C": 8.0, "CPL": 2.5},
        "\u0627\u0644\u0645\u063a\u0631\u0628": {"currency": "MAD", "P": 299.0, "C": 120.0, "CPL": 40.0},
        "\u0645\u0635\u0631": {"currency": "EGP", "P": 500.0, "C": 200.0, "CPL": 50.0},
        "\u0623\u062e\u0631\u0649": {"currency": "USD", "P": 50.0, "C": 20.0, "CPL": 5.0},
    }
    sel = st.selectbox("\U0001f30d \u0627\u0644\u062f\u0648\u0644\u0629:", list(COUNTRIES.keys()))
    d = COUNTRIES[sel]
    c1, c2, c3 = st.columns(3)
    P = c1.number_input(f"\u0633\u0639\u0631 \u0627\u0644\u0628\u064a\u0639 [{d['currency']}]", value=d["P"])
    C = c2.number_input(f"\u0627\u0644\u062a\u0643\u0644\u0641\u0629 [{d['currency']}]", value=d["C"])
    CPL = c3.number_input(f"CPL [{d['currency']}]", value=d["CPL"])
    c4, c5 = st.columns(2)
    CR = c4.slider("CR %", 10, 100, 60) / 100
    DR = c5.slider("DR %", 10, 100, 55) / 100
    margin = P - C
    max_cpl = margin * CR * DR
    profit = max_cpl - CPL
    m1, m2, m3 = st.columns(3)
    m1.metric("\u0647\u0627\u0645\u0634 \u0627\u0644\u0631\u0628\u062d", f"{margin:.2f} {d['currency']}")
    m2.metric("\u0623\u0642\u0635\u0649 CPL", f"{max_cpl:.2f} {d['currency']}")
    if profit >= 0:
        m3.metric("\u0627\u0644\u062d\u0627\u0644\u0629", "\u2705 \u0631\u0627\u0628\u062d", f"+{profit:.2f}")
    else:
        m3.metric("\u0627\u0644\u062d\u0627\u0644\u0629", "\U0001f6a8 \u062e\u0627\u0633\u0631", f"{profit:.2f}")
