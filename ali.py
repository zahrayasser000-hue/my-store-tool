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
    prompt = pm.get(style, f"{safe} high quality realistic commercial photo 8k") + " no text no letters no words no writing" + " no text no letters no words no writing"
    seed = random.randint(1, 999999)
    return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt + ' no text no letters no words')}?width={width}&height={height}&nologo=true&nofeed=true&model=flux&seed={seed}"

AUTO_COLORS = {
    "skincare":  {"primary":"#be185d","secondary":"#fdf2f8","accent":"#f59e0b","gradient1":"#be185d","gradient2":"#ec4899"},
    "cosmetics": {"primary":"#0f766e","secondary":"#f0fdfa","accent":"#eab308","gradient1":"#0f766e","gradient2":"#14b8a6"},
    "health":    {"primary":"#15803d","secondary":"#f0fdf4","accent":"#f97316","gradient1":"#15803d","gradient2":"#22c55e"},
    "gadgets":   {"primary":"#1e3a5f","secondary":"#f0f4f8","accent":"#ef4444","gradient1":"#1e3a5f","gradient2":"#3b82f6"},
    "fashion":   {"primary":"#7c2d12","secondary":"#fef3c7","accent":"#d97706","gradient1":"#7c2d12","gradient2":"#ea580c"},
    "default":   {"primary":"#1e40af","secondary":"#eff6ff","accent":"#f59e0b","gradient1":"#1e40af","gradient2":"#3b82f6"},
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
    if 'model_name' in st.session_state: return st.session_state.model_name
    genai.configure(api_key=api_key, transport="rest")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.model_name = m.name; return m.name
    except: pass
    st.session_state.model_name = "gemini-pro"; return "gemini-pro"

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
  "dimensions": {{"height": "15 cm","width": "8 cm","weight": "200g","volume": "50ml","note": "ملاحظة المقاسات"}},
  "image_dimensions_search": "product flat lay ruler measurement size reference clean white background 8k",
  "image_dimensions_2_search": "product packaging box dimensions label close up clean background 8k",
  "stats": [{{"number": "98%","label": "نسبة الرضا"}},{{"number": "+5000","label": "عميل سعيد"}},{{"number": "4.9/5","label": "التقييم"}}],
  "reviews": [
    {{"name": "سارة م.","rating": 5,"comment": "تعليق واقعي تفصيلي مقنع","image_search": "close up portrait happy arab woman headshot neutral background soft lighting 8k"}},
    {{"name": "أحمد ع.","rating": 5,"comment": "تعليق واقعي تفصيلي مقنع","image_search": "close up portrait confident arab man headshot neutral background soft lighting 8k"}},
    {{"name": "نورة ك.","rating": 5,"comment": "تعليق واقعي تفصيلي مقنع","image_search": "close up portrait smiling arab woman headshot neutral background soft lighting 8k"}}
  ],
  "pricing": {{"original": "399","discounted": "199","currency": "SAR","discount_percent": "50%"}},
  "urgency_text": "⚡ العرض ينتهي خلال 24 ساعة!",
  "countdown_hours": 24,
  "faq": [
    {{"q": "متى سألاحظ النتائج؟","a": "إجابة تفصيلية"}},
    {{"q": "هل المنتج آمن؟","a": "إجابة تفصيلية"}},
    {{"q": "كيف أطلب؟","a": "إجابة تفصيلية"}},
    {{"q": "ما سياسة الإرجاع؟","a": "إجابة تفصيلية"}}
  ],
  "guarantee_title": "ضمان استرجاع الأموال 30 يوماً",
  "guarantee_text": "نص الضمان التفصيلي",
  "call_to_action": "اطلب الآن",
  "footer_text": "جميع الحقوق محفوظة"
}}
"""
    r = model.generate_content(prompt, request_options={"timeout": 60.0})
    tb = chr(96)*3
    clean = re.sub(f'{tb}(?:json|JSON)?','',r.text,flags=re.IGNORECASE).replace(tb,'').strip()
    m = re.search(r'\{.*\}', clean, re.DOTALL)
    return m.group(0) if m else clean

def generate_deep_research(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel(get_model(api_key))
    r = model.generate_content(
        f'أنت Deep Research. المنتج: "{product}". الفئة: "{category}".\nأخرج تقريراً شاملاً بالعربية Markdown:\n1. Avatar Sheet\n2. بحث السوق والمنافسين\n3. Offer Brief\n4. المعتقدات الضرورية\n5. زوايا البيع PAS+FAB',
        request_options={"timeout":60.0})
    return r.text

# ─── IMAGE SLOTS ──────────────────────────────────────────────────────────────

def extract_image_slots(data):
    slots = []
    pn = data.get('_product_name','')
    def add(key, section, keyword, itype, context=""):
        pm = {
            "product":    f"{keyword} product photo white background studio 8k",
            "lifestyle":  f"lifestyle person using {keyword} natural warm authentic 8k",
            "problem":    f"frustrated person problem {keyword} worried dramatic realistic 8k",
            "solution":   f"happy person after using {keyword} bright smile positive 8k",
            "feature":    f"visual {context} {keyword} circular white background commercial 8k",
            "ingredient": f"macro {keyword} natural organic studio white background 8k",
            "gif_step":   f"hands tutorial {keyword} clean demonstration bright 8k",
            "review":     f"happy satisfied customer avatar illustration digital art warm colors circular frame 8k",
            "doctor":     f"professional doctor white coat hospital confident smile 8k",
            "family":     f"happy arab family group {keyword} warm home authentic 8k",
            "hero_person":f"confident arab person {keyword} cinematic editorial 8k",
            "composite":  f"{keyword} product dark dramatic studio commercial 8k",
            "before":     f"BEFORE state {keyword} problem visible high quality 8k",
            "after":      f"AFTER state {keyword} problem solved improvement 8k",
            "dimensions": f"{keyword} product flat lay ruler measurement white background 8k",
        }
        prompt = pm.get(itype, f"{keyword} commercial photo 8k") + " no text no letters no words no writing"
        if pn: prompt = f"Product: {pn}. {prompt}"
        slots.append({"key":key,"section":section,"keyword":keyword,"prompt":prompt,"type":itype,"context":context})

    # HERO (3)
    add("IMG_HERO_PERSON",    "hero",           data.get('image_hero_person_search','arab person'),       "hero_person")
    add("IMG_HERO_PRODUCT",   "hero",           data.get('image_hero_product_search','product'),          "composite")
    add("IMG_HERO_LIFESTYLE", "hero",           data.get('image_hero_lifestyle_search','lifestyle'),       "lifestyle")
    # PROBLEM (2)
    add("IMG_PROB_1",         "problem",        data.get('image_problem_1_search','problem person'),      "problem")
    add("IMG_PROB_2",         "problem",        data.get('image_problem_2_search','problem visual'),      "problem")
    # SOLUTION (2)
    add("IMG_SOL_1",          "solution",       data.get('image_solution_1_search','happy person'),       "solution")
    add("IMG_SOL_2",          "solution",       data.get('image_solution_2_search','product use'),        "product")
    # BEFORE/AFTER (2)
    add("IMG_BEFORE",         "before_after",   data.get('image_before_search','before'),                 "before")
    add("IMG_AFTER",          "before_after",   data.get('image_after_search','after'),                   "after")
    # DOCTORS (2)
    for i, doc in enumerate(data.get('doctors',[])[:2], 1):
        add(f"IMG_DOC_{i}", "doctors", doc.get('image_search','doctor'), "doctor")
    # FAMILY (2)
    add("IMG_FAM_1",          "family",         data.get('image_family_1_search','family'),               "family")
    add("IMG_FAM_2",          "family",         data.get('image_family_2_search','customers'),            "family")
    # FEATURES (4)
    for i, f in enumerate(data.get('features',[])[:4], 1):
        add(f"IMG_FEAT_{i}", "features", f.get('image_search','feature'), "feature",
            context=f"{f.get('title','')} {f.get('desc','')}")
    # INGREDIENTS (4)
    for i, ing in enumerate(data.get('ingredients',[])[:4], 1):
        add(f"IMG_ING_{i}", "ingredients", ing.get('image_search','ingredient'), "ingredient")
    # STEPS (4)
    step_imgs = data.get('how_to_use_images',[])
    for i in range(min(4, len(step_imgs))):
        add(f"IMG_STEP_{i+1}", "steps", step_imgs[i], "gif_step")
    # DIMENSIONS (2)
    add("IMG_DIM_1",          "dimensions",     data.get('image_dimensions_search','product dimensions'), "dimensions")
    add("IMG_DIM_2",          "dimensions",     data.get('image_dimensions_2_search','product packaging'),"product")
    # REVIEWS (3)
    for i, rev in enumerate(data.get('reviews',[])[:3], 1):
        add(f"IMG_REV_{i}", "reviews", rev.get('image_search','person portrait'), "review")
    return slots

# ─── HTML BUILDER ─────────────────────────────────────────────────────────────

def build_lp_html(data, colors, image_map=None):
    p=colors["primary"]; s=colors["secondary"]; a=colors["accent"]
    g1=colors["gradient1"]; g2=colors["gradient2"]

    def img(key, kw, w, h, st_, context=""):
        if image_map and key in image_map: return image_map[key]
        return get_ai_image(kw, w, h, st_, context)

    # ── All images ──
    hero_person    = img("IMG_HERO_PERSON",   data.get('image_hero_person_search','person'),        600,700,"hero_person")
    hero_product   = img("IMG_HERO_PRODUCT",  data.get('image_hero_product_search','product'),      500,500,"composite")
    hero_lifestyle = img("IMG_HERO_LIFESTYLE",data.get('image_hero_lifestyle_search','lifestyle'),  800,350,"lifestyle")
    prob1          = img("IMG_PROB_1",        data.get('image_problem_1_search','problem'),         500,380,"problem")
    prob2          = img("IMG_PROB_2",        data.get('image_problem_2_search','problem2'),        500,380,"problem")
    sol1           = img("IMG_SOL_1",         data.get('image_solution_1_search','solution'),       500,380,"solution")
    sol2           = img("IMG_SOL_2",         data.get('image_solution_2_search','solution2'),      500,380,"product")
    before_img     = img("IMG_BEFORE",        data.get('image_before_search','before'),             450,320,"before")
    after_img      = img("IMG_AFTER",         data.get('image_after_search','after'),               450,320,"after")
    fam1           = img("IMG_FAM_1",         data.get('image_family_1_search','family'),           500,380,"family")
    fam2           = img("IMG_FAM_2",         data.get('image_family_2_search','customers'),        500,380,"family")
    dim1           = img("IMG_DIM_1",         data.get('image_dimensions_search','dimensions'),     500,400,"dimensions")
    dim2           = img("IMG_DIM_2",         data.get('image_dimensions_2_search','packaging'),    400,300,"product")

    badges   = data.get('trust_badges',[])
    pricing  = data.get('pricing',{})
    cta      = data.get('call_to_action','اطلب الآن')
    cdh      = data.get('countdown_hours',24)
    dims     = data.get('dimensions',{})

    tb_badges = ''.join(f'<span class="tb-b">✅ {b}</span>' for b in badges[:4])
    probs_html= ''.join(f'<div class="pain"><span>❌</span>{pt}</div>' for pt in data.get('problem_points',[]))
    stats_html= ''.join(f'<div class="stat-box"><div class="sn">{st__.get("number","")}</div><div class="sl">{st__.get("label","")}</div></div>' for st__ in data.get('stats',[])[:3])

    # DOCTORS
    docs_html = ''
    for i, doc in enumerate(data.get('doctors',[])[:2], 1):
        di = img(f"IMG_DOC_{i}", doc.get('image_search','doctor'), 300, 380, "doctor")
        docs_html += f'''<div class="doc-card">
<img loading="lazy" src="{di}" alt="{doc.get('name','')}">
<div class="doc-info">
  <div class="doc-name">{doc.get('name','')}</div>
  <div class="doc-title">{doc.get('title','')}</div>
  <div class="doc-quote"><span class="qm">"</span>{doc.get('quote','')}<span class="qm">"</span></div>
</div></div>'''

    # FEATURES
    feats_html = ''
    for i, f in enumerate(data.get('features',[])[:4], 1):
        fi = img(f"IMG_FEAT_{i}", f.get('image_search','feature'), 300, 300, "feature",
                 context=f"{f.get('title','')} {f.get('desc','')}")
        feats_html += f'''<div class="feat-card">
<div class="feat-circle"><img loading="lazy" src="{fi}" alt="{f.get('title','')}"></div>
<h4>{f.get('title','')}</h4><p>{f.get('desc','')}</p></div>'''

    # INGREDIENTS
    ings_html = ''
    for i, ing in enumerate(data.get('ingredients',[])[:4], 1):
        ii = img(f"IMG_ING_{i}", ing.get('image_search','ingredient'), 300, 300, "ingredient")
        ings_html += f'''<div class="ing-card">
<img loading="lazy" src="{ii}" alt="{ing.get('name','')}">
<h4>{ing.get('name','')}</h4><p>{ing.get('benefit','')}</p></div>'''

    # STEPS
    steps_html = ''
    step_imgs  = data.get('how_to_use_images',[])
    for i, step in enumerate(data.get('how_to_use',[])[:4], 1):
        sk = step_imgs[i-1] if i-1 < len(step_imgs) else f'step {i}'
        si = img(f"IMG_STEP_{i}", sk, 400, 300, "gif_step", step)
        steps_html += f'''<div class="step-card">
<img loading="lazy" src="{si}" alt="خطوة {i}">
<div class="step-num">{i}</div>
<p class="step-txt">{step}</p></div>'''

    # REVIEWS
    revs_html = ''
    for i, rev in enumerate(data.get('reviews',[])[:3], 1):
        ri = img(f"IMG_REV_{i}", rev.get('image_search','person'), 250, 250, "review")
        stars = '⭐'*int(rev.get('rating',5))
        revs_html += f'''<div class="rev-card">
<div class="rev-top">
  <img loading="lazy" src="{ri}" class="rev-av" onerror="this.src='https://ui-avatars.com/api/?name='+this.alt+'&background=random&size=250&bold=true'">
  <div><strong>{rev.get('name','')}</strong><div class="stars">{stars}</div></div>
</div>
<p class="rev-txt">"{rev.get('comment','')}"</p>
<span class="vbadge">✅ مشتري موثق</span></div>'''

    # FAQ
    faq_html = ''.join(f'<details class="faq-item"><summary>▸ {f.get("q","")}</summary><p>{f.get("a","")}</p></details>' for f in data.get('faq',[])[:4])

    css = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Cairo',sans-serif;background:#fff;color:#1a1a2e;direction:rtl;}}
img{{max-width:100%;height:auto;display:block;}}
a{{text-decoration:none;}}
.cnt{{max-width:680px;margin:0 auto;padding:0 15px;}}

/* TOPBAR */
.topbar{{background:linear-gradient(135deg,{g1},{g2});color:#fff;text-align:center;padding:10px;position:sticky;top:0;z-index:999;box-shadow:0 4px 20px rgba(0,0,0,.35);}}
.topbar .ot{{font-weight:900;font-size:1rem;margin-bottom:6px;}}
.tr{{display:flex;justify-content:center;align-items:center;gap:8px;margin-bottom:7px;}}
.tb{{background:rgba(0,0,0,.3);padding:5px 12px;border-radius:8px;font-weight:900;font-size:1.4rem;min-width:46px;text-align:center;border:1px solid rgba(255,255,255,.25);}}
.ts{{font-size:1.4rem;font-weight:900;}}
.tbb{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;}}
.tb-b{{background:rgba(255,255,255,.15);padding:3px 10px;border-radius:20px;font-size:.78rem;font-weight:600;}}

/* HERO */
.hero{{background:linear-gradient(180deg,#0d0d1a,#1a1a2e 55%,{g1});overflow:hidden;}}
.hero-top{{display:flex;align-items:flex-end;justify-content:space-between;max-width:680px;margin:0 auto;padding:25px 15px 0;gap:10px;}}
.hero-txt{{flex:1;color:#fff;padding-bottom:15px;}}
.hero-txt h1{{font-size:1.6rem;font-weight:900;line-height:1.35;margin-bottom:10px;text-shadow:0 2px 10px rgba(0,0,0,.5);}}
.hero-txt .sub{{font-size:.88rem;color:rgba(255,255,255,.85);margin-bottom:14px;line-height:1.6;}}
.hero-person{{flex:0 0 280px;max-width:280px;border-radius:16px 16px 0 0;height:420px;object-fit:cover;box-shadow:-8px 0 25px rgba(0,0,0,.45);}}
.hero-bgs{{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:12px;}}
.hbg{{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);color:#fff;padding:4px 10px;border-radius:20px;font-size:.72rem;font-weight:600;}}
.hero-sp{{background:{a};color:#fff;text-align:center;padding:11px;font-size:.95rem;font-weight:700;border-radius:12px;max-width:300px;margin:12px auto;}}
.hero-product-row{{display:flex;justify-content:center;align-items:center;gap:15px;padding:15px;background:rgba(0,0,0,.2);}}
.hero-prod-img{{width:160px;border-radius:14px;filter:drop-shadow(0 8px 20px rgba(0,0,0,.6));}}
.hero-lifestyle{{width:100%;max-height:200px;object-fit:cover;}}

/* CTA */
.btn{{display:block;background:linear-gradient(135deg,{a},#f59e0b);color:#fff;padding:15px 30px;border-radius:14px;font-weight:900;font-size:1.15rem;text-align:center;max-width:400px;margin:18px auto;box-shadow:0 8px 25px {a}66;border:2px solid rgba(255,255,255,.25);transition:transform .2s;}}
.btn:hover{{transform:translateY(-3px);}}

/* SECTIONS */
.sec{{padding:35px 15px;}}
.sec-dark{{background:linear-gradient(135deg,#0d0d1a,#1a1a2e);color:#fff;padding:35px 15px;}}
.sec-color{{background:linear-gradient(135deg,{s},#fff);padding:35px 15px;}}
.sec-title{{font-size:1.45rem;font-weight:900;color:{p};text-align:center;margin-bottom:20px;line-height:1.4;}}
.sec-dark .sec-title{{color:#fff;}}

/* STATS */
.stats{{display:flex;justify-content:center;gap:25px;flex-wrap:wrap;}}
.stat-box{{text-align:center;}}
.sn{{font-size:2rem;font-weight:900;color:{a};}}
.sl{{font-size:.78rem;color:rgba(255,255,255,.8);margin-top:3px;}}

/* PROBLEM / SOLUTION */
.two-col{{display:flex;gap:18px;align-items:center;flex-wrap:wrap;}}
.two-col img{{flex:1;min-width:200px;border-radius:14px;box-shadow:0 6px 20px rgba(0,0,0,.1);}}
.two-col .tc-text{{flex:1;min-width:200px;}}
.pain{{background:#fef2f2;border-right:4px solid #ef4444;padding:11px 14px;margin-bottom:9px;border-radius:0 10px 10px 0;font-size:.88rem;color:#991b1b;display:flex;align-items:center;gap:8px;}}
.img-pair{{display:flex;gap:12px;margin-top:15px;}}
.img-pair img{{flex:1;border-radius:12px;min-width:0;}}

/* BEFORE/AFTER */
.ba-wrap{{position:relative;display:flex;max-width:600px;margin:20px auto;border-radius:18px;overflow:hidden;box-shadow:0 12px 35px rgba(0,0,0,.45);}}
.ba-card{{flex:1;position:relative;}}
.ba-card img{{width:100%;height:260px;object-fit:cover;}}
.ba-lbl{{position:absolute;top:10px;right:10px;font-weight:900;font-size:.95rem;padding:4px 16px;border-radius:20px;}}
.ba-before .ba-lbl{{background:#ef4444;color:#fff;}}
.ba-after .ba-lbl{{background:#22c55e;color:#fff;}}
.ba-arrow{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;background:{a};border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;z-index:5;box-shadow:0 4px 15px rgba(0,0,0,.4);}}

/* DOCTORS */
.docs-grid{{display:flex;gap:18px;flex-wrap:wrap;justify-content:center;}}
.doc-card{{display:flex;gap:15px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,.08);padding:0;flex:1;min-width:280px;max-width:640px;border:1px solid {p}22;}}
.doc-card img{{width:120px;min-width:120px;object-fit:cover;border-radius:0;}}
.doc-info{{padding:15px 15px 15px 10px;flex:1;}}
.doc-name{{font-weight:900;font-size:1rem;color:{p};margin-bottom:3px;}}
.doc-title{{font-size:.8rem;color:#666;margin-bottom:10px;}}
.doc-quote{{font-size:.88rem;color:#333;line-height:1.6;font-style:italic;background:{s};padding:10px;border-radius:10px;border-right:3px solid {p};}}
.qm{{font-size:1.5rem;color:{a};line-height:.3;display:inline-block;vertical-align:bottom;}}

/* FAMILY */
.fam-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:640px;margin:20px auto;}}
.fam-img{{border-radius:14px;overflow:hidden;}}
.fam-img img{{width:100%;height:200px;object-fit:cover;transition:transform .3s;}}
.fam-img img:hover{{transform:scale(1.03);}}

/* FEATURES */
.feat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;}}
.feat-card{{background:#fff;border-radius:16px;padding:20px 15px;text-align:center;box-shadow:0 5px 18px rgba(0,0,0,.07);border:1px solid #f1f5f9;}}
.feat-circle{{width:110px;height:110px;border-radius:50%;overflow:hidden;margin:0 auto 13px;border:3px solid {p};box-shadow:0 4px 14px {p}33;}}
.feat-circle img{{width:100%;height:100%;object-fit:cover;}}
.feat-card h4{{color:{p};font-size:.92rem;font-weight:700;margin-bottom:5px;}}
.feat-card p{{font-size:.8rem;color:#666;line-height:1.5;}}

/* INGREDIENTS */
.ing-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}}
.ing-card{{text-align:center;background:#fff;border-radius:14px;padding:14px 8px;box-shadow:0 3px 12px rgba(0,0,0,.06);}}
.ing-card img{{width:80px;height:80px;border-radius:50%;margin:0 auto 8px;object-fit:cover;border:2px solid {a};}}
.ing-card h4{{font-size:.82rem;color:{p};font-weight:700;}}
.ing-card p{{font-size:.74rem;color:#666;margin-top:3px;}}

/* STEPS */
.steps-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}}
.step-card{{border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.07);position:relative;}}
.step-card img{{width:100%;height:160px;object-fit:cover;}}
.step-num{{position:absolute;top:8px;right:8px;background:linear-gradient(135deg,{g1},{g2});color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:.9rem;box-shadow:0 3px 10px rgba(0,0,0,.3);}}
.step-txt{{padding:10px;font-size:.8rem;color:#333;line-height:1.5;}}

/* DIMENSIONS */
.dim-grid{{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap;}}
.dim-imgs{{flex:1;min-width:220px;}}
.dim-imgs img{{border-radius:14px;margin-bottom:10px;box-shadow:0 6px 18px rgba(0,0,0,.1);}}
.dim-table{{flex:1;min-width:220px;}}
.dim-row{{display:flex;justify-content:space-between;padding:12px 15px;border-bottom:1px solid #e5e7eb;font-size:.9rem;}}
.dim-row:last-child{{border-bottom:none;}}
.dim-row .label{{color:#666;font-weight:600;}}
.dim-row .value{{color:{p};font-weight:900;}}
.dim-note{{background:{s};border-radius:12px;padding:12px;margin-top:10px;font-size:.85rem;color:#555;border-right:3px solid {p};}}

/* REVIEWS */
.revs-grid{{display:flex;gap:15px;flex-wrap:wrap;justify-content:center;}}
.rev-card{{background:#fff;border-radius:16px;padding:18px;min-width:200px;flex:1;max-width:280px;box-shadow:0 4px 15px rgba(0,0,0,.07);border:1px solid #f1f5f9;}}
.rev-top{{display:flex;align-items:center;gap:12px;margin-bottom:12px;}}
.rev-av{{width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid {a};flex-shrink:0;}}
.rev-top strong{{display:block;font-size:.9rem;}}
.stars{{color:#f59e0b;font-size:.85rem;margin-top:3px;}}
.rev-txt{{font-size:.85rem;color:#444;font-style:italic;margin-bottom:10px;line-height:1.6;}}
.vbadge{{background:#f0fdf4;color:#166534;font-size:.72rem;padding:3px 10px;border-radius:10px;font-weight:600;}}

/* PRICING */
.price-box{{text-align:center;background:linear-gradient(135deg,{s},#fff);padding:35px 20px;border-radius:20px;max-width:420px;margin:0 auto;box-shadow:0 10px 35px rgba(0,0,0,.1);border:2px solid {p}22;}}
.old-p{{font-size:1.2rem;color:#999;text-decoration:line-through;}}
.new-p{{font-size:2.8rem;font-weight:900;color:{p};margin:8px 0;}}
.dtag{{background:#ef4444;color:#fff;padding:5px 18px;border-radius:20px;font-size:.88rem;font-weight:700;display:inline-block;}}
.g-row{{display:flex;justify-content:center;gap:18px;margin-top:14px;font-size:.82rem;color:#666;flex-wrap:wrap;}}

/* FAQ */
.faq-item{{border-bottom:1px solid #e5e7eb;padding:15px 0;}}
.faq-item summary{{font-weight:700;cursor:pointer;color:{p};font-size:.95rem;list-style:none;}}
.faq-item p{{padding:10px 0 0;color:#555;font-size:.88rem;line-height:1.6;}}

/* GUARANTEE */
.gbox{{text-align:center;background:#f0fdf4;border:2px solid #22c55e;border-radius:18px;padding:28px;max-width:500px;margin:0 auto;}}
.gbox h3{{color:#15803d;font-size:1.15rem;font-weight:900;margin-bottom:8px;}}
.gbox p{{color:#166534;font-size:.88rem;line-height:1.6;}}

/* FINAL CTA */
.final{{background:linear-gradient(135deg,{g1},{g2});padding:50px 15px;text-align:center;color:#fff;}}
.final h2{{font-size:1.55rem;font-weight:900;margin-bottom:10px;}}
.final p{{color:rgba(255,255,255,.85);margin-bottom:20px;font-size:.92rem;}}

/* RESPONSIVE */
@media(max-width:600px){{
  .hero-person{{flex:0 0 200px;max-width:200px;height:320px;}}
  .hero-txt h1{{font-size:1.25rem;}}
  .feat-grid{{grid-template-columns:1fr 1fr;}}
  .ing-grid{{grid-template-columns:1fr 1fr;}}
  .steps-grid{{grid-template-columns:1fr 1fr;}}
  .ba-card img{{height:170px;}}
  .fam-grid{{grid-template-columns:1fr 1fr;}}
  .doc-card{{flex-direction:column;}}
  .doc-card img{{width:100%;height:160px;border-radius:14px 14px 0 0;}}
  .dim-grid{{flex-direction:column;}}
}}
"""

    html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>

<!-- S1: TOPBAR -->
<div class="topbar">
  <div class="ot">{data.get('urgency_text','')}</div>
  <div class="tr">
    <div class="tb" id="cd-h">00</div><span class="ts">:</span>
    <div class="tb" id="cd-m">00</div><span class="ts">:</span>
    <div class="tb" id="cd-s">00</div>
  </div>
  <div class="tbb">{tb_badges}</div>
</div>

<!-- S2: HERO -->
<div class="hero">
  <div class="hero-top">
    <div class="hero-txt">
      <h1>{data.get('hero_headline','')}</h1>
      <p class="sub">{data.get('hero_subheadline','')}</p>
      <div class="hero-bgs">{''.join(f'<span class="hbg">✅ {f.get("title","")}</span>' for f in data.get('hero_benefits', data.get('features',[])))}</div>
      <div class="hero-sp">👥 {data.get('social_proof_number','')} {data.get('social_proof_text','')}</div>
      <a href="#order" class="btn">{cta} ➜</a>
    </div>
    <img src="{hero_person}" class="hero-person" alt="hero" loading="lazy">
  </div>
  <div class="hero-product-row">
    <img src="{hero_product}" class="hero-prod-img" alt="product" loading="lazy">
    <div style="color:#fff;flex:1;font-size:.9rem;opacity:.9;line-height:1.7;">{data.get('hero_subheadline','')}</div>
  </div>
  <img src="{hero_lifestyle}" class="hero-lifestyle" alt="lifestyle" loading="lazy">
</div>

<!-- S3: STATS -->
<div class="sec-dark">
  <div class="cnt"><div class="stats">{stats_html}</div></div>
</div>

<!-- S4: PROBLEM -->
<div class="sec">
  <div class="cnt">
    <h2 class="sec-title">{data.get('problem_title','')}</h2>
    <div class="two-col">
      <img loading="lazy" src="{prob1}" alt="problem 1">
      <div class="tc-text">
        <p style="color:#555;line-height:1.7;margin-bottom:14px;">{data.get('problem_description','')}</p>
        {probs_html}
      </div>
    </div>
    <div class="img-pair" style="margin-top:15px;">
      <img loading="lazy" src="{prob2}" alt="problem 2" style="border-radius:12px;">
    </div>
  </div>
</div>

<!-- S5: SOLUTION -->
<div class="sec-color">
  <div class="cnt">
    <h2 class="sec-title">{data.get('solution_title','')}</h2>
    <div class="two-col">
      <div class="tc-text">
        <p style="color:#333;line-height:1.7;font-size:1rem;">{data.get('solution_description','')}</p>
      </div>
      <img loading="lazy" src="{sol1}" alt="solution 1">
    </div>
    <div class="img-pair" style="margin-top:15px;">
      <img loading="lazy" src="{sol2}" alt="solution 2" style="border-radius:12px;width:100%;">
    </div>
    <a href="#order" class="btn">{cta} ➜</a>
  </div>
</div>

<!-- S6: BEFORE / AFTER -->
<div class="sec-dark">
  <div class="cnt">
    <h2 class="sec-title">✨ الفرق واضح — قبل وبعد</h2>
    <div style="position:relative;">
      <div class="ba-wrap">
        <div class="ba-card ba-before">
          <img loading="lazy" src="{before_img}" alt="before">
          <div class="ba-lbl">قبل</div>
        </div>
        <div class="ba-card ba-after">
          <img loading="lazy" src="{after_img}" alt="after">
          <div class="ba-lbl">بعد</div>
        </div>
      </div>
      <div class="ba-arrow">➡</div>
    </div>
    <p style="color:rgba(255,255,255,.9);text-align:center;margin-top:15px;font-size:.95rem;">{data.get('solution_title','')}</p>
  </div>
</div>

<!-- S7: DOCTORS -->
<div class="sec-color">
  <div class="cnt">
    <h2 class="sec-title">👨‍⚕️ رأي الأطباء والخبراء</h2>
    <div class="docs-grid">{docs_html}</div>
    <a href="#order" class="btn" style="margin-top:25px;">{cta} ➜</a>
  </div>
</div>

<!-- S8: FAMILY / SOCIAL PROOF -->
<div class="sec-dark">
  <div class="cnt">
    <h2 class="sec-title">{data.get('family_headline','يثق بنا الآلاف')}</h2>
    <div class="fam-grid">
      <div class="fam-img"><img loading="lazy" src="{fam1}" alt="family 1"></div>
      <div class="fam-img"><img loading="lazy" src="{fam2}" alt="family 2"></div>
    </div>
  </div>
</div>

<!-- S9: FEATURES -->
<div class="sec">
  <div class="cnt">
    <h2 class="sec-title">⭐ تحولات & الملمة — لماذا هو مختلف؟</h2>
    <div class="feat-grid">{feats_html}</div>
  </div>
</div>

<!-- S10: INGREDIENTS -->
<div class="sec-color">
  <div class="cnt">
    <h2 class="sec-title">🌿 السر في مكوناتنا الطبيعية</h2>
    <div class="ing-grid">{ings_html}</div>
  </div>
</div>

<!-- S11: HOW TO USE -->
<div class="sec">
  <div class="cnt">
    <h2 class="sec-title">📋 كيف تستخدمه؟ — 4 خطوات بسيطة</h2>
    <div class="steps-grid">{steps_html}</div>
    <a href="#order" class="btn" style="margin-top:25px;">{cta} ➜</a>
  </div>
</div>

<!-- S12: DIMENSIONS -->
<div class="sec-color">
  <div class="cnt">
    <h2 class="sec-title">📐 أبعاد وحجم المنتج</h2>
    <div class="dim-grid">
      <div class="dim-imgs">
        <img loading="lazy" src="{dim1}" alt="dimensions">
        <img loading="lazy" src="{dim2}" alt="packaging">
      </div>
      <div class="dim-table">
        <div class="dim-row"><span class="label">الارتفاع</span><span class="value">{dims.get('height','')}</span></div>
        <div class="dim-row"><span class="label">العرض</span><span class="value">{dims.get('width','')}</span></div>
        <div class="dim-row"><span class="label">الوزن</span><span class="value">{dims.get('weight','')}</span></div>
        <div class="dim-row"><span class="label">الحجم</span><span class="value">{dims.get('volume','')}</span></div>
        {f'<div class="dim-note">{dims.get("note","")}</div>' if dims.get('note') else ''}
      </div>
    </div>
  </div>
</div>

<!-- S13: REVIEWS -->
<div class="sec-dark">
  <div class="cnt">
    <h2 class="sec-title">💬 آراء عملائنا الحقيقيين</h2>
    <div class="revs-grid">{revs_html}</div>
  </div>
</div>

<!-- S14: PRICING -->
<div class="sec" id="order">
  <div class="cnt">
    <div class="price-box">
      <h2 class="sec-title">🛒 احصل عليه الآن!</h2>
      <div class="old-p">{pricing.get('original','')} {pricing.get('currency','')}</div>
      <div class="new-p">{pricing.get('discounted','')} {pricing.get('currency','')}</div>
      <div class="dtag">🔥 خصم {pricing.get('discount_percent','')}</div>
      <a href="#" class="btn" style="margin-top:22px;">{cta} ➜</a>
      <div class="g-row"><span>🛡️ ضمان 30 يوم</span><span>🚚 شحن مجاني</span><span>💳 دفع عند الاستلام</span></div>
    </div>
  </div>
</div>

<!-- FAQ -->
<div class="sec">
  <div class="cnt">
    <h2 class="sec-title">❓ الأسئلة الشائعة</h2>
    {faq_html}
  </div>
</div>

<!-- GUARANTEE -->
<div class="sec">
  <div class="cnt">
    <div class="gbox">
      <div style="font-size:3rem;margin-bottom:10px;">🛡️</div>
      <h3>{data.get('guarantee_title','')}</h3>
      <p>{data.get('guarantee_text','')}</p>
    </div>
  </div>
</div>

<!-- S15: FINAL CTA -->
<div class="final">
  <div class="cnt">
    <h2>لا تفوّت هذا العرض الاستثنائي!</h2>
    <p>{data.get('urgency_text','')}</p>
    <a href="#order" class="btn" style="background:#fff;color:{p};max-width:350px;">{cta} ➜</a>
    <p style="margin-top:18px;font-size:.78rem;opacity:.55;">{data.get('footer_text','')}</p>
  </div>
</div>

<script>(function(){{
  var hrs={cdh},key='cd_v3',end=parseInt(localStorage.getItem(key)||0);
  if(!end||end<Date.now()){{end=Date.now()+hrs*3600000;localStorage.setItem(key,end);}}
  function tick(){{
    var l=Math.max(0,end-Date.now());
    var pad=n=>n<10?'0'+n:n;
    var eh=document.getElementById('cd-h'),em=document.getElementById('cd-m'),es=document.getElementById('cd-s');
    if(eh)eh.textContent=pad(Math.floor(l/3600000));
    if(em)em.textContent=pad(Math.floor(l%3600000/60000));
    if(es)es.textContent=pad(Math.floor(l%60000/1000));
    if(l>0)setTimeout(tick,1000);
  }}
  tick();
}})();</script>
</body></html>"""
    return html

# ─── YOUCAN EXPORT ────────────────────────────────────────────────────────────

def generate_youcan_json(html):
    """Wrap HTML in YouCan-compatible page JSON format"""
    import json as _json
    yc_html = get_youcan_html(html)
    page_json = {
        "sections": [
            {
                "id": "custom_html_1",
                "type": "custom_html",
                "settings": {
                    "html": yc_html
                }
            }
        ]
    }
    return _json.dumps(page_json, ensure_ascii=False, indent=2)


def get_youcan_html(html):
    sm = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    style_content = sm.group(1) if sm else ''
    for pat in [r'\*\s*\{[^}]*\}', r'body\s*\{[^}]*\}', r'img\s*\{[^}]*\}', r'\ba\b\s*\{[^}]*\}']:
        style_content = re.sub(pat, '', style_content)
    scoped = ''
    for m in re.finditer(r'(@media[^{]+\{)(.*?)(\})\s*\}', style_content, re.DOTALL):
        inner = ''.join(f'.ali-lp {rm.group(1).strip()}{{{rm.group(2).strip()}}}\n'
                        for rm in re.finditer(r'([^{]+)\{([^}]+)\}', m.group(2)))
    for m in re.finditer(r'((?:[.#\w][^{{@]*?))\{{([^}}]+)\}}', style_content):
        sel = m.group(1).strip(); rules = m.group(2).strip()
        if not sel or not rules or sel.startswith('@'): continue
        scoped += f'.ali-lp {sel}{{{rules}}}\n'
    scoped += '.ali-lp img{max-width:100%;height:auto;display:block;}\n.ali-lp a{text-decoration:none;}\n'
    bm = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    body = bm.group(1) if bm else html
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    for pat in [r'<!DOCTYPE[^>]*>', r'</?(?:html|head|body)[^>]*>', r'<meta[^>]*>', r'<link[^>]*>', r'<style[^>]*>.*?</style>']:
        body = re.sub(pat, '', body, flags=re.DOTALL|re.IGNORECASE)
    body = body.replace(' data-src="', ' src="')
    result = f'<style>\n{scoped}</style>\n<div class="ali-lp" style="direction:rtl;font-family:\'Cairo\',sans-serif;max-width:680px;margin:0 auto;">\n{body.strip()}\n</div>'
    return re.sub(r'\n\s*\n\s*\n', '\n\n', result).strip()

def generate_nb_image(api_key, prompt, ref_b64=None):
    """Generate image using Gemini imagen or fallback to Pollinations"""
    import urllib.request as _ur
    import urllib.parse as _up
    import gc as garbage
    # Try Gemini imagen-3
    try:
        import google.generativeai as _genai
        _genai.configure(api_key=api_key)
        from google.generativeai import GenerativeModel
        # Use imagen via REST
        import requests as _req
        headers = {"Content-Type": "application/json"}
        body = {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
        r = _req.post(url, json=body, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data.get('predictions'):
                b64 = data['predictions'][0].get('bytesBase64Encoded','')
                if b64:
                    return f'data:image/png;base64,{b64}'
    except Exception as e1:
        pass
    # Fallback: Pollinations AI (always works, free)
    try:
        safe_prompt = _up.quote(prompt + ' no text no letters no watermark', safe='')
        seed = random.randint(1, 999999)
        img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=600&nologo=true&nofeed=true&model=flux&seed={seed}"
        with _ur.urlopen(img_url, timeout=25) as resp:
            img_bytes = resp.read()
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        return f'data:image/jpeg;base64,{b64}'
    except Exception as e2:
        return None
with st.sidebar:
      st.header("⚙️ الإعدادات")
      global_api_key        = st.text_input("🔑 Gemini API Key", type="password")
      global_product_name   = st.text_area("📦 اسم وتفاصيل المنتج", placeholder="مثال: نظارات رؤية ليلية للقيادة")
      global_category       = st.selectbox("📁 فئة المنتج", [
          "💄 مستحضرات تجميل وعناية (Cosmetics)",
              "⚙️ أدوات وأجهزة ذكية (Gadgets)",
          "🌿 صحة ومكملات (Health)",
          "👗 أزياء وموضة (Fashion)"
      ])
      uploaded_img = st.file_uploader("📷 صورة المنتج (مرجع AI)", type=["png","jpg","jpeg","webp"])
      product_image_b64 = None
      if uploaded_img:
          product_image_b64 = base64.b64encode(uploaded_img.read()).decode('utf-8')
          uploaded_img.seek(0)
          st.image(uploaded_img, caption="صورة المنتج", )
      st.markdown("---")
      app_mode = st.radio("🛠️ الأداة:", [
          "🏗️ منشئ صفحات الهبوط",
          "🔍 بحث السوق المعمق (SOP-1)",
          "💰 حاسبة التعادل المالي (Matrix)"
      ])

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════
if app_mode == "🏗️ منشئ صفحات الهبوط":
    cols_info = st.columns(5)
    cols_info[0].metric("الأقسام","15")
    cols_info[1].metric("الصور","30+")
    cols_info[2].metric("أطباء","2")
    cols_info[3].metric("خطوات الاستخدام","4")
    cols_info[4].metric("مكونات","4")

    if st.button("🚀 توليد صفحة الهبوط الكاملة (15 قسم + 30 صورة)"):
        if not global_api_key or not global_product_name:
            st.error("الرجاء إدخال مفتاح API واسم المنتج.")
        else:
            with st.spinner("🤖 جاري بناء الصفحة..."):
                try:
                    raw  = generate_lp_json(global_api_key, global_product_name, global_category)
                    try:    data = json.loads(raw)
                    except:
                        fixed = re.sub(r',\s*([}\]])', r'\1', raw)
                        data  = json.loads(fixed)
                    data['_product_name'] = global_product_name
                    colors = detect_colors(global_product_name, global_category)
                    st.session_state.lp_data    = data
                    st.session_state.lp_colors  = colors
                    st.session_state.lp_html    = build_lp_html(data, colors)
                    st.session_state.pop('lp_ai_images', None)
                    st.session_state.pop('lp_html_ai',   None)
                    st.success("🎉 تم! 15 قسم + 30 صورة Pollinations")
                except Exception as e:
                    st.error(f"🛑 {str(e)}")

    if 'lp_html' in st.session_state:
        t1,t2,t3,t4,t5 = st.tabs(["📱 المعاينة","🤖 صور AI","📥 JSON","📤 YouCan","🎨 برومبتات"])

        with t1:
            preview = st.session_state.get('lp_html_ai', st.session_state.lp_html)
            st.download_button("⬇️ تحميل HTML", preview, "landing_page.html", "text/html", key="dl_html_main")
            components.html(preview, height=6000, scrolling=True)

        with t2:
            st.markdown("### 🤖 توليد الصور بـ Gemini AI ودمجها")
            if 'lp_data' not in st.session_state:
                st.warning("ولّد الصفحة أولاً.")
            else:
                slots = extract_image_slots(st.session_state.lp_data)
                c1,c2 = st.columns(2)
                with c1: use_ref = st.checkbox("استخدام صورة المنتج مرجعاً", value=bool(product_image_b64))
                with c2: st.metric("إجمالي الصور", len(slots))

                if st.button("🚀 توليد جميع الصور ودمجها في HTML", key="gen_ai"):
                    if not global_api_key: st.error("أدخل مفتاح API")
                    else:
                        prog = st.progress(0); status = st.empty()
                        generated = {}
                        ref = product_image_b64 if use_ref else None
                        for i, slot in enumerate(slots):
                            status.text(f"⏳ {slot['key']} ({i+1}/{len(slots)})")
                            img_data = generate_nb_image(
                                global_api_key,
                                f"Professional commercial photo. {slot['prompt']}. 8k ultra high quality. no text no letters no words no writing no captions.",
                                ref_b64=ref
                            )
                            generated[slot['key']] = img_data or get_ai_image(slot['keyword'],800,600,slot['type'])
                            prog.progress((i+1)/len(slots))
                            time.sleep(0.4)
                        status.success(f"✅ {len(generated)} صورة!")
                        st.session_state.lp_ai_images = generated
                        new_html = build_lp_html(st.session_state.lp_data, st.session_state.lp_colors, image_map=generated)
                        st.session_state.lp_html_ai = new_html
                        st.success("✅ الصور مدمجة في HTML كـ base64!")
                        st.download_button("⬇️ HTML + صور AI مدمجة", new_html, "lp_ai.html", "text/html", key="dl_ai_html")

                if 'lp_ai_images' in st.session_state:
                    st.markdown("#### 🖼️ الصور المولدة")
                    cols3 = st.columns(3)
                    for i,(k,v) in enumerate(st.session_state.lp_ai_images.items()):
                        with cols3[i%3]:
                            if v and v.startswith('data:'): st.image(v, caption=k)
                            else: st.caption(f"**{k}**: Pollinations")

        with t3:
            if 'lp_data' in st.session_state:
                d = {k:v for k,v in st.session_state.lp_data.items() if k!='_product_name'}
                js = json.dumps(d, ensure_ascii=False, indent=2)
                st.download_button("📥 تحميل JSON", js, "lp.json","application/json", key="dl_lp_json")
                st.json(d)

        with t4:
            src = st.session_state.get('lp_html_ai', st.session_state.lp_html)
            yc = get_youcan_html(src)
            st.download_button("📥 تحميل YouCan JSON", generate_youcan_json(src), "youcan_page.lp", "application/json", key="yc_json_dl")
            if 'lp_html_ai' in st.session_state:
                st.success("✅ صور AI مدمجة base64 — جاهز لـ YouCan!")
            else:
                st.info("💡 ولّد صور AI أولاً لدمجها.")

            section_map = {
                'S1':'📌 TOPBAR','S2':'🏠 Hero','S3':'📊 Stats','S4':'😟 المشكلة',
                'S5':'✅ الحل','S6':'🔄 قبل/بعد','S7':'👨‍⚕️ الأطباء','S8':'👨‍👩‍👧 الثقة',
                'S9':'⭐ المميزات','S10':'🌿 المكونات','S11':'📋 طريقة الاستخدام',
                'S12':'📐 الأبعاد','S13':'💬 المراجعات','S14':'💰 التسعير','S15':'🚀 Final CTA',
                'FAQ':'❓ FAQ','GUARANTEE':'🛡️ الضمان',
            }
            sm2 = re.search(r'(<style>.*?</style>)', yc, re.DOTALL)
            if sm2:
                with st.expander("🎨 CSS (انسخ أولاً)", expanded=False):
                    st.code(sm2.group(1), language='html')
            parts = re.split(r'(<!--\s*S\d+[^>]*-->)', yc)
            cur = 'START'
            for part in parts:
                cm = re.match(r'<!--\s*(S\d+|FAQ|GUARANTEE)', part.strip())
                if cm: cur = cm.group(1); continue
                content = part.strip()
                if not content or content.startswith('<style'): continue
                label = section_map.get(cur, f'📦 {cur}')
                with st.expander(label, expanded=False):
                    st.code(content, language='html')
            st.download_button("📥 YouCan HTML كامل", yc, "youcan.html","text/html")
                        # YouCan JSON Export
            yc_json = generate_youcan_json(src)
            st.download_button("📥 YouCan JSON (استيراد مباشر)", yc_json, "youcan_page.lp", "application/json", key="yc_html_dl")

        with t5:
            if 'lp_data' in st.session_state:
                slots = extract_image_slots(st.session_state.lp_data)
                st.markdown(f"### 🎨 {len(slots)} برومبت صورة")
                for slot in slots:
                    with st.expander(f"🖼️ {slot['key']} — {slot['section']}"):
                        st.code(slot['prompt'])
                        st.caption(f"Type: {slot['type']} | Keyword: {slot['keyword']}")
                st.download_button("📥 CSV", pd.DataFrame(slots).to_csv(index=False), "prompts.csv","text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# SOP-1
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "🔍 بحث السوق المعمق (SOP-1)":
    st.markdown("### 🔍 البحث العميق في السوق")
    if st.button("🧠 استخراج وثائق البيع"):
        if not global_api_key or not global_product_name:
            st.error("أدخل مفتاح API واسم المنتج.")
        else:
            with st.spinner("جاري البحث..."):
                try:
                    res = generate_deep_research(global_api_key, global_product_name, global_category)
                    st.session_state.deep_res = res
                    st.success("✅ اكتمل!")
                except Exception as e:
                    st.error(f"🛑 {str(e)}")
    if 'deep_res' in st.session_state:
        st.markdown(st.session_state.deep_res)
        st.download_button("📥 تحميل التقرير", st.session_state.deep_res, "deep_research.md","text/markdown")

# ══════════════════════════════════════════════════════════════════════════════
# MATRIX
# ══════════════════════════════════════════════════════════════════════════════
elif app_mode == "💰 حاسبة التعادل المالي (Matrix)":
    st.markdown("### 💰 حاسبة التعادل المالي")
    c1,c2 = st.columns(2)
    with c1:
        cost  = st.number_input("💵 تكلفة المنتج",        min_value=0.0, value=50.0,  step=1.0)
        price = st.number_input("🏷️ سعر البيع",            min_value=0.0, value=199.0, step=1.0)
        cod   = st.number_input("🚚 رسوم COD/التوصيل",    min_value=0.0, value=20.0,  step=1.0)
        ret   = st.slider("↩️ نسبة الإرجاع (%)", 0, 100, 20)
    with c2:
        budget= st.number_input("📢 ميزانية الإعلان (يومي)", min_value=0.0, value=100.0, step=5.0)
        cpc   = st.number_input("👆 تكلفة النقرة CPC",       min_value=0.01, value=0.5,  step=0.01)
        cvr   = st.slider("🎯 معدل التحويل (%)", 0.1, 20.0, 2.0, step=0.1)
    if st.button("📊 احسب"):
        clicks    = budget/cpc
        orders    = clicks*(cvr/100)
        returned  = orders*(ret/100)
        fulfilled = orders-returned
        revenue   = fulfilled*price
        total_c   = orders*cost + orders*cod + budget
        profit    = revenue-total_c
        roas      = revenue/budget if budget>0 else 0
        cpa       = budget/orders  if orders>0 else 0
        margin    = profit/revenue*100 if revenue>0 else 0
        st.markdown("---")
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("🛒 الطلبات",f"{orders:.0f}")
        m2.metric("✅ المنفذة", f"{fulfilled:.0f}")
        m3.metric("💰 الإيراد", f"{revenue:.0f}")
        m4.metric("📈 الربح",   f"{profit:.0f}", delta="✅ ربح" if profit>0 else "❌ خسارة")
        st.markdown("---")
        r1,r2,r3,r4 = st.columns(4)
        r1.metric("🎯 ROAS",      f"{roas:.2f}x")
        r2.metric("💸 CPA",       f"{cpa:.2f}")
        r3.metric("📉 هامش الربح",f"{margin:.1f}%")
        r4.metric("↩️ المرتجعة",  f"{returned:.0f}")
        if profit>0: st.success(f"✅ مربحة! ربح {profit:.2f} مقابل إنفاق {budget:.0f}")
        else:        st.error(f"❌ خاسرة! خسارة {abs(profit):.2f}")
        with st.expander("📊 تفاصيل"):
            st.write(f"- نقرات: {clicks:.0f} | طلبات: {orders:.0f} | منفذة: {fulfilled:.0f}")
            st.write(f"- تكلفة بضاعة: {orders*cost:.0f} | COD: {orders*cod:.0f} | إعلان: {budget:.0f}")
            st.write(f"- إجمالي تكاليف: {total_c:.0f} | إيراد: {revenue:.0f} | ربح: {profit:.0f}")
