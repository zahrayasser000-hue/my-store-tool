import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd
import random
import urllib.parse
import base64
import time
import uuid
import requests
import traceback
import sys

st.set_page_config(page_title="ALI Engine Pro", layout="wide", page_icon="🚀")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stSidebar"]{font-family:'Cairo',sans-serif!important;direction:rtl;text-align:right;background:#f8fafc;}
.main-header{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;padding:40px 20px;border-radius:20px;text-align:center;margin-bottom:35px;border-bottom:5px solid #3b82f6;}
.main-header h1{font-weight:900;font-size:3rem;background:linear-gradient(to right,#93c5fd,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.main-header p{color:#94a3b8;font-size:1.2rem;font-weight:600;}
.stButton>button{background:linear-gradient(135deg,#2563eb,#3b82f6)!important;color:#fff!important;font-weight:800!important;font-size:1.1rem!important;border:none!important;border-radius:12px!important;padding:15px 30px!important;width:100%;}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>ALI Growth Engine Pro 🚀</h1><p>منصة العمليات التسويقية | 15 قسم | +30 صورة AI</p></div>', unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_ai_image(keyword, width=800, height=600, style="product", context=""):
    safe = str(keyword).strip() or "product"
    pm = {
        "product":     f"{safe} product photo white background studio lighting professional 8k",
        "lifestyle":   f"lifestyle photography person using {safe} natural warm setting authentic 8k",
        "problem":     f"frustrated person problem {safe} worried expression dramatic lighting realistic 8k",
        "solution":    f"happy satisfied person using {safe} bright smile positive natural lighting 8k",
        "feature":     f"visual representation {context} {safe} circular composition white background commercial 8k",
        "ingredient":  f"close up macro {safe} natural organic ingredient studio white background 8k",
        "gif_step":    f"hands tutorial step using {safe} clean demonstration bright lighting instructional 8k",
        "review":      f"happy satisfied customer avatar illustration digital art warm colors neutral background soft lighting 8k",
        "doctor":      f"professional arab doctor white coat hospital confident smile realistic 8k",
        "family":      f"happy arab family group {safe} warm home lighting authentic 8k",
        "hero_person": f"confident arab person using {safe} cinematic lighting editorial photography 8k",
        "composite":   f"{safe} product dark dramatic background studio lighting commercial photography 8k",
        "before":      f"clear BEFORE state without {safe} problem visible high quality 8k",
        "after":       f"clear AFTER state {safe} problem solved dramatic improvement 8k",
        "dimensions":  f"{safe} product flat lay ruler measurement size reference clean white background 8k",
    }
    prompt = pm.get(style, f"{safe} high quality realistic commercial photo 8k") + " no text no letters no words no writing"
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true&seed={random.randint(1,99999)}"

AUTO_COLORS = {
    "skincare":  {"primary":"#be185d","secondary":"#fdf2f8","accent":"#f59e0b","gradient1":"#be185d","gradient2":"#ec4899","bg_light":"#fff5f8","text_dark":"#4a0e2b","card_bg":"#fff0f5","badge_bg":"#fce7f3"},
    "cosmetics": {"primary":"#0f766e","secondary":"#f0fdfa","accent":"#eab308","gradient1":"#0f766e","gradient2":"#14b8a6","bg_light":"#f0fdfa","text_dark":"#064e47","card_bg":"#ecfdf5","badge_bg":"#d1fae5"},
    "health":    {"primary":"#15803d","secondary":"#f0fdf4","accent":"#f97316","gradient1":"#15803d","gradient2":"#22c55e","bg_light":"#f0fdf4","text_dark":"#0a3d1c","card_bg":"#ecfdf5","badge_bg":"#dcfce7"},
    "gadgets":   {"primary":"#1e3a5f","secondary":"#f0f4f8","accent":"#ef4444","gradient1":"#1e3a5f","gradient2":"#3b82f6","bg_light":"#eff6ff","text_dark":"#0f1f33","card_bg":"#e8f0fe","badge_bg":"#dbeafe"},
    "fashion":   {"primary":"#7c2d12","secondary":"#fef3c7","accent":"#d97706","gradient1":"#7c2d12","gradient2":"#ea580c","bg_light":"#fffbeb","text_dark":"#451a0a","card_bg":"#fef3c7","badge_bg":"#fde68a"},
    "default":   {"primary":"#1e40af","secondary":"#eff6ff","accent":"#f59e0b","gradient1":"#1e40af","gradient2":"#3b82f6","bg_light":"#eff6ff","text_dark":"#0f1f55","card_bg":"#e8f0fe","badge_bg":"#dbeafe"},
}

def detect_colors(name, cat):
    t = (name+" "+cat).lower()
    if any(w in t for w in ["cream","كريم","collagen","كولاجين","serum","سيروم"]): return AUTO_COLORS["skincare"]
    if any(w in t for w in ["skin","بشرة","beauty","جمال","cosmetic","تجميل"]):    return AUTO_COLORS["cosmetics"]
    if any(w in t for w in ["health","صحة","vitamin","فيتامين","supplement"]):     return AUTO_COLORS["health"]
    if any(w in t for w in ["gadget","جهاز","device","smart","glasses","نظارة"]):  return AUTO_COLORS["gadgets"]
    if any(w in t for w in ["fashion","موضة","clothes","ملابس"]):                  return AUTO_COLORS["fashion"]
    return AUTO_COLORS["default"]

def get_model(api_key):
    st.session_state.model_name = "gemini-2.5-flash"
    return "gemini-2.5-flash"

# ─── JSON GENERATION ──────────────────────────────────────────────────────────

def generate_lp_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel(get_model(api_key))
    prompt = f"""
أنت خبير Copywriter. المنتج: "{product}". الفئة: "{category}".
النصوص عربية فصحى. حقول _search هي كلمات إنجليزية دقيقة لتوليد صور AI (6-10 كلمات). أضف دائماً 'no text no letters no words' في نهاية كل حقل _search.
رد بـ JSON صالح فقط:
{{
  "hero_headline": "عنوان رئيسي قوي",
  "hero_subheadline": "عنوان فرعي داعم",
  "image_hero_person_search": "confident arab person holding exact product cinematic editorial photography 8k no text no letters",
  "image_hero_product_search": "exact product isolated dark dramatic studio lighting 8k",
  "image_hero_lifestyle_search": "lifestyle person using product natural warm setting wide shot 8k",
  "trust_badges": ["شحن مجاني","الدفع عند الاستلام","ضمان 30 يوم","دعم 24/7"],
  "hero_benefits": [{{"icon":"\U0001f4aa","title":"\u0641\u0627\u0626\u062f\u0629 1 \u0645\u062e\u062a\u0635\u0631\u0629"}},{{"icon":"\u2728","title":"\u0641\u0627\u0626\u062f\u0629 2 \u0645\u062e\u062a\u0635\u0631\u0629"}},{{"icon":"\u2705","title":"\u0641\u0627\u0626\u062f\u0629 3 \u0645\u062e\u062a\u0635\u0631\u0629"}},{{"icon":"\U0001f31f","title":"\u0641\u0627\u0626\u062f\u0629 4 \u0645\u062e\u062a\u0635\u0631\u0629"}}], "social_proof_number": "+12,000",
  "social_proof_text": "عميل سعيد",
  "problem_title": "عنوان المشكلة",
  "problem_description": "فقرة تصف الإحباط بعمق",
  "problem_points": ["مشكلة تفصيلية 1","مشكلة تفصيلية 2","مشكلة تفصيلية 3"],
  "image_problem_1_search": "frustrated person exact problem worried realistic dramatic lighting 8k",
  "image_problem_2_search": "visual second aspect of the problem close up realistic 8k",
  "solution_title": "عنوان الحل",
  "solution_description": "فقرة الحل التفصيلية",
  "image_solution_1_search": "happy person after solving problem with product natural lighting 8k",
  "image_solution_2_search": "product in use showing solution benefit close up 8k",
  "image_before_search": "clear BEFORE state without product problem visible dramatic 8k",
  "image_after_search": "clear AFTER state with product problem solved improvement 8k",
  "doctors": [
    {{"name": "د. اسم طبيب 1","title": "استشاري تخصص مناسب","quote": "اقتباس تأييد طبي قوي 2-3 جمل","image_search": "professional arab doctor white coat hospital confident smile pointing 8k"}},
    {{"name": "د. اسم طبيب 2","title": "خبير تخصص مناسب","quote": "اقتباس تأييد خبير موثوق 2-3 جمل","image_search": "professional arab medical expert white coat laboratory confident 8k"}}
  ],
  "family_headline": "يثق بنا الآلاف في المنطقة العربية",
  "image_family_1_search": "happy arab family group using product together warm home lighting 8k",
  "image_family_2_search": "group satisfied arab customers smiling holding product diverse ages 8k",
  "features": [
    {{"title": "ميزة 1","desc": "فائدة تفصيلية","image_search": "exact visual feature 1 circular white background commercial 8k"}},
    {{"title": "ميزة 2","desc": "فائدة تفصيلية","image_search": "exact visual feature 2 circular white background commercial 8k"}},
    {{"title": "ميزة 3","desc": "فائدة تفصيلية","image_search": "exact visual feature 3 circular white background commercial 8k"}},
    {{"title": "ميزة 4","desc": "فائدة تفصيلية","image_search": "exact visual feature 4 circular white background commercial 8k"}}
  ],
  "ingredients": [
    {{"name": "مكون 1","benefit": "فائدته التفصيلية","image_search": "exact ingredient 1 raw natural macro close up white background 8k"}},
    {{"name": "مكون 2","benefit": "فائدته التفصيلية","image_search": "exact ingredient 2 raw natural macro close up white background 8k"}},
    {{"name": "مكون 3","benefit": "فائدته التفصيلية","image_search": "exact ingredient 3 raw natural macro close up white background 8k"}},
    {{"name": "مكون 4","benefit": "فائدته التفصيلية","image_search": "exact ingredient 4 raw natural macro close up white background 8k"}}
  ],
  "how_to_use": ["خطوة 1 تفصيلية","خطوة 2 تفصيلية","خطوة 3 تفصيلية","خطوة 4 تفصيلية"],
  "how_to_use_images": [
    "hands demonstrating step 1 action with product close up bright studio 8k",
    "hands demonstrating step 2 action with product close up bright studio 8k",
    "hands demonstrating step 3 action with product close up bright studio 8k",
    "hands demonstrating step 4 action with product close up bright studio 8k"
  ],
  "dimensions": {{"height": "15 cm","width": "8 cm","weight": "200g","volume": "50ml","note": "ملاحظة المقاسات"}
