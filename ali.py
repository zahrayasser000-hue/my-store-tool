import re
import json
import pandas as pd
import random
import urllib.parse
import base64
import time
import requests
import traceback
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

st.set_page_config(page_title="ALI Engine Pro", layout="wide", page_icon="🚀")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
        background: #f8fafc;
    }
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #fff;
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 35px;
        border-bottom: 5px solid #3b82f6;
    }
    .main-header h1 {
        font-weight: 900;
        font-size: 3rem;
        background: linear-gradient(to right, #93c5fd, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-header p { color: #94a3b8; font-size: 1.2rem; font-weight: 600; }
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: #fff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">'
    "<h1>ALI Growth Engine Pro 🚀</h1>"
    "<p>منصة العمليات التسويقية | 15 قسم | +30 صورة AI</p>"
    "</div>",
    unsafe_allow_html=True,
)


# ─── HELPERS ──────────────────────────────────────────────────────────────────


def get_model(api_key):
    return "gemini-1.5-flash"


def get_ai_image(keyword, width=800, height=600, style="product", context=""):
    safe = str(keyword).strip() or "product"
    pm = {
        "product": "{} product photo white background studio lighting professional 8k".format(safe),
        "lifestyle": "lifestyle photography person using {} natural warm setting authentic 8k".format(safe),
        "problem": "frustrated person problem {} worried expression dramatic lighting realistic 8k".format(safe),
        "solution": "happy satisfied person using {} bright smile positive natural lighting 8k".format(safe),
        "feature": "visual representation {} {} circular composition white background commercial 8k".format(context, safe),
        "ingredient": "close up macro {} natural organic ingredient studio white background 8k".format(safe),
        "gif_step": "hands tutorial step using {} clean demonstration bright lighting instructional 8k".format(safe),
        "review": "happy satisfied customer avatar illustration digital art warm colors neutral background soft lighting 8k",
        "doctor": "professional arab doctor white coat hospital confident smile realistic 8k",
        "family": "happy arab family group {} warm home lighting authentic 8k".format(safe),
        "hero_person": "confident arab person using {} cinematic lighting editorial photography 8k".format(safe),
        "composite": "{} product dark dramatic background studio lighting commercial photography 8k".format(safe),
        "before": "clear BEFORE state without {} problem visible high quality 8k".format(safe),
        "after": "clear AFTER state {} problem solved dramatic improvement 8k".format(safe),
        "dimensions": "{} product flat lay ruler measurement size reference clean white background 8k".format(safe),
    }
    prompt = pm.get(style, "{} high quality realistic commercial photo 8k".format(safe))
    prompt += " no text no letters no words no writing"
    encoded = urllib.parse.quote(prompt)
    return "https://image.pollinations.ai/prompt/{}?width={}&height={}&nologo=true&seed={}".format(
        encoded, width, height, random.randint(1, 99999)
    )


AUTO_COLORS = {
    "skincare": {
        "primary": "#be185d",
        "secondary": "#fdf2f8",
        "accent": "#f59e0b",
        "gradient1": "#be185d",
        "gradient2": "#ec4899",
        "bg_light": "#fff5f8",
        "text_dark": "#4a0e2b",
        "card_bg": "#fff0f5",
        "badge_bg": "#fce7f3",
    },
    "cosmetics": {
        "primary": "#0f766e",
        "secondary": "#f0fdfa",
        "accent": "#eab308",
        "gradient1": "#0f766e",
        "gradient2": "#14b8a6",
        "bg_light": "#f0fdfa",
        "text_dark": "#064e47",
        "card_bg": "#ecfdf5",
        "badge_bg": "#d1fae5",
    },
    "health": {
        "primary": "#15803d",
        "secondary": "#f0fdf4",
        "accent": "#f97316",
        "gradient1": "#15803d",
        "gradient2": "#22c55e",
        "bg_light": "#f0fdf4",
        "text_dark": "#0a3d1c",
        "card_bg": "#ecfdf5",
        "badge_bg": "#dcfce7",
    },
    "gadgets": {
        "primary": "#1e3a5f",
        "secondary": "#f0f4f8",
        "accent": "#ef4444",
        "gradient1": "#1e3a5f",
        "gradient2": "#3b82f6",
        "bg_light": "#eff6ff",
        "text_dark": "#0f1f33",
        "card_bg": "#e8f0fe",
        "badge_bg": "#dbeafe",
    },
    "fashion": {
        "primary": "#7c2d12",
        "secondary": "#fef3c7",
        "accent": "#d97706",
        "gradient1": "#7c2d12",
        "gradient2": "#ea580c",
        "bg_light": "#fffbeb",
        "text_dark": "#451a0a",
        "card_bg": "#fef3c7",
        "badge_bg": "#fde68a",
    },
    "default": {
        "primary": "#1e40af",
        "secondary": "#eff6ff",
        "accent": "#f59e0b",
        "gradient1": "#1e40af",
        "gradient2": "#3b82f6",
        "bg_light": "#eff6ff",
        "text_dark": "#0f1f55",
        "card_bg": "#e8f0fe",
        "badge_bg": "#dbeafe",
    },
}


def detect_colors(name, cat):
    name_l = (name or "").lower()
    cat_l = (cat or "").lower()
    for key in AUTO_COLORS:
        if key in name_l or key in cat_l:
            return AUTO_COLORS[key]
    return AUTO_COLORS["default"]


# ─── AI GENERATION ────────────────────────────────────────────────────────────


def generate_lp_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel(get_model(api_key))
    prompt = (
        'أنت خبير تسويق رقمي ومتخصص في إنشاء صفحات هبوط عربية عالية التحويل.\n'
        'المنتج: "{}"\n'
        'الفئة: "{}"\n\n'
        'أنشئ JSON كامل ومفصل لصفحة هبوط احترافية. أخرج JSON فقط بدون أي نص إضافي.\n'
        'الهيكل المطلوب:\n'
        '{{\n'
        '  "hero_headline": "عنوان رئيسي قوي ومقنع",\n'
        '  "hero_subheadline": "عنوان فرعي تفصيلي",\n'
        '  "hero_benefits": [{{"title": "ميزة 1"}}, {{"title": "ميزة 2"}}, {{"title": "ميزة 3"}}],\n'
        '  "social_proof_number": "+5000",\n'
        '  "social_proof_text": "عميل سعيد حول العالم",\n'
        '  "trust_badges": ["شحن مجاني", "ضمان 30 يوم", "دفع آمن", "جودة مضمونة"],\n'
        '  "problem_title": "عنوان المشكلة",\n'
        '  "problem_description": "وصف تفصيلي للمشكلة",\n'
        '  "problem_points": ["نقطة مشكلة 1", "نقطة مشكلة 2", "نقطة مشكلة 3"],\n'
        '  "solution_title": "عنوان الحل",\n'
        '  "solution_description": "وصف تفصيلي للحل",\n'
        '  "image_hero_person_search": "وصف صورة شخص البطل بالانجليزية",\n'
        '  "image_hero_product_search": "وصف صورة المنتج بالانجليزية",\n'
        '  "image_hero_lifestyle_search": "وصف صورة نمط الحياة بالانجليزية",\n'
        '  "image_problem_1_search": "وصف صورة المشكلة 1 بالانجليزية",\n'
        '  "image_problem_2_search": "وصف صورة المشكلة 2 بالانجليزية",\n'
        '  "image_solution_1_search": "وصف صورة الحل 1 بالانجليزية",\n'
        '  "image_solution_2_search": "وصف صورة الحل 2 بالانجليزية",\n'
        '  "image_before_search": "وصف صورة قبل بالانجليزية",\n'
        '  "image_after_search": "وصف صورة بعد بالانجليزية",\n'
        '  "image_family_1_search": "وصف صورة عائلة 1 بالانجليزية",\n'
        '  "image_family_2_search": "وصف صورة عائلة 2 بالانجليزية",\n'
        '  "family_headline": "عنوان قسم العائلة والثقة",\n'
        '  "doctors": [\n'
        '    {{"name": "د. اسم الطبيب", "title": "تخصصه", "quote": "اقتباس مقنع من الطبيب", "image_search": "professional arab doctor white coat"}},\n'
        '    {{"name": "د. اسم طبيب 2", "title": "تخصصه", "quote": "اقتباس مقنع", "image_search": "professional arab doctor hospital"}}\n'
        '  ],\n'
        '  "features": [\n'
        '    {{"title": "ميزة 1", "desc": "وصف الميزة", "image_search": "feature description english"}},\n'
        '    {{"title": "ميزة 2", "desc": "وصف الميزة", "image_search": "feature description english"}},\n'
        '    {{"title": "ميزة 3", "desc": "وصف الميزة", "image_search": "feature description english"}},\n'
        '    {{"title": "ميزة 4", "desc": "وصف الميزة", "image_search": "feature description english"}}\n'
        '  ],\n'
        '  "ingredients": [\n'
        '    {{"name": "مكون 1", "benefit": "فائدته", "image_search": "ingredient english"}},\n'
        '    {{"name": "مكون 2", "benefit": "فائدته", "image_search": "ingredient english"}},\n'
        '    {{"name": "مكون 3", "benefit": "فائدته", "image_search": "ingredient english"}},\n'
        '    {{"name": "مكون 4", "benefit": "فائدته", "image_search": "ingredient english"}}\n'
        '  ],\n'
        '  "how_to_use": ["الخطوة الاولى", "الخطوة الثانية", "الخطوة الثالثة", "الخطوة الرابعة"],\n'
        '  "how_to_use_images": [\n'
        '    "hands demonstrating step 1 action with product close up bright studio 8k",\n'
        '    "hands demonstrating step 2 action with product close up bright studio 8k",\n'
        '    "hands demonstrating step 3 action with product close up bright studio 8k",\n'
        '    "hands demonstrating step 4 action with product close up bright studio 8k"\n'
        '  ],\n'
        '  "dimensions": {{"height": "15 cm", "width": "8 cm", "weight": "200g", "volume": "50ml", "note": "ملاحظة المقاسات"}},\n'
        '  "image_dimensions_search": "product flat lay ruler measurement size reference clean white background 8k",\n'
        '  "image_dimensions_2_search": "product packaging box dimensions label close up clean background 8k",\n'
        '  "stats": [{{"number": "98%", "label": "نسبة الرضا"}}, {{"number": "+5000", "label": "عميل سعيد"}}, {{"number": "4.9/5", "label": "التقييم"}}],\n'
        '  "reviews": [\n'
        '    {{"name": "سارة م.", "rating": 5, "comment": "تعليق واقعي مقنع", "image_search": "close up portrait happy arab woman headshot neutral background soft lighting 8k"}},\n'
        '    {{"name": "احمد ع.", "rating": 5, "comment": "تعليق واقعي مقنع", "image_search": "close up portrait confident arab man headshot neutral background soft lighting 8k"}},\n'
        '    {{"name": "نورة ك.", "rating": 5, "comment": "تعليق واقعي مقنع", "image_search": "close up portrait smiling arab woman headshot neutral background soft lighting 8k"}}\n'
        '  ],\n'
        '  "pricing": {{"original": "399", "discounted": "199", "currency": "SAR", "discount_percent": "50%"}},\n'
        '  "urgency_text": "العرض ينتهي خلال 24 ساعة!",\n'
        '  "countdown_hours": 24,\n'
        '  "faq": [\n'
        '    {{"q": "متى سالاحظ النتائج؟", "a": "اجابة تفصيلية"}},\n'
        '    {{"q": "هل المنتج آمن؟", "a": "اجابة تفصيلية"}},\n'
        '    {{"q": "كيف أطلب؟", "a": "اجابة تفصيلية"}},\n'
        '    {{"q": "ما سياسة الارجاع؟", "a": "اجابة تفصيلية"}}\n'
        '  ],\n'
        '  "guarantee_title": "ضمان استرجاع الاموال 30 يوماً",\n'
        '  "guarantee_text": "نص الضمان التفصيلي",\n'
        '  "call_to_action": "اطلب الآن",\n'
        '  "footer_text": "جميع الحقوق محفوظة"\n'
        '}}'
    ).format(product, category)

    r = model.generate_content(prompt, request_options={"timeout": 60.0})
    tb = chr(96) * 3
    clean = re.sub(tb + "(?:json|JSON)?", "", r.text, flags=re.IGNORECASE).replace(tb, "").strip()
    m = re.search(r"\{.*\}", clean, re.DOTALL)
    return m.group(0) if m else clean


def generate_deep_research(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel(get_model(api_key))
    r = model.generate_content(
        'أنت Deep Research. المنتج: "{}". الفئة: "{}".\n'
        "أخرج تقريراً شاملاً بالعربية Markdown:\n"
        "1. Avatar Sheet\n2. بحث السوق والمنافسين\n3. Offer Brief\n"
        "4. المعتقدات الضرورية\n5. زوايا البيع PAS+FAB".format(product, category),
        request_options={"timeout": 60.0},
    )
    return r.text


# ─── IMAGE SLOTS ──────────────────────────────────────────────────────────────


def extract_image_slots(data):
    slots = []
    pn = data.get("_product_name", "")

    def add(key, section, keyword, itype, context=""):
        pm = {
            "product": "{} product photo white background studio 8k".format(keyword),
            "lifestyle": "lifestyle person using {} natural warm authentic 8k".format(keyword),
            "problem": "frustrated person problem {} worried dramatic realistic 8k".format(keyword),
            "solution": "happy person after using {} bright smile positive 8k".format(keyword),
            "feature": "visual {} {} circular white background commercial 8k".format(context, keyword),
            "ingredient": "macro {} natural organic studio white background 8k".format(keyword),
            "gif_step": "hands tutorial {} clean demonstration bright 8k".format(keyword),
            "review": "happy satisfied customer avatar illustration digital art warm colors circular frame 8k",
            "doctor": "professional doctor white coat hospital confident smile 8k",
            "family": "happy arab family group {} warm home authentic 8k".format(keyword),
            "hero_person": "confident arab person {} cinematic editorial 8k".format(keyword),
            "composite": "{} product dark dramatic studio commercial 8k".format(keyword),
            "before": "BEFORE state {} problem visible high quality 8k".format(keyword),
            "after": "AFTER state {} problem solved improvement 8k".format(keyword),
            "dimensions": "{} product flat lay ruler measurement white background 8k".format(keyword),
        }
        prompt = pm.get(itype, "{} commercial photo 8k".format(keyword))
        prompt += " no text no letters no words no writing"
        if pn:
            prompt = "Product: {}. {}".format(pn, prompt)
        slots.append(
            {
                "key": key,
                "section": section,
                "keyword": keyword,
                "prompt": prompt,
                "type": itype,
                "context": context,
            }
        )

    add("IMG_HERO_PERSON", "hero", data.get("image_hero_person_search", "arab person"), "hero_person")
    add("IMG_HERO_PRODUCT", "hero", data.get("image_hero_product_search", "product"), "composite")
    add("IMG_HERO_LIFESTYLE", "hero", data.get("image_hero_lifestyle_search", "lifestyle"), "lifestyle")
    add("IMG_PROB_1", "problem", data.get("image_problem_1_search", "problem person"), "problem")
    add("IMG_PROB_2", "problem", data.get("image_problem_2_search", "problem visual"), "problem")
    add("IMG_SOL_1", "solution", data.get("image_solution_1_search", "happy person"), "solution")
    add("IMG_SOL_2", "solution", data.get("image_solution_2_search", "product use"), "product")
    add("IMG_BEFORE", "before_after", data.get("image_before_search", "before"), "before")
    add("IMG_AFTER", "before_after", data.get("image_after_search", "after"), "after")

    for i, doc in enumerate(data.get("doctors", [])[:2], 1):
        add("IMG_DOC_{}".format(i), "doctors", doc.get("image_search", "doctor"), "doctor")

    add("IMG_FAM_1", "family", data.get("image_family_1_search", "family"), "family")
    add("IMG_FAM_2", "family", data.get("image_family_2_search", "customers"), "family")

    for i, feat in enumerate(data.get("features", [])[:4], 1):
        add(
            "IMG_FEAT_{}".format(i),
            "features",
            feat.get("image_search", "feature"),
            "feature",
            context="{} {}".format(feat.get("title", ""), feat.get("desc", "")),
        )

    for i, ing in enumerate(data.get("ingredients", [])[:4], 1):
        add("IMG_ING_{}".format(i), "ingredients", ing.get("image_search", "ingredient"), "ingredient")

    step_imgs = data.get("how_to_use_images", [])
    for i in range(min(4, len(step_imgs))):
        add("IMG_STEP_{}".format(i + 1), "steps", step_imgs[i], "gif_step")

    add("IMG_DIM_1", "dimensions", data.get("image_dimensions_search", "product dimensions"), "dimensions")
    add("IMG_DIM_2", "dimensions", data.get("image_dimensions_2_search", "product packaging"), "product")

    for i, rev in enumerate(data.get("reviews", [])[:3], 1):
        add("IMG_REV_{}".format(i), "reviews", rev.get("image_search", "person portrait"), "review")

    return slots


# ─── HTML BUILDER ─────────────────────────────────────────────────────────────


def build_lp_html(data, colors, image_map=None):
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]
    g1 = colors["gradient1"]
    g2 = colors["gradient2"]

    def img(key, kw, w, h, st_style, context=""):
        if image_map and key in image_map:
            return image_map[key]
        return get_ai_image(kw, w, h, st_style, context)

    hero_person = img("IMG_HERO_PERSON", data.get("image_hero_person_search", "person"), 600, 700, "hero_person")
    hero_product = img("IMG_HERO_PRODUCT", data.get("image_hero_product_search", "product"), 500, 500, "composite")
    hero_lifestyle = img("IMG_HERO_LIFESTYLE", data.get("image_hero_lifestyle_search", "lifestyle"), 800, 350, "lifestyle")
    prob1 = img("IMG_PROB_1", data.get("image_problem_1_search", "problem"), 500, 380, "problem")
    prob2 = img("IMG_PROB_2", data.get("image_problem_2_search", "problem2"), 500, 380, "problem")
    sol1 = img("IMG_SOL_1", data.get("image_solution_1_search", "solution"), 500, 380, "solution")
    sol2 = img("IMG_SOL_2", data.get("image_solution_2_search", "solution2"), 500, 380, "product")
    before_img = img("IMG_BEFORE", data.get("image_before_search", "before"), 450, 320, "before")
    after_img = img("IMG_AFTER", data.get("image_after_search", "after"), 450, 320, "after")
    fam1 = img("IMG_FAM_1", data.get("image_family_1_search", "family"), 500, 380, "family")
    fam2 = img("IMG_FAM_2", data.get("image_family_2_search", "customers"), 500, 380, "family")
    dim1 = img("IMG_DIM_1", data.get("image_dimensions_search", "dimensions"), 500, 400, "dimensions")
    dim2 = img("IMG_DIM_2", data.get("image_dimensions_2_search", "packaging"), 400, 300, "product")

    badges = data.get("trust_badges", [])
    pricing = data.get("pricing", {})
    cta = data.get("call_to_action", "اطلب الآن")
    cdh = data.get("countdown_hours", 24)
    dims = data.get("dimensions", {})

    tb_badges = "".join('<span class="tb-b">&#x2705; {}</span>'.format(b) for b in badges[:4])
    probs_html = "".join(
        '<div class="pain"><span>&#x274C;</span>{}</div>'.format(pt)
        for pt in data.get("problem_points", [])
    )
    stats_html = "".join(
        '<div class="stat-box"><div class="sn">{}</div><div class="sl">{}</div></div>'.format(
            st_item.get("number", ""), st_item.get("label", "")
        )
        for st_item in data.get("stats", [])[:3]
    )

    docs_html = ""
    for i, doc in enumerate(data.get("doctors", [])[:2], 1):
        di = img("IMG_DOC_{}".format(i), doc.get("image_search", "doctor"), 300, 380, "doctor")
        docs_html += (
            '<div class="doc-card">'
            '<img loading="lazy" src="{}" alt="{}">'.format(di, doc.get("name", ""))
            + '<div class="doc-info">'
            + '<div class="doc-name">{}</div>'.format(doc.get("name", ""))
            + '<div class="doc-title">{}</div>'.format(doc.get("title", ""))
            + '<div class="doc-quote"><span class="qm">&ldquo;</span>{}<span class="qm">&rdquo;</span></div>'.format(
                doc.get("quote", "")
            )
            + "</div></div>"
        )

    feats_html = ""
    for i, feat in enumerate(data.get("features", [])[:4], 1):
        fi = img(
            "IMG_FEAT_{}".format(i),
            feat.get("image_search", "feature"),
            300,
            300,
            "feature",
            context="{} {}".format(feat.get("title", ""), feat.get("desc", "")),
        )
        feats_html += (
            '<div class="feat-card">'
            '<div class="feat-circle"><img loading="lazy" src="{}" alt="{}"></div>'.format(
                fi, feat.get("title", "")
            )
            + "<h4>{}</h4>".format(feat.get("title", ""))
            + "<p>{}</p>".format(feat.get("desc", ""))
            + "</div>"
        )

    ings_html = ""
    for i, ing in enumerate(data.get("ingredients", [])[:4], 1):
        ii = img("IMG_ING_{}".format(i), ing.get("image_search", "ingredient"), 300, 300, "ingredient")
        ings_html += (
            '<div class="ing-card">'
            '<img loading="lazy" src="{}" alt="{}">'.format(ii, ing.get("name", ""))
            + "<h4>{}</h4>".format(ing.get("name", ""))
            + "<p>{}</p>".format(ing.get("benefit", ""))
            + "</div>"
        )

    steps_html = ""
    step_imgs = data.get("how_to_use_images", [])
    for i, step in enumerate(data.get("how_to_use", [])[:4], 1):
        sk = step_imgs[i - 1] if i - 1 < len(step_imgs) else "step {}".format(i)
        si = img("IMG_STEP_{}".format(i), sk, 400, 300, "gif_step", step)
        steps_html += (
            '<div class="step-card">'
            '<img loading="lazy" src="{}" alt="step {}">'.format(si, i)
            + '<div class="step-num">{}</div>'.format(i)
            + '<p class="step-txt">{}</p>'.format(step)
            + "</div>"
        )

    revs_html = ""
    for i, rev in enumerate(data.get("reviews", [])[:3], 1):
        ri = img("IMG_REV_{}".format(i), rev.get("image_search", "person"), 250, 250, "review")
        stars = "&#11088;" * int(rev.get("rating", 5))
        revs_html += (
            '<div class="rev-card">'
            '<div class="rev-top">'
            '<img loading="lazy" src="{}" class="rev-av" alt="{}">'.format(ri, rev.get("name", ""))
            + "<div><strong>{}</strong>".format(rev.get("name", ""))
            + '<div class="stars">{}</div></div>'.format(stars)
            + "</div>"
            + '<p class="rev-txt">&ldquo;{}&rdquo;</p>'.format(rev.get("comment", ""))
            + '<span class="vbadge">&#x2705; مشتري موثق</span>'
            + "</div>"
        )

    faq_html = "".join(
        '<details class="faq-item"><summary>&#x25B8; {}</summary><p>{}</p></details>'.format(
            f.get("q", ""), f.get("a", "")
        )
        for f in data.get("faq", [])[:4]
    )

    hero_benefits_html = "".join(
        '<span class="hbg">&#x2705; {}</span>'.format(f.get("title", ""))
        for f in data.get("hero_benefits", data.get("features", []))
    )

    dim_note_html = ""
    if dims.get("note"):
        dim_note_html = '<div class="dim-note">{}</div>'.format(dims.get("note", ""))

    css = (
        "* {{ margin: 0; padding: 0; box-sizing: border-box; }}"
        "body {{ font-family: 'Cairo', sans-serif; background: #fff; color: #1a1a2e; direction: rtl; }}"
        "img {{ max-width: 100%; height: auto; display: block; }}"
        "a {{ text-decoration: none; }}"
        ".cnt {{ max-width: 680px; margin: 0 auto; padding: 0 15px; }}"
        ".topbar {{ background: linear-gradient(135deg, {g1}, {g2}); color: #fff; text-align: center; padding: 10px; position: sticky; top: 0; z-index: 999; box-shadow: 0 4px 20px rgba(0,0,0,.35); }}"
        ".topbar .ot {{ font-weight: 900; font-size: 1rem; margin-bottom: 6px; }}"
        ".tr {{ display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 7px; }}"
        ".tb {{ background: rgba(0,0,0,.3); padding: 5px 12px; border-radius: 8px; font-weight: 900; font-size: 1.4rem; min-width: 46px; text-align: center; border: 1px solid rgba(255,255,255,.25); }}"
        ".ts {{ font-size: 1.4rem; font-weight: 900; }}"
        ".tbb {{ display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }}"
        ".tb-b {{ background: rgba(255,255,255,.15); padding: 3px 10px; border-radius: 20px; font-size: .78rem; font-weight: 600; }}"
        ".hero {{ background: linear-gradient(180deg, #0d0d1a, #1a1a2e 55%, {g1}); overflow: hidden; }}"
        ".hero-top {{ display: flex; align-items: flex-end; justify-content: space-between; max-width: 680px; margin: 0 auto; padding: 25px 15px 0; gap: 10px; }}"
        ".hero-txt {{ flex: 1; color: #fff; padding-bottom: 15px; }}"
        ".hero-txt h1 {{ font-size: 1.6rem; font-weight: 900; line-height: 1.35; margin-bottom: 10px; text-shadow: 0 2px 10px rgba(0,0,0,.5); }}"
        ".hero-txt .sub {{ font-size: .88rem; color: rgba(255,255,255,.85); margin-bottom: 14px; line-height: 1.6; }}"
        ".hero-person {{ flex: 0 0 280px; max-width: 280px; border-radius: 16px 16px 0 0; height: 420px; object-fit: cover; box-shadow: -8px 0 25px rgba(0,0,0,.45); }}"
        ".hero-bgs {{ display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }}"
        ".hbg {{ background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22); color: #fff; padding: 4px 10px; border-radius: 20px; font-size: .72rem; font-weight: 600; }}"
        ".hero-sp {{ background: {a}; color: #fff; text-align: center; padding: 11px; font-size: .95rem; font-weight: 700; border-radius: 12px; max-width: 300px; margin: 12px auto; }}"
        ".hero-product-row {{ display: flex; justify-content: center; align-items: center; gap: 15px; padding: 15px; background: rgba(0,0,0,.2); }}"
        ".hero-prod-img {{ width: 160px; border-radius: 14px; filter: drop-shadow(0 8px 20px rgba(0,0,0,.6)); }}"
        ".hero-lifestyle {{ width: 100%; max-height: 200px; object-fit: cover; }}"
        ".btn {{ display: block; background: linear-gradient(135deg, {a}, #f59e0b); color: #fff; padding: 15px 30px; border-radius: 14px; font-weight: 900; font-size: 1.15rem; text-align: center; max-width: 400px; margin: 18px auto; box-shadow: 0 8px 25px rgba(245,158,11,.4); border: 2px solid rgba(255,255,255,.25); transition: transform .2s; }}"
        ".btn:hover {{ transform: translateY(-3px); }}"
        ".sec {{ padding: 35px 15px; }}"
        ".sec-dark {{ background: linear-gradient(135deg, #0d0d1a, #1a1a2e); color: #fff; padding: 35px 15px; }}"
        ".sec-color {{ background: linear-gradient(135deg, {s}, #fff); padding: 35px 15px; }}"
        ".sec-title {{ font-size: 1.45rem; font-weight: 900; color: {p}; text-align: center; margin-bottom: 20px; line-height: 1.4; }}"
        ".sec-dark .sec-title {{ color: #fff; }}"
        ".stats {{ display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; }}"
        ".stat-box {{ text-align: center; }}"
        ".sn {{ font-size: 2rem; font-weight: 900; color: {a}; }}"
        ".sl {{ font-size: .78rem; color: rgba(255,255,255,.8); margin-top: 3px; }}"
        ".two-col {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }}"
        ".two-col img {{ flex: 1; min-width: 200px; border-radius: 14px; box-shadow: 0 6px 20px rgba(0,0,0,.1); }}"
        ".two-col .tc-text {{ flex: 1; min-width: 200px; }}"
        ".pain {{ background: #fef2f2; border-right: 4px solid #ef4444; padding: 11px 14px; margin-bottom: 9px; border-radius: 0 10px 10px 0; font-size: .88rem; color: #991b1b; display: flex; align-items: center; gap: 8px; }}"
        ".img-pair {{ display: flex; gap: 12px; margin-top: 15px; }}"
        ".img-pair img {{ flex: 1; border-radius: 12px; min-width: 0; }}"
        ".ba-wrap {{ position: relative; display: flex; max-width: 600px; margin: 20px auto; border-radius: 18px; overflow: hidden; box-shadow: 0 12px 35px rgba(0,0,0,.45); }}"
        ".ba-card {{ flex: 1; position: relative; }}"
        ".ba-card img {{ width: 100%; height: 260px; object-fit: cover; }}"
        ".ba-lbl {{ position: absolute; top: 10px; right: 10px; font-weight: 900; font-size: .95rem; padding: 4px 16px; border-radius: 20px; }}"
        ".ba-before .ba-lbl {{ background: #ef4444; color: #fff; }}"
        ".ba-after .ba-lbl {{ background: #22c55e; color: #fff; }}"
        ".ba-arrow {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 44px; height: 44px; background: {a}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; z-index: 5; box-shadow: 0 4px 15px rgba(0,0,0,.4); }}"
        ".docs-grid {{ display: flex; gap: 18px; flex-wrap: wrap; justify-content: center; }}"
        ".doc-card {{ display: flex; gap: 15px; background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 6px 20px rgba(0,0,0,.08); padding: 0; flex: 1; min-width: 280px; max-width: 640px; border: 1px solid rgba(30,64,175,.13); }}"
        ".doc-card img {{ width: 120px; min-width: 120px; object-fit: cover; border-radius: 0; }}"
        ".doc-info {{ padding: 15px 15px 15px 10px; flex: 1; }}"
        ".doc-name {{ font-weight: 900; font-size: 1rem; color: {p}; margin-bottom: 3px; }}"
        ".doc-title {{ font-size: .8rem; color: #666; margin-bottom: 10px; }}"
        ".doc-quote {{ font-size: .88rem; color: #333; line-height: 1.6; font-style: italic; background: {s}; padding: 10px; border-radius: 10px; border-right: 3px solid {p}; }}"
        ".qm {{ font-size: 1.5rem; color: {a}; line-height: .3; display: inline-block; vertical-align: bottom; }}"
        ".fam-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 640px; margin: 20px auto; }}"
        ".fam-img {{ border-radius: 14px; overflow: hidden; }}"
        ".fam-img img {{ width: 100%; height: 200px; object-fit: cover; transition: transform .3s; }}"
        ".fam-img img:hover {{ transform: scale(1.03); }}"
        ".feat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}"
        ".feat-card {{ background: #fff; border-radius: 16px; padding: 20px 15px; text-align: center; box-shadow: 0 5px 18px rgba(0,0,0,.07); border: 1px solid #f1f5f9; }}"
        ".feat-circle {{ width: 110px; height: 110px; border-radius: 50%; overflow: hidden; margin: 0 auto 13px; border: 3px solid {p}; box-shadow: 0 4px 14px rgba(30,64,175,.2); }}"
        ".feat-circle img {{ width: 100%; height: 100%; object-fit: cover; }}"
        ".feat-card h4 {{ color: {p}; font-size: .92rem; font-weight: 700; margin-bottom: 5px; }}"
        ".feat-card p {{ font-size: .8rem; color: #666; line-height: 1.5; }}"
        ".ing-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}"
        ".ing-card {{ text-align: center; background: #fff; border-radius: 14px; padding: 14px 8px; box-shadow: 0 3px 12px rgba(0,0,0,.06); }}"
        ".ing-card img {{ width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 8px; object-fit: cover; border: 2px solid {a}; }}"
        ".ing-card h4 {{ font-size: .82rem; color: {p}; font-weight: 700; }}"
        ".ing-card p {{ font-size: .74rem; color: #666; margin-top: 3px; }}"
        ".steps-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}"
        ".step-card {{ border-radius: 14px; overflow: hidden; background: #fff; box-shadow: 0 4px 14px rgba(0,0,0,.07); position: relative; }}"
        ".step-card img {{ width: 100%; height: 160px; object-fit: cover; }}"
        ".step-num {{ position: absolute; top: 8px; right: 8px; background: linear-gradient(135deg, {g1}, {g2}); color: #fff; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: .9rem; box-shadow: 0 3px 10px rgba(0,0,0,.3); }}"
        ".step-txt {{ padding: 10px; font-size: .8rem; color: #333; line-height: 1.5; }}"
        ".dim-grid {{ display: flex; gap: 18px; align-items: flex-start; flex-wrap: wrap; }}"
        ".dim-imgs {{ flex: 1; min-width: 220px; }}"
        ".dim-imgs img {{ border-radius: 14px; margin-bottom: 10px; box-shadow: 0 6px 18px rgba(0,0,0,.1); }}"
        ".dim-table {{ flex: 1; min-width: 220px; }}"
        ".dim-row {{ display: flex; justify-content: space-between; padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-size: .9rem; }}"
        ".dim-row:last-child {{ border-bottom: none; }}"
        ".dim-row .label {{ color: #666; font-weight: 600; }}"
        ".dim-row .value {{ color: {p}; font-weight: 900; }}"
        ".dim-note {{ background: {s}; border-radius: 12px; padding: 12px; margin-top: 10px; font-size: .85rem; color: #555; border-right: 3px solid {p}; }}"
        ".revs-grid {{ display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; }}"
        ".rev-card {{ background: #fff; border-radius: 16px; padding: 18px; min-width: 200px; flex: 1; max-width: 280px; box-shadow: 0 4px 15px rgba(0,0,0,.07); border: 1px solid #f1f5f9; }}"
        ".rev-top {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}"
        ".rev-av {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid {a}; flex-shrink: 0; }}"
        ".rev-top strong {{ display: block; font-size: .9rem; }}"
        ".stars {{ color: #f59e0b; font-size: .85rem; margin-top: 3px; }}"
        ".rev-txt {{ font-size: .85rem; color: #444; font-style: italic; margin-bottom: 10px; line-height: 1.6; }}"
        ".vbadge {{ background: #f0fdf4; color: #166534; font-size: .72rem; padding: 3px 10px; border-radius: 10px; font-weight: 600; }}"
        ".price-box {{ text-align: center; background: linear-gradient(135deg, {s}, #fff); padding: 35px 20px; border-radius: 20px; max-width: 420px; margin: 0 auto; box-shadow: 0 10px 35px rgba(0,0,0,.1); border: 2px solid rgba(30,64,175,.13); }}"
        ".old-p {{ font-size: 1.2rem; color: #999; text-decoration: line-through; }}"
        ".new-p {{ font-size: 2.8rem; font-weight: 900; color: {p}; margin: 8px 0; }}"
        ".dtag {{ background: #ef4444; color: #fff; padding: 5px 18px; border-radius: 20px; font-size: .88rem; font-weight: 700; display: inline-block; }}"
        ".g-row {{ display: flex; justify-content: center; gap: 18px; margin-top: 14px; font-size: .82rem; color: #666; flex-wrap: wrap; }}"
        ".faq-item {{ border-bottom: 1px solid #e5e7eb; padding: 15px 0; }}"
        ".faq-item summary {{ font-weight: 700; cursor: pointer; color: {p}; font-size: .95rem; list-style: none; }}"
        ".faq-item p {{ padding: 10px 0 0; color: #555; font-size: .88rem; line-height: 1.6; }}"
        ".gbox {{ text-align: center; background: #f0fdf4; border: 2px solid #22c55e; border-radius: 18px; padding: 28px; max-width: 500px; margin: 0 auto; }}"
        ".gbox h3 {{ color: #15803d; font-size: 1.15rem; font-weight: 900; margin-bottom: 8px; }}"
        ".gbox p {{ color: #166534; font-size: .88rem; line-height: 1.6; }}"
        ".final {{ background: linear-gradient(135deg, {g1}, {g2}); padding: 50px 15px; text-align: center; color: #fff; }}"
        ".final h2 {{ font-size: 1.55rem; font-weight: 900; margin-bottom: 10px; }}"
        ".final p {{ color: rgba(255,255,255,.85); margin-bottom: 20px; font-size: .92rem; }}"
        "@media (max-width: 600px) {{"
        "  .hero-person {{ flex: 0 0 200px; max-width: 200px; height: 320px; }}"
        "  .hero-txt h1 {{ font-size: 1.25rem; }}"
        "  .feat-grid {{ grid-template-columns: 1fr 1fr; }}"
        "  .ing-grid {{ grid-template-columns: 1fr 1fr; }}"
        "  .steps-grid {{ grid-template-columns: 1fr 1fr; }}"
        "  .ba-card img {{ height: 170px; }}"
        "  .fam-grid {{ grid-template-columns: 1fr 1fr; }}"
        "  .doc-card {{ flex-direction: column; }}"
        "  .doc-card img {{ width: 100%; height: 160px; border-radius: 14px 14px 0 0; }}"
        "  .dim-grid {{ flex-direction: column; }}"
        "}}"
    ).format(p=p, s=s, a=a, g1=g1, g2=g2)

    html = (
        "<!DOCTYPE html>\n"
        '<html lang="ar" dir="rtl">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">\n'
        "<style>{css}</style>\n"
        "</head>\n"
        "<body>\n"
        '<div class="topbar">\n'
        '  <div class="ot">{urgency}</div>\n'
        '  <div class="tr">\n'
        '    <div class="tb" id="cd-h">00</div><span class="ts">:</span>\n'
        '    <div class="tb" id="cd-m">00</div><span class="ts">:</span>\n'
        '    <div class="tb" id="cd-s">00</div>\n'
        "  </div>\n"
        '  <div class="tbb">{tb_badges}</div>\n'
        "</div>\n"
        '<div class="hero">\n'
        '  <div class="hero-top">\n'
        '    <div class="hero-txt">\n'
        "      <h1>{hero_headline}</h1>\n"
        '      <p class="sub">{hero_sub}</p>\n'
        '      <div class="hero-bgs">{hero_benefits_html}</div>\n'
        '      <div class="hero-sp">&#x1F465; {sp_number} {sp_text}</div>\n'
        '      <a href="#order" class="btn">{cta} &#x27A1;</a>\n'
        "    </div>\n"
        '    <img src="{hero_person}" class="hero-person" alt="hero" loading="lazy">\n'
        "  </div>\n"
        '  <div class="hero-product-row">\n'
        '    <img src="{hero_product}" class="hero-prod-img" alt="product" loading="lazy">\n'
        '    <div style="color:#fff;flex:1;font-size:.9rem;opacity:.9;line-height:1.7;">{hero_sub}</div>\n'
        "  </div>\n"
        '  <img src="{hero_lifestyle}" class="hero-lifestyle" alt="lifestyle" loading="lazy">\n'
        "</div>\n"
        '<div class="sec-dark">\n'
        '  <div class="cnt"><div class="stats">{stats_html}</div></div>\n'
        "</div>\n"
        '<div class="sec">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">{problem_title}</h2>\n'
        '    <div class="two-col">\n'
        '      <img loading="lazy" src="{prob1}" alt="problem 1">\n'
        '      <div class="tc-text">\n'
        '        <p style="color:#555;line-height:1.7;margin-bottom:14px;">{problem_desc}</p>\n'
        "        {probs_html}\n"
        "      </div>\n"
        "    </div>\n"
        '    <div class="img-pair">\n'
        '      <img loading="lazy" src="{prob2}" alt="problem 2" style="border-radius:12px;">\n'
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec-color">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">{solution_title}</h2>\n'
        '    <div class="two-col">\n'
        '      <div class="tc-text">\n'
        '        <p style="color:#333;line-height:1.7;font-size:1rem;">{solution_desc}</p>\n'
        "      </div>\n"
        '      <img loading="lazy" src="{sol1}" alt="solution 1">\n'
        "    </div>\n"
        '    <div class="img-pair">\n'
        '      <img loading="lazy" src="{sol2}" alt="solution 2" style="border-radius:12px;width:100%;">\n'
        "    </div>\n"
        '    <a href="#order" class="btn">{cta} &#x27A1;</a>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec-dark">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x2728; الفرق واضح &mdash; قبل وبعد</h2>\n'
        '    <div style="position:relative;">\n'
        '      <div class="ba-wrap">\n'
        '        <div class="ba-card ba-before">\n'
        '          <img loading="lazy" src="{before_img}" alt="before">\n'
        '          <div class="ba-lbl">قبل</div>\n'
        "        </div>\n"
        '        <div class="ba-card ba-after">\n'
        '          <img loading="lazy" src="{after_img}" alt="after">\n'
        '          <div class="ba-lbl">بعد</div>\n'
        "        </div>\n"
        "      </div>\n"
        '      <div class="ba-arrow">&#x27A1;</div>\n'
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec-color">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">رأي الأطباء والخبراء</h2>\n'
        '    <div class="docs-grid">{docs_html}</div>\n'
        '    <a href="#order" class="btn" style="margin-top:25px;">{cta} &#x27A1;</a>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec-dark">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">{family_headline}</h2>\n'
        '    <div class="fam-grid">\n'
        '      <div class="fam-img"><img loading="lazy" src="{fam1}" alt="family 1"></div>\n'
        '      <div class="fam-img"><img loading="lazy" src="{fam2}" alt="family 2"></div>\n'
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x2B50; المميزات &mdash; لماذا هو مختلف؟</h2>\n'
        '    <div class="feat-grid">{feats_html}</div>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec-color">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x1F33F; السر في مكوناتنا الطبيعية</h2>\n'
        '    <div class="ing-grid">{ings_html}</div>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x1F4CB; كيف تستخدمه؟ &mdash; 4 خطوات بسيطة</h2>\n'
        '    <div class="steps-grid">{steps_html}</div>\n'
        '    <a href="#order" class="btn" style="margin-top:25px;">{cta} &#x27A1;</a>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec-color">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x1F4D0; أبعاد وحجم المنتج</h2>\n'
        '    <div class="dim-grid">\n'
        '      <div class="dim-imgs">\n'
        '        <img loading="lazy" src="{dim1}" alt="dimensions">\n'
        '        <img loading="lazy" src="{dim2}" alt="packaging">\n'
        "      </div>\n"
        '      <div class="dim-table">\n'
        '        <div class="dim-row"><span class="label">الارتفاع</span><span class="value">{dim_h}</span></div>\n'
        '        <div class="dim-row"><span class="label">العرض</span><span class="value">{dim_w}</span></div>\n'
        '        <div class="dim-row"><span class="label">الوزن</span><span class="value">{dim_wt}</span></div>\n'
        '        <div class="dim-row"><span class="label">الحجم</span><span class="value">{dim_v}</span></div>\n'
        "        {dim_note_html}\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec-dark">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x1F4AC; آراء عملائنا الحقيقيين</h2>\n'
        '    <div class="revs-grid">{revs_html}</div>\n'
        "  </div>\n"
        "</div>\n"
        '<div class="sec" id="order">\n'
        '  <div class="cnt">\n'
        '    <div class="price-box">\n'
        '      <h2 class="sec-title">&#x1F6D2; احصل عليه الآن!</h2>\n'
        '      <div class="old-p">{price_orig} {price_cur}</div>\n'
        '      <div class="new-p">{price_disc} {price_cur}</div>\n'
        '      <div class="dtag">&#x1F525; خصم {price_pct}</div>\n'
        '      <a href="#" class="btn" style="margin-top:22px;">{cta} &#x27A1;</a>\n'
        '      <div class="g-row"><span>&#x1F6E1;&#xFE0F; ضمان 30 يوم</span><span>&#x1F69A; شحن مجاني</span><span>&#x1F4B3; دفع عند الاستلام</span></div>\n'
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec">\n'
        '  <div class="cnt">\n'
        '    <h2 class="sec-title">&#x2753; الأسئلة الشائعة</h2>\n'
        "    {faq_html}\n"
        "  </div>\n"
        "</div>\n"
        '<div class="sec">\n'
        '  <div class="cnt">\n'
        '    <div class="gbox">\n'
        '      <div style="font-size:3rem;margin-bottom:10px;">&#x1F6E1;&#xFE0F;</div>\n'
        "      <h3>{guarantee_title}</h3>\n"
        "      <p>{guarantee_text}</p>\n"
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        '<div class="final">\n'
        '  <div class="cnt">\n'
        "    <h2>لا تفوت هذا العرض الاستثنائي!</h2>\n"
        "    <p>{urgency}</p>\n"
        '    <a href="#order" class="btn" style="background:#fff;color:{p};max-width:350px;">{cta} &#x27A1;</a>\n'
        '    <p style="margin-top:18px;font-size:.78rem;opacity:.55;">{footer}</p>\n'
        "  </div>\n"
        "</div>\n"
        "<script>\n"
        "(function() {{\n"
        "  var hrs = {cdh};\n"
        "  var key = 'cd_v3';\n"
        "  var stored = localStorage.getItem(key);\n"
        "  var end = stored ? parseInt(stored) : 0;\n"
        "  if (!end || end < Date.now()) {{\n"
        "    end = Date.now() + hrs * 3600000;\n"
        "    localStorage.setItem(key, end);\n"
        "  }}\n"
        "  function pad(n) {{ return n < 10 ? '0' + n : '' + n; }}\n"
        "  function tick() {{\n"
        "    var l = Math.max(0, end - Date.now());\n"
        "    var eh = document.getElementById('cd-h');\n"
        "    var em = document.getElementById('cd-m');\n"
        "    var es = document.getElementById('cd-s');\n"
        "    if (eh) {{ eh.textContent = pad(Math.floor(l / 3600000)); }}\n"
        "    if (em) {{ em.textContent = pad(Math.floor(l % 3600000 / 60000)); }}\n"
        "    if (es) {{ es.textContent = pad(Math.floor(l % 60000 / 1000)); }}\n"
        "    if (l > 0) {{ setTimeout(tick, 1000); }}\n"
        "  }}\n"
        "  tick();\n"
        "}})();\n"
        "</script>\n"
        "</body>\n"
        "</html>"
    ).format(
        css=css,
        urgency=data.get("urgency_text", ""),
        tb_badges=tb_badges,
        hero_headline=data.get("hero_headline", ""),
        hero_sub=data.get("hero_subheadline", ""),
        hero_benefits_html=hero_benefits_html,
        sp_number=data.get("social_proof_number", ""),
        sp_text=data.get("social_proof_text", ""),
        cta=cta,
        hero_person=hero_person,
        hero_product=hero_product,
        hero_lifestyle=hero_lifestyle,
        stats_html=stats_html,
        problem_title=data.get("problem_title", ""),
        prob1=prob1,
        problem_desc=data.get("problem_description", ""),
        probs_html=probs_html,
        prob2=prob2,
        solution_title=data.get("solution_title", ""),
        sol1=sol1,
        solution_desc=data.get("solution_description", ""),
        sol2=sol2,
        before_img=before_img,
        after_img=after_img,
        docs_html=docs_html,
        family_headline=data.get("family_headline", "يثق بنا الآلاف"),
        fam1=fam1,
        fam2=fam2,
        feats_html=feats_html,
        ings_html=ings_html,
        steps_html=steps_html,
        dim1=dim1,
        dim2=dim2,
        dim_h=dims.get("height", ""),
        dim_w=dims.get("width", ""),
        dim_wt=dims.get("weight", ""),
        dim_v=dims.get("volume", ""),
        dim_note_html=dim_note_html,
        revs_html=revs_html,
        price_orig=pricing.get("original", ""),
        price_cur=pricing.get("currency", ""),
        price_disc=pricing.get("discounted", ""),
        price_pct=pricing.get("discount_percent", ""),
        faq_html=faq_html,
        guarantee_title=data.get("guarantee_title", ""),
        guarantee_text=data.get("guarantee_text", ""),
        footer=data.get("footer_text", ""),
        p=p,
        cdh=cdh,
    )
    return html


# ─── YOUCAN EXPORT ────────────────────────────────────────────────────────────


def get_youcan_html(html):
    sm = re.search(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    style_content = sm.group(1) if sm else ""

    for pat in [r"\*\s*\{[^}]*\}", r"body\s*\{[^}]*\}", r"img\s*\{[^}]*\}", r"\ba\b\s*\{[^}]*\}"]:
        style_content = re.sub(pat, "", style_content)

    scoped = ""
    for m in re.finditer(r"(@media[^{]+\{)(.*?)\}\s*\}", style_content, re.DOTALL):
        media_inner = ""
        for rm in re.finditer(r"([^{]+)\{([^}]+)\}", m.group(2)):
            media_inner += ".ali-lp {}{{{}}}\n".format(rm.group(1).strip(), rm.group(2).strip())
        media_query = m.group(1).strip()
        scoped += "{}{{{}}}\n".format(media_query, media_inner)

    for m in re.finditer(r"((?:[.#\w][^{@]*?))\{([^}]+)\}", style_content):
        sel = m.group(1).strip()
        rules = m.group(2).strip()
        if not sel or not rules or sel.startswith("@"):
            continue
        scoped += ".ali-lp {}{{{}}}\n".format(sel, rules)

    scoped += ".ali-lp img { max-width: 100%; height: auto; display: block; }\n"
    scoped += ".ali-lp a { text-decoration: none; }\n"

    bm = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    body = bm.group(1) if bm else html
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL)

    for pat in [
        r"<!DOCTYPE[^>]*>",
        r"</?(?:html|head|body)[^>]*>",
        r"<meta[^>]*>",
        r"<link[^>]*>",
        r"<style[^>]*>.*?</style>",
    ]:
        body = re.sub(pat, "", body, flags=re.DOTALL | re.IGNORECASE)

    body = body.replace(' data-src="', ' src="')
    result = (
        "<style>\n{}</style>\n"
        '<div class="ali-lp" style="direction:rtl;font-family:\'Cairo\',sans-serif;max-width:680px;margin:0 auto;">\n'
        "{}\n</div>"
    ).format(scoped, body.strip())
    return re.sub(r"\n\s*\n\s*\n", "\n\n", result).strip()


def generate_youcan_json(html):
    yc_html = get_youcan_html(html)
    page_json = {
        "sections": [
            {
                "id": "custom_html_1",
                "type": "custom_html",
                "settings": {"html": yc_html},
            }
        ]
    }
    return json.dumps(page_json, ensure_ascii=False, indent=2)


# ─── AI IMAGE GENERATION ──────────────────────────────────────────────────────


def generate_nb_image(api_key, prompt, ref_b64=None):
    try:
        import io
        from PIL import Image as PILImage

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash-preview-image-generation:generateContent?key={}".format(api_key)
        )
        full_prompt = "{}. Professional commercial photo, 8k quality, no text no letters no words no writing.".format(
            prompt
        )

        if ref_b64:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"inline_data": {"mime_type": "image/jpeg", "data": ref_b64}},
                            {"text": "Based on this product image, generate: {}".format(full_prompt)},
                        ]
                    }
                ],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
            }
        else:
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
            }

        for _retry in range(3):
            resp = requests.post(url, json=payload, timeout=90)
            if resp.status_code == 429:
                wait_t = 15 * (_retry + 1)
                st.warning("Rate limit hit, waiting {}s...".format(wait_t))
                time.sleep(wait_t)
                continue
            resp.raise_for_status()
            break

        resp_data = resp.json()
        for part in resp_data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                pil_img = PILImage.open(io.BytesIO(img_bytes))
                pil_img.thumbnail((300, 300))
                buf = io.BytesIO()
                pil_img.convert("RGB").save(buf, format="JPEG", quality=65, optimize=True)
                b = base64.b64encode(buf.getvalue()).decode()
                del pil_img, buf
                import gc

                gc.collect()
                return "data:image/jpeg;base64,{}".format(b)

        st.warning("No image in response: {}".format(str(resp_data)[:300]))
        return None

    except Exception as e:
        st.warning("IMG ERR: {}".format(str(e)[:200]))
        return None


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

st.sidebar.header("⚙️ الإعدادات")
global_api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")
global_product_name = st.sidebar.text_input(
    "📦 اسم وتفاصيل المنتج", placeholder="مثال: نظارات رؤية ليلية للقيادة"
)
global_category = st.sidebar.selectbox(
    "📁 فئة المنتج",
    [
        "💄 مستحضرات تجميل وعناية (Cosmetics)",
        "⚙️ أدوات وأجهزة ذكية (Gadgets)",
        "🌿 صحة ومكملات (Health)",
        "👗 أزياء وموضة (Fashion)",
    ],
)

uploaded_img = st.sidebar.file_uploader(
    "📷 صورة المنتج (مرجع AI)", type=["png", "jpg", "jpeg", "webp"]
)
product_image_b64 = None

if uploaded_img:
    product_image_b64 = base64.b64encode(uploaded_img.read()).decode("utf-8")
    uploaded_img.seek(0)
    st.sidebar.image(uploaded_img, caption="صورة المنتج")

st.sidebar.markdown("---")
app_mode = st.sidebar.radio(
    "🛠️ الأداة:",
    [
        "🏗️ منشئ صفحات الهبوط",
        "🔍 بحث السوق المعمق (SOP-1)",
        "💰 حاسبة التعادل المالي (Matrix)",
    ],
)

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

if app_mode == "🏗️ منشئ صفحات الهبوط":
    cols_info = st.columns(5)
    cols_info[0].metric("الأقسام", "15")
    cols_info[1].metric("الصور", "30+")
    cols_info[2].metric("أطباء", "2")
    cols_info[3].metric("خطوات الاستخدام", "4")
    cols_info[4].metric("مكونات", "4")

    if st.button("🚀 توليد صفحة الهبوط الكاملة (15 قسم + 30 صورة)"):
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال مفتاح API واسم المنتج.")
        else:
            with st.spinner("🤖 جاري بناء الصفحة..."):
                try:
                    raw = generate_lp_json(global_api_key, global_product_name, global_category)
                    try:
                        lp_data = json.loads(raw)
                    except Exception:
                        fixed = re.sub(r",\s*([}\]])", r"\1", raw)
                        lp_data = json.loads(fixed)

                    lp_data["_product_name"] = global_product_name
                    colors = detect_colors(global_product_name, global_category)

                    st.session_state.lp_data = lp_data
                    st.session_state.lp_colors = colors
                    st.session_state.lp_html = build_lp_html(lp_data, colors)

                    st.info("🤖 جاري توليد الصور بالذكاء الاصطناعي ودمجها تلقائياً...")
                    slots = extract_image_slots(lp_data)
                    generated = {}
                    ref = product_image_b64 if product_image_b64 else None
                    prog = st.progress(0)
                    status_txt = st.empty()

                    for i, slot in enumerate(slots):
                        status_txt.text(
                            "⏳ توليد صورة {} ({}/{})".format(slot["key"], i + 1, len(slots))
                        )
                        img_data = generate_nb_image(
                            global_api_key,
                            "Professional commercial photo. {}. 8k ultra high quality. no text no letters no words no writing no captions.".format(
                                slot["prompt"]
                            ),
                            ref_b64=ref,
                        )
                        if img_data:
                            generated[slot["key"]] = img_data
                            st.session_state["lp_ai_images"] = dict(generated)
                        prog.progress((i + 1) / len(slots))
                        import gc

                        gc.collect()
                        time.sleep(1)

                    status_txt.empty()
                    prog.empty()

                    st.session_state.lp_ai_images = generated
                    new_html = build_lp_html(lp_data, colors, image_map=generated)
                    st.session_state.lp_html = new_html
                    st.session_state.lp_html_ai = new_html
                    st.success(
                        "🎉 تم توليد {} صورة ودمجها تلقائياً في صفحة الهبوط!".format(len(generated))
                    )

                except Exception as e:
                    traceback.print_exc()
                    st.session_state["lp_error"] = str(e)
                    st.error("🛑 {}".format(str(e)))

    if "lp_html" in st.session_state:
        t1, t2, t3, t4, t5 = st.tabs(
            ["📱 المعاينة", "🤖 صور AI", "📥 JSON", "📤 YouCan", "🎨 برومبتات"]
        )

        with t1:
            preview = build_lp_html(
                st.session_state.lp_data,
                st.session_state.lp_colors,
                image_map=st.session_state.get("lp_ai_images"),
            )
            st.download_button(
                "⬇️ تحميل HTML", preview, "landing_page.html", "text/html", key="dl_html_main"
            )
            components.html(preview, height=6000, scrolling=True)

        with t2:
            st.markdown("### 🤖 توليد الصور بـ Gemini AI ودمجها")
            if "lp_data" not in st.session_state:
                st.warning("ولّد الصفحة أولاً.")
            else:
                slots = extract_image_slots(st.session_state.lp_data)
                c1, c2 = st.columns(2)
                with c1:
                    use_ref = st.checkbox("استخدام صورة المنتج مرجعاً", value=bool(product_image_b64))
                with c2:
                    st.metric("إجمالي الصور", len(slots))

                if st.button("🚀 توليد جميع الصور ودمجها في HTML", key="gen_ai"):
                    if not global_api_key:
                        st.error("أدخل مفتاح API")
                    else:
                        prog2 = st.progress(0)
                        status2 = st.empty()
                        generated2 = {}
                        ref2 = product_image_b64 if use_ref else None

                        for i, slot in enumerate(slots):
                            status2.text("⏳ {} ({}/{})".format(slot["key"], i + 1, len(slots)))
                            img_data = generate_nb_image(
                                global_api_key,
                                "Professional commercial photo. {}. 8k ultra high quality. no text no letters no words no writing no captions.".format(
                                    slot["prompt"]
                                ),
                                ref_b64=ref2,
                            )
                            if img_data:
                                generated2[slot["key"]] = img_data
                            prog2.progress((i + 1) / len(slots))
                            import gc

                            gc.collect()
                            time.sleep(1)

                        status2.success("✅ {} صورة!".format(len(generated2)))
                        st.session_state.lp_ai_images = generated2
                        new_html2 = build_lp_html(
                            st.session_state.lp_data,
                            st.session_state.lp_colors,
                            image_map=generated2,
                        )
                        st.session_state.lp_html_ai = new_html2
                        st.success("✅ الصور مدمجة في HTML كـ base64!")
                        st.download_button(
                            "⬇️ HTML + صور AI مدمجة",
                            new_html2,
                            "lp_ai.html",
                            "text/html",
                            key="dl_ai_html",
                        )

                if "lp_ai_images" in st.session_state:
                    st.markdown("#### 🖼️ الصور المولدة")
                    cols3 = st.columns(3)
                    for i, (k, v) in enumerate(st.session_state.lp_ai_images.items()):
                        with cols3[i % 3]:
                            if v:
                                if v.startswith("data:"):
                                    st.image(base64.b64decode(v.split(",")[1]), caption=k)
                                else:
                                    st.image(v, caption=k)
                            else:
                                st.caption(k)

        with t3:
            if "lp_data" in st.session_state:
                d = {k: v for k, v in st.session_state.lp_data.items() if k != "_product_name"}
                js = json.dumps(d, ensure_ascii=False, indent=2)
                st.download_button(
                    "📥 تحميل JSON", js, "lp.json", "application/json", key="dl_lp_json"
                )
                st.json(d)

        with t4:
            src = build_lp_html(
                st.session_state.lp_data,
                st.session_state.lp_colors,
                image_map=st.session_state.get("lp_ai_images"),
            )
            yc = get_youcan_html(src)

            st.download_button(
                "📥 تحميل YouCan JSON",
                generate_youcan_json(src),
                "youcan_page.lp",
                "application/json",
                key="yc_json_dl",
            )

            if "lp_ai_images" in st.session_state:
                st.success("✅ صور AI مدمجة base64 — جاهز لـ YouCan!")
            else:
                st.info("💡 ولّد صور AI أولاً لدمجها.")

            section_map = {
                "S1": "📌 TOPBAR",
                "S2": "🏠 Hero",
                "S3": "📊 Stats",
                "S4": "😟 المشكلة",
                "S5": "✅ الحل",
                "S6": "🔄 قبل/بعد",
                "S7": "👨‍⚕️ الأطباء",
                "S8": "👨‍👩‍👧 الثقة",
                "S9": "⭐ المميزات",
                "S10": "🌿 المكونات",
                "S11": "📋 طريقة الاستخدام",
                "S12": "📐 الأبعاد",
                "S13": "💬 المراجعات",
                "S14": "💰 التسعير",
                "S15": "🚀 Final CTA",
                "FAQ": "❓ FAQ",
                "GUARANTEE": "🛡️ الضمان",
            }

            sm2 = re.search(r"(<style>.*?</style>)", yc, re.DOTALL)
            if sm2:
                with st.expander("🎨 CSS (انسخ أولاً)", expanded=False):
                    st.code(sm2.group(1), language="html")

            parts = re.split(r"(<!--\s*S\d+[^>]*-->)", yc)
            cur = "START"
            for part in parts:
                cm = re.match(r"<!--\s*(S\d+|FAQ|GUARANTEE)", part.strip())
                if cm:
                    cur = cm.group(1)
                    continue
                content = part.strip()
                if not content or content.startswith("<style"):
                    continue
                label = section_map.get(cur, "📦 {}".format(cur))
                with st.expander(label, expanded=False):
                    st.code(content, language="html")

            st.download_button("📥 YouCan HTML كامل", yc, "youcan.html", "text/html")
            yc_json = generate_youcan_json(src)
            st.download_button(
                "📥 YouCan JSON (استيراد مباشر)",
                yc_json,
                "youcan_page.lp",
                "application/json",
                key="yc_html_dl",
            )

        with t5:
            if "lp_data" in st.session_state:
                slots = extract_image_slots(st.session_state.lp_data)
                st.markdown("### 🎨 {} برومبت صورة".format(len(slots)))
                for slot in slots:
                    with st.expander("🖼️ {} — {}".format(slot["key"], slot["section"])):
                        st.code(slot["prompt"])
                        st.caption("Type: {} | Keyword: {}".format(slot["type"], slot["keyword"]))
                st.download_button(
                    "📥 CSV",
                    pd.DataFrame(slots).to_csv(index=False),
                    "prompts.csv",
                    "text/csv",
                )

# ══════════════════════════════════════════════════════════════════════════════
# SOP-1 DEEP RESEARCH
# ══════════════════════════════════════════════════════════════════════════════

elif app_mode == "🔍 بحث السوق المعمق (SOP-1)":
    st.markdown("### 🔍 البحث العميق في السوق")

    if st.button("🧠 استخراج وثائق البيع"):
        if not global_api_key or not global_product_name:
            st.error("أدخل مفتاح API واسم المنتج.")
        else:
            with st.spinner("جاري البحث..."):
                try:
                    res = generate_deep_research(
                        global_api_key, global_product_name, global_category
                    )
                    st.session_state.deep_res = res
                    st.success("✅ اكتمل!")
                except Exception as e:
                    st.error("🛑 {}".format(str(e)))

    if "deep_res" in st.session_state:
        st.markdown(st.session_state.deep_res)
        st.download_button(
            "📥 تحميل التقرير",
            st.session_state.deep_res,
            "deep_research.md",
            "text/markdown",
        )

# ══════════════════════════════════════════════════════════════════════════════
# MATRIX CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════

elif app_mode == "💰 حاسبة التعادل المالي (Matrix)":
    st.markdown("### 💰 حاسبة التعادل المالي")

    c1, c2 = st.columns(2)
    with c1:
        cost = st.number_input("💵 تكلفة المنتج", min_value=0.0, value=50.0, step=1.0)
        price = st.number_input("🏷️ سعر البيع", min_value=0.0, value=199.0, step=1.0)
        cod = st.number_input("🚚 رسوم COD/التوصيل", min_value=0.0, value=20.0, step=1.0)
        ret = st.slider("↩️ نسبة الإرجاع (%)", 0, 100, 20)
    with c2:
        budget = st.number_input(
            "📢 ميزانية الإعلان (يومي)", min_value=0.0, value=100.0, step=5.0
        )
        cpc = st.number_input("👆 تكلفة النقرة CPC", min_value=0.01, value=0.5, step=0.01)
        cvr = st.slider("🎯 معدل التحويل (%)", 0.1, 20.0, 2.0, step=0.1)

    if st.button("📊 احسب"):
        clicks = budget / cpc
        orders = clicks * (cvr / 100)
        returned = orders * (ret / 100)
        fulfilled = orders - returned
        revenue = fulfilled * price
        total_c = orders * cost + orders * cod + budget
        profit = revenue - total_c
        roas = revenue / budget if budget > 0 else 0
        cpa = budget / orders if orders > 0 else 0
        margin = profit / revenue * 100 if revenue > 0 else 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🛒 الطلبات", "{:.0f}".format(orders))
        m2.metric("✅ المنفذة", "{:.0f}".format(fulfilled))
        m3.metric("💰 الإيراد", "{:.0f}".format(revenue))
        m4.metric(
            "📈 الربح",
            "{:.0f}".format(profit),
            delta="✅ ربح" if profit > 0 else "❌ خسارة",
        )

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🎯 ROAS", "{:.2f}x".format(roas))
        r2.metric("💸 CPA", "{:.2f}".format(cpa))
        r3.metric("📉 هامش الربح", "{:.1f}%".format(margin))
        r4.metric("↩️ المرتجعة", "{:.0f}".format(returned))

        if profit > 0:
            st.success("✅ مربحة! ربح {:.2f} مقابل إنفاق {:.0f}".format(profit, budget))
        else:
            st.error("❌ خاسرة! خسارة {:.2f}".format(abs(profit)))

        with st.expander("📊 تفاصيل"):
            st.write(
                "- نقرات: {:.0f} | طلبات: {:.0f} | منفذة: {:.0f}".format(
                    clicks, orders, fulfilled
                )
            )
            st.write(
                "- تكلفة بضاعة: {:.0f} | COD: {:.0f} | إعلان: {:.0f}".format(
                    orders * cost, orders * cod, budget
                )
            )
            st.write(
                "- إجمالي تكاليف: {:.0f} | إيراد: {:.0f} | ربح: {:.0f}".format(
                    total_c, revenue, profit
                )
            )
