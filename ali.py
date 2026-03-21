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
    hero_img = get_ai_image(data.get('image_hero_search', 'product'), 900, 1100, 'product')
    hero_lifestyle = get_ai_image(data.get('image_hero_lifestyle_search', 'person using product'), 800, 600, 'lifestyle')
    hero_closeup = get_ai_image(data.get('image_hero_closeup_search', 'product detail'), 600, 600, 'product')
    prob_img = get_ai_image(data.get('image_problem_search', 'worried person'), 700, 500, 'problem')
    prob_img2 = get_ai_image(data.get('image_problem_2_search', 'skin problem'), 600, 400, 'problem')
    sol_img = get_ai_image(data.get('image_solution_search', 'happy person'), 800, 600, 'solution')
    sol_img2 = get_ai_image(data.get('image_solution_2_search', 'product result'), 600, 600, 'lifestyle')
    before_img = get_ai_image(data.get('image_before_search', 'before treatment'), 500, 600, 'before_after')
    after_img = get_ai_image(data.get('image_after_search', 'after treatment'), 500, 600, 'before_after')
    dims = data.get('dimensions', {})
    dim_img = get_ai_image(dims.get('image_search', 'product dimensions'), 600, 600, 'dimensions')
    countdown_hours = data.get('countdown_hours', 24)
    badges_html = ""
    for badge in data.get('trust_badges', []):
        badges_html += f' \u2705 {badge}  '
    problems_html = ""
    for pt in data.get('problem_points', []):
        problems_html += f'<li style="padding:8px 0;font-size:1.05rem;">\u274c {pt}</li>\n'
    features_html = ""
    for feat in data.get('features', [])[:4]:
        feat_img = get_ai_image(feat.get('image_search', 'feature'), 400, 400, 'feature')
        features_html += f'''<div style="background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
            <img src="{feat_img}" style="width:100%;height:200px;object-fit:cover;">
            <div style="padding:20px;text-align:center;"><h4 style="color:{p};margin-bottom:8px;">\u2728 {feat.get('title','')}</h4>
            <p style="color:#64748b;font-size:0.95rem;">{feat.get('desc','')}</p></div></div>'''
    ingredients_html = ""
    for ing in data.get('ingredients', [])[:3]:
        ing_img = get_ai_image(ing.get('image_search', 'natural ingredient'), 300, 300, 'ingredient')
        ingredients_html += f'''<div style="text-align:center;">
            <img src="{ing_img}" style="width:120px;height:120px;border-radius:50%;object-fit:cover;margin:0 auto 15px;display:block;box-shadow:0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color:{p};margin-bottom:5px;">{ing.get('name','')}</h4>
            <p style="color:#64748b;font-size:0.9rem;">{ing.get('benefit','')}</p></div>'''
    steps_html = ""
    step_images = data.get('how_to_use_images', [])
    for i, step in enumerate(data.get('how_to_use', [])[:3], 1):
        step_kw = step_images[i-1] if i-1 < len(step_images) else f'step {i} tutorial'
        step_img = get_ai_image(step_kw, 500, 400, 'gif_step')
        direction = 'row' if i % 2 != 0 else 'row-reverse'
        steps_html += f'''<div style="display:flex;flex-direction:{direction};align-items:center;gap:25px;flex-wrap:wrap;margin-bottom:30px;background:white;border-radius:16px;padding:20px;box-shadow:0 4px 15px rgba(0,0,0,0.06);">
            <img src="{step_img}" style="flex:1;min-width:220px;max-width:350px;border-radius:12px;">
            <div style="flex:1;min-width:220px;"><div style="width:50px;height:50px;background:linear-gradient(135deg,{g1},{g2});border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:900;font-size:1.3rem;margin-bottom:12px;">{i}</div>
            <p style="font-size:1.1rem;color:#334155;line-height:1.7;">{step}</p></div></div>'''
    stats_html = ""
    for stat in data.get('stats', [])[:3]:
        stats_html += f'<div style="text-align:center;"><div style="font-size:2.2rem;font-weight:900;color:white;">{stat.get("number","")}</div><div style="color:rgba(255,255,255,0.8);font-size:0.95rem;margin-top:5px;">{stat.get("label","")}</div></div>'
    reviews_html = ""
    for rev in data.get('reviews', [])[:3]:
        stars = '\u2b50' * int(rev.get('rating', 5))
        rev_img = get_ai_image(rev.get('image_search', 'person portrait'), 150, 150, 'review')
        reviews_html += f'''<div style="background:white;border-radius:16px;padding:25px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;"><img src="{rev_img}" style="width:55px;height:55px;border-radius:50%;object-fit:cover;">
            <div><strong>{rev.get('name','')}</strong><br><span style="color:{a};">{stars}</span></div></div>
            <p style="color:#475569;font-style:italic;line-height:1.6;">\"{rev.get('comment','')}</p>
            <p style="color:{p};font-size:0.85rem;margin-top:8px;">\u2705 \u0645\u0634\u062a\u0631\u064a \u0645\u0648\u062b\u0642</p></div>'''
    faq_html = ""
    for faq in data.get('faq', [])[:4]:
        faq_html += f'''<details style="background:white;border-radius:12px;padding:18px 22px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.05);cursor:pointer;">
            <summary style="font-weight:700;color:{p};font-size:1.05rem;">{faq.get('q','')}</summary>
            <p style="color:#64748b;margin-top:10px;line-height:1.7;">{faq.get('a','')}</p></details>'''
    pricing = data.get('pricing', {})
    cta = data.get('call_to_action', '\u0627\u0637\u0644\u0628 \u0627\u0644\u0622\u0646')
    html = f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Cairo",sans-serif; background:{s}; color:#1e293b; direction:rtl; scroll-behavior:smooth; }}
img {{ max-width:100%; height:auto; display:block; }}
.container {{ max-width:860px; margin:0 auto; padding:0 20px; }}
.btn {{ display:block; background:linear-gradient(135deg,{a},{a}cc); color:white; padding:18px 30px; border-radius:14px; font-weight:900; font-size:1.25rem; text-decoration:none; text-align:center; box-shadow:0 8px 25px {a}55; transition:all 0.3s; border:none; cursor:pointer; width:100%; max-width:420px; margin:0 auto; }}
.btn:hover {{ transform:translateY(-3px); box-shadow:0 14px 35px {a}77; }}
.section {{ padding:55px 20px; }}
.section-title {{ font-size:1.9rem; font-weight:900; color:{p}; text-align:center; margin-bottom:30px; line-height:1.3; }}
.badge-bar {{ text-align:center; padding:15px; }}
.img-text-row {{ display:flex; align-items:center; gap:30px; flex-wrap:wrap; margin-bottom:30px; }}
.img-text-row img {{ flex:1; min-width:260px; border-radius:18px; box-shadow:0 10px 30px rgba(0,0,0,0.12); }}
.img-text-row .text-side {{ flex:1; min-width:240px; }}
.grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
.countdown-bar {{ background:linear-gradient(135deg,#dc2626,#ef4444); color:white; padding:20px; text-align:center; position:sticky; top:0; z-index:1000; box-shadow:0 4px 15px rgba(220,38,38,0.4); }}
.countdown-bar .timer {{ display:flex; justify-content:center; gap:15px; margin-top:8px; }}
.countdown-bar .timer div {{ background:rgba(0,0,0,0.3); padding:10px 18px; border-radius:10px; min-width:65px; }}
.countdown-bar .timer div span {{ display:block; font-size:1.8rem; font-weight:900; }}
.countdown-bar .timer div small {{ font-size:0.75rem; opacity:0.9; }}
@media(max-width:600px) {{ .grid-2 {{ grid-template-columns:1fr; }} .img-text-row {{ flex-direction:column; }} }}
</style></head><body>'''
    html += f'''<div class="countdown-bar" id="countdown-section">
        <div style="font-weight:700;font-size:1.1rem;">\u23f0 \u0627\u0644\u0639\u0631\u0636 \u064a\u0646\u062a\u0647\u064a \u062e\u0644\u0627\u0644</div>
        <div class="timer"><div><span id="cd-hours">00</span><small>\u0633\u0627\u0639\u0629</small></div><div><span id="cd-mins">00</span><small>\u062f\u0642\u064a\u0642\u0629</small></div><div><span id="cd-secs">00</span><small>\u062b\u0627\u0646\u064a\u0629</small></div></div></div>'''
    html += f'''<section style="background:linear-gradient(160deg,{g1},{g2});padding:60px 20px 50px;">
        <div class="container" style="display:flex;align-items:center;gap:35px;flex-wrap:wrap;">
            <div style="flex:1;min-width:280px;"><div class="badge-bar" style="margin-bottom:20px;background:rgba(255,255,255,0.15);border-radius:12px;padding:12px;color:white;">{badges_html}</div>
                <h1 style="font-size:2.5rem;font-weight:900;color:white;line-height:1.3;margin-bottom:15px;">{data.get('hero_headline','')}</h1>
                <p style="color:rgba(255,255,255,0.85);font-size:1.15rem;line-height:1.7;margin-bottom:20px;">{data.get('hero_subheadline','')}</p>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:25px;"><span style="color:{a};font-size:1.3rem;">\u2665</span><span style="color:white;font-weight:700;">{data.get('social_proof_number','')}</span><span style="color:rgba(255,255,255,0.8);">{data.get('social_proof_text','')}</span></div>
                <a href="#order" class="btn">{cta} \u2794</a></div>
            <div style="flex:1;min-width:280px;"><img src="{hero_img}" style="border-radius:20px;box-shadow:0 20px 50px rgba(0,0,0,0.3);">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;"><img src="{hero_lifestyle}" style="border-radius:12px;"><img src="{hero_closeup}" style="border-radius:12px;"></div></div></div></section>'''
    html += f'''<section style="background:linear-gradient(135deg,{p},{g2});padding:35px 20px;"><div class="container" style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:20px;">{stats_html}</div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container">
        <h2 class="section-title">\u26a0\ufe0f {data.get('problem_title','')}</h2>
        <div class="img-text-row"><img src="{prob_img}"><div class="text-side">
            <p style="color:#64748b;font-size:1.05rem;line-height:1.8;margin-bottom:20px;">{data.get('problem_description','')}</p>
            <ul style="list-style:none;">{problems_html}</ul></div></div>
        <img src="{prob_img2}" style="max-width:500px;margin:20px auto;border-radius:16px;">
    </div></section>'''
    html += f'''<section class="section" style="background:{s};"><div class="container">
        <h2 class="section-title">\u2728 {data.get('solution_title','')}</h2>
        <div class="img-text-row" style="flex-direction:row-reverse;"><img src="{sol_img}"><div class="text-side">
            <p style="color:#64748b;font-size:1.05rem;line-height:1.8;">{data.get('solution_description','')}</p></div></div>
        <img src="{sol_img2}" style="max-width:500px;margin:20px auto;border-radius:16px;">
        <h3 style="text-align:center;color:{p};margin:30px 0 20px;">\u2728 \u062a\u062d\u0648\u0644 \u0645\u0630\u0647\u0644!</h3>
        <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;">
            <div style="text-align:center;"><img src="{before_img}" style="max-width:280px;border-radius:16px;"><p style="margin-top:8px;font-weight:700;color:#ef4444;">\u0642\u0628\u0644</p></div>
            <div style="font-size:2.5rem;color:{a};">\u27a1</div>
            <div style="text-align:center;"><img src="{after_img}" style="max-width:280px;border-radius:16px;"><p style="margin-top:8px;font-weight:700;color:#22c55e;">\u0628\u0639\u062f</p></div></div>
    </div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container">
        <h2 class="section-title">\u0644\u0645\u0627\u0630\u0627 \u0647\u0630\u0627 \u0627\u0644\u0645\u0646\u062a\u062c \u0645\u062e\u062a\u0644\u0641\u061f</h2>
        <div class="grid-2">{features_html}</div></div></section>'''
    html += f'''<section class="section" style="background:{s};"><div class="container">
        <h2 class="section-title">\u0627\u0644\u0633\u0631 \u0641\u064a \u0645\u0643\u0648\u0646\u0627\u062a\u0646\u0627</h2>
        <div style="display:flex;justify-content:center;gap:40px;flex-wrap:wrap;">{ingredients_html}</div></div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container">
        <h2 class="section-title">\U0001f3ac \u0643\u064a\u0641 \u062a\u0633\u062a\u062e\u062f\u0645\u0647\u061f</h2>
        <p style="text-align:center;color:#64748b;margin-bottom:30px;">\u062a\u0639\u0644\u064a\u0645\u0627\u062a \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u062e\u0637\u0648\u0629 \u0628\u062e\u0637\u0648\u0629</p>
        {steps_html}</div></section>'''
    html += f'''<section class="section" style="background:{s};"><div class="container">
        <h2 class="section-title">\U0001f4cf \u0623\u0628\u0639\u0627\u062f \u0648\u062d\u062c\u0645 \u0627\u0644\u0645\u0646\u062a\u062c</h2>
        <div style="display:flex;align-items:center;gap:30px;flex-wrap:wrap;justify-content:center;">
            <img src="{dim_img}" style="max-width:350px;border-radius:16px;">
            <div style="min-width:250px;"><h4 style="color:{p};margin-bottom:15px;">\u0627\u0644\u0645\u0648\u0627\u0635\u0641\u0627\u062a \u0627\u0644\u062a\u0642\u0646\u064a\u0629</h4>
                <table style="width:100%;border-collapse:collapse;"><tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:12px;font-weight:700;color:{p};">\u0627\u0644\u0627\u0631\u062a\u0641\u0627\u0639</td><td style="padding:12px;">{dims.get('height','')}</td></tr>
                <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:12px;font-weight:700;color:{p};">\u0627\u0644\u0639\u0631\u0636</td><td style="padding:12px;">{dims.get('width','')}</td></tr>
                <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:12px;font-weight:700;color:{p};">\u0627\u0644\u0648\u0632\u0646</td><td style="padding:12px;">{dims.get('weight','')}</td></tr>
                <tr><td style="padding:12px;font-weight:700;color:{p};">\u0627\u0644\u062d\u062c\u0645</td><td style="padding:12px;">{dims.get('volume','')}</td></tr></table></div></div></div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container">
        <h2 class="section-title">\u2b50 \u0622\u0631\u0627\u0621 \u0627\u0644\u0639\u0645\u0644\u0627\u0621</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;">{reviews_html}</div></div></section>'''
    html += f'''<section id="order" class="section" style="background:linear-gradient(135deg,{s},{s});border-top:4px solid {a};"><div class="container" style="text-align:center;">
        <h2 class="section-title">\U0001f525 \u0627\u062d\u0635\u0644 \u0639\u0644\u064a\u0647 \u0627\u0644\u0622\u0646!</h2>
        <div style="background:white;border-radius:20px;padding:35px;max-width:450px;margin:0 auto;box-shadow:0 10px 30px rgba(0,0,0,0.1);">
            <p style="text-decoration:line-through;color:#94a3b8;font-size:1.2rem;">{pricing.get('original','')} {pricing.get('currency','')}</p>
            <p style="font-size:2.8rem;font-weight:900;color:{p};">{pricing.get('discounted','')}<span style="font-size:1rem;color:#64748b;"> {pricing.get('currency','')}</span></p>
            <span style="background:#dc2626;color:white;padding:5px 15px;border-radius:20px;font-weight:700;font-size:0.9rem;">\u062e\u0635\u0645 {pricing.get('discount_percent','')}</span>
            <div style="background:linear-gradient(135deg,#dc2626,#ef4444);color:white;border-radius:12px;padding:15px;margin:20px 0;">
                <p style="font-weight:700;margin-bottom:8px;">\u23f0 {data.get('urgency_text','')}</p>
                <div style="display:flex;justify-content:center;gap:10px;"><div style="background:rgba(0,0,0,0.3);padding:8px 14px;border-radius:8px;"><span id="cd2-h" style="font-size:1.4rem;font-weight:900;">00</span><br><small>\u0633\u0627\u0639\u0629</small></div><div style="background:rgba(0,0,0,0.3);padding:8px 14px;border-radius:8px;"><span id="cd2-m" style="font-size:1.4rem;font-weight:900;">00</span><br><small>\u062f\u0642\u064a\u0642\u0629</small></div><div style="background:rgba(0,0,0,0.3);padding:8px 14px;border-radius:8px;"><span id="cd2-s" style="font-size:1.4rem;font-weight:900;">00</span><br><small>\u062b\u0627\u0646\u064a\u0629</small></div></div></div>
            <a href="#" class="btn" style="margin-top:15px;">{cta} \u2794</a></div></div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container" style="max-width:700px;margin:0 auto;">
        <h2 class="section-title">\u2753 \u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0634\u0627\u0626\u0639\u0629</h2>
        {faq_html}</div></section>'''
    html += f'''<section class="section" style="background:white;"><div class="container" style="text-align:center;">
        <div style="max-width:550px;margin:0 auto;padding:35px;background:linear-gradient(135deg,{s},white);border-radius:20px;border:2px solid {p}20;">
            <div style="font-size:4rem;margin-bottom:15px;">\U0001f6e1</div>
            <h3 style="color:{p};font-size:1.6rem;font-weight:900;margin-bottom:10px;">{data.get('guarantee_title','')}</h3>
            <p style="color:#64748b;font-size:1rem;line-height:1.7;">{data.get('guarantee_text','')}</p></div></div></section>'''
    html += f'''<section style="background:linear-gradient(160deg,{g1},{g2});padding:50px 20px;"><div class="container" style="text-align:center;">
        <h2 style="color:white;font-size:1.9rem;font-weight:900;margin-bottom:20px;">\u2764\ufe0f \u0644\u0627 \u062a\u0641\u0648\u062a \u0647\u0630\u0627 \u0627\u0644\u0639\u0631\u0636!</h2>
        <a href="#order" class="btn" style="font-size:1.3rem;padding:20px 40px;">{cta} \u2794</a>
        <p style="color:rgba(255,255,255,0.75);margin-top:20px;font-size:0.9rem;">{data.get('footer_text','')}</p></div></section>'''
    html += f'''<script>
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
            if(document.getElementById('cd2-h')){{document.getElementById('cd2-h').textContent=pad(h);document.getElementById('cd2-m').textContent=pad(m);document.getElementById('cd2-s').textContent=pad(s);}}
            if(left>0)setTimeout(tick,1000);
        }}
        tick();
    }})();
    </script></body></html>'''
    html = html.replace('<img ', '<img loading=lazy ')

    return html

def get_youcan_html(html):
    """Strip script tags for YouCan compatibility"""
    import re
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    # Remove data-src and restore src for YouCan
    clean = clean.replace(' data-src="', ' src="')
    # Remove countdown IDs that need JS
    clean = clean.replace('id="cd-hours"', '').replace('id="cd-mins"', '').replace('id="cd-secs"', '')
    clean = clean.replace('id="cd2-h"', '').replace('id="cd2-m"', '').replace('id="cd2-s"', '')
    return clean

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
        tab1, tab2, tab3, tab4 = st.tabs(["\U0001f4f1 \u0627\u0644\u0645\u0639\u0627\u064a\u0646\u0629 \u0627\u0644\u0628\u0635\u0631\u064a\u0629", "\U0001f4bb \u0643\u0648\u062f HTML", "\U0001f4e5 \u062a\u062d\u0645\u064a\u0644 JSON", "\U0001f4e4 YouCan HTML"])
        with tab1:
            components.html(st.session_state.final_page, height=4000, scrolling=True)
        with tab2:
            st.code(st.session_state.final_page, language="html")
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
