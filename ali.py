import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import pandas as pd

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Ultimate Structure", layout="wide", page_icon="🏗️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stMetric { background-color: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🚀 ALI Growth Engine (الإصدار الشامل)</h1><p style="color:#94a3b8; margin:0;">بناء صفحات الهبوط + حاسبة التحليل المالي والمصفوفة</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: القوالب الهيكلية الشاملة (بدون صور AI عشوائية)
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 💄 قالب مستحضرات التجميل (Cosmetics)
    # ---------------------------------------------------------
    "Cosmetics": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            :root { --primary: {{COLOR_PRIMARY}}; --secondary: {{COLOR_SECONDARY}}; --accent: {{COLOR_ACCENT}}; }
            body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }
            .bg-primary { background-color: var(--primary); }
            .text-primary { color: var(--primary); }
            .bg-accent { background-color: var(--accent); }
            .text-accent { color: var(--accent); }
            section { padding: 3rem 1.5rem; }
            .placeholder-box { background-color: #e5e7eb; border: 2px dashed #9ca3af; display: flex; align-items: center; justify-content: center; color: #6b7280; font-weight: bold; text-align: center; flex-direction: column;}
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            
            <!-- Trust Bar -->
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span><span>🔒 الدفع عند الاستلام</span>
            </div>

            <!-- Hero Section -->
            <section class="!p-0 relative w-full bg-gray-100">
                <!-- مكان صورة/فيديو المنتج الرئيسي -->
                <div class="w-full h-[500px] placeholder-box">
                    <span class="text-4xl mb-2">📸/🎥</span>
                    <span>ضع صورة أو فيديو المنتج الرائع هنا</span>
                    <span class="text-xs font-normal mt-1">(مثال: 800x1000 px)</span>
                </div>
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <h1 class="text-4xl font-black mb-3 leading-tight drop-shadow-md">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6 drop-shadow">{{HERO_SUB}}</p>
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-lg transition transform hover:scale-105">{{CTA_BUTTON}}</a>
                </div>
            </section>

            <!-- Problem Section (Agitation) -->
            <section class="bg-white text-center border-b border-gray-100">
                <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
                <div class="w-full h-56 rounded-2xl mb-5 placeholder-box bg-red-50 border-red-200 text-red-400">
                    <span class="text-3xl mb-2">😟</span>
                    <span>ضع صورة GIF متحركة توضح ألم العميل</span>
                </div>
                <p class="text-lg font-bold text-gray-700 leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>

            <!-- Solution Section -->
            <section class="bg-primary text-white text-center relative z-20">
                <h2 class="text-3xl font-black text-accent mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-bold mb-6 text-gray-100">{{SOLUTION_DESC}}</p>
                <div class="w-full h-64 rounded-2xl border-4 border-white placeholder-box bg-green-50 text-green-500">
                    <span class="text-3xl mb-2">😍</span>
                    <span>صورة/GIF للعميل وهو سعيد بالنتائج</span>
                </div>
            </section>

            <!-- Before & After Section -->
            <section class="bg-gray-50 text-center border-b border-gray-200">
                <h2 class="text-3xl font-black text-gray-900 mb-6">تحول مذهل تلاحظه فوراً!</h2>
                <div class="flex gap-2 relative">
                    <div class="w-1/2 relative placeholder-box h-48 rounded-r-2xl border-red-300 bg-red-50">
                        <span class="text-red-400">صورة قبل</span>
                        <div class="absolute bottom-2 right-2 bg-red-600 text-white px-2 py-1 text-xs font-bold rounded">قبل</div>
                    </div>
                    <div class="w-1/2 relative placeholder-box h-48 rounded-l-2xl border-green-300 bg-green-50">
                        <span class="text-green-500">صورة بعد</span>
                        <div class="absolute bottom-2 left-2 bg-green-600 text-white px-2 py-1 text-xs font-bold rounded">بعد</div>
                    </div>
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-accent text-white w-10 h-10 flex items-center justify-center rounded-full border-4 border-white shadow-lg font-black text-xl z-10">></div>
                </div>
            </section>

            <!-- Video Reviews (UGC) -->
            <section class="bg-white border-b border-gray-200 text-center">
                <h2 class="text-3xl font-black text-primary mb-2">شاهد تجارب عملائنا</h2>
                <p class="text-gray-500 font-bold mb-8">لا تأخذ كلمتنا، شاهد الفيديوهات بنفسك!</p>
                <div class="flex gap-3 overflow-x-auto pb-4 snap-x">
                    <!-- YouTube Video 1 -->
                    <div class="min-w-[80%] snap-center">
                        <div class="w-full h-64 bg-gray-200 rounded-xl overflow-hidden relative shadow-md">
                            <!-- استبدل هذا الكود بكود تضمين يوتيوب الخاص بك -->
                            <iframe class="w-full h-full absolute top-0 left-0" src="https://www.youtube.com/embed/dQw4w9WgXcQ?controls=0" title="Review Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                        </div>
                    </div>
                    <!-- YouTube Video 2 -->
                    <div class="min-w-[80%] snap-center">
                        <div class="w-full h-64 bg-gray-200 rounded-xl overflow-hidden relative shadow-md placeholder-box">
                            <span class="text-red-500 text-4xl mb-2">▶️</span>
                            <span>ضع فيديو المراجعة الثاني هنا</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Ingredients & Features -->
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">السر في مكوناتنا</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{DYNAMIC_SECTION_HTML}}
                </div>
            </section>

            <!-- Text Reviews -->
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">آراء العملاء</h2>
                <div class="space-y-4">
                    {{REVIEWS_HTML}}
                </div>
            </section>

            <!-- FAQ -->
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ الأسئلة الشائعة</h2>
                <div class="space-y-3 text-right">
                    {{FAQ_HTML}}
                </div>
            </section>

            <!-- Guarantee -->
            <section class="bg-primary text-center pb-20 text-white rounded-t-3xl mt-4">
                <div class="text-6xl mb-4 drop-shadow-lg">🛡️</div>
                <h3 class="text-3xl font-black text-accent mb-4">{{GUARANTEE_TITLE}}</h3>
                <p class="text-lg font-bold text-gray-100">{{GUARANTEE_TEXT}}</p>
            </section>

            <!-- Sticky CTA -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3">
                        <span>🛒</span> {{CTA_BUTTON}}
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """,

    # ---------------------------------------------------------
    # ⚙️ قالب الأدوات والأجهزة الذكية (Gadgets)
    # ---------------------------------------------------------
    "Gadgets": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            :root { --primary: {{COLOR_PRIMARY}}; --secondary: {{COLOR_SECONDARY}}; --accent: {{COLOR_ACCENT}}; }
            body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }
            .bg-primary { background-color: var(--primary); }
            .text-primary { color: var(--primary); }
            .bg-accent { background-color: var(--accent); }
            .text-accent { color: var(--accent); }
            section { padding: 3rem 1.5rem; }
            .no-pad { padding: 0 !important; }
            .placeholder-box { background-color: #e5e7eb; border: 2px dashed #9ca3af; display: flex; align-items: center; justify-content: center; color: #6b7280; font-weight: bold; text-align: center; flex-direction: column;}
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            
            <!-- Trust Bar -->
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold flex justify-center gap-4">
                <span>🚚 توصيل سريع </span><span>🔒 جودة مضمونة</span>
            </div>

            <!-- Hero Section -->
            <section class="no-pad relative w-full bg-gray-900">
                <div class="w-full h-[500px] placeholder-box border-none !bg-gray-800 !text-gray-400">
                    <span class="text-4xl mb-2">📸/🎥</span>
                    <span>صورة أو فيديو الأداة وهي تعمل</span>
                </div>
                <div class="absolute bottom-0 left-0 w-full h-3/4 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <h1 class="text-4xl font-black mb-3 leading-tight drop-shadow-md">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 mb-6 drop-shadow">{{HERO_SUB}}</p>
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-lg transition transform hover:scale-105">{{CTA_BUTTON}}</a>
                </div>
            </section>

            <!-- Problem Section -->
            <section class="bg-white text-center border-b border-gray-100">
                <h2 class="text-2xl font-black mb-5 text-red-600">⚠️ {{PROBLEM_TITLE}}</h2>
                <div class="w-full h-56 rounded-2xl mb-5 placeholder-box bg-red-50 border-red-200">
                    <span>صورة للمشكلة اليومية بدون الأداة</span>
                </div>
                <p class="text-lg font-bold text-gray-700 leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>

            <!-- Solution Section -->
            <section class="bg-primary text-white text-center relative z-20">
                <h2 class="text-3xl font-black text-accent mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-bold mb-6 text-gray-100">{{SOLUTION_DESC}}</p>
                <div class="w-full h-64 rounded-2xl border-4 border-white placeholder-box text-gray-700">
                    <span>GIF / فيديو يوضح سهولة الأداة</span>
                </div>
            </section>

            <!-- Dimensions & Specs (مهم جداً للـ Gadgets) -->
            <section class="bg-gray-100 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-6">⚙️ المقاسات والمواصفات</h2>
                <div class="flex flex-col gap-4">
                    <div class="w-full h-48 rounded-xl placeholder-box bg-white">
                        <span>صورة توضيحية للمقاسات أو الأبعاد</span>
                    </div>
                    <ul class="space-y-3 bg-white p-4 rounded-xl shadow-sm border border-gray-200 text-right">
                        {{DIMENSIONS_HTML}}
                    </ul>
                </div>
            </section>

            <!-- How it works (Steps) -->
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-primary mb-8">سهولة تامة في الاستخدام</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{DYNAMIC_SECTION_HTML}}
                </div>
            </section>

            <!-- Video Reviews (UGC) -->
            <section class="bg-gray-50 border-b border-gray-200 text-center">
                <h2 class="text-3xl font-black text-primary mb-2">تجارب عملائنا المباشرة</h2>
                <p class="text-gray-500 font-bold mb-6">شاهد المنتج وهو يعمل على أرض الواقع</p>
                <div class="space-y-4">
                    <!-- YouTube Video 1 -->
                    <div class="w-full h-56 bg-gray-200 rounded-xl overflow-hidden relative shadow-md placeholder-box">
                        <span class="text-red-500 text-4xl mb-2">▶️</span>
                        <span>ضع رابط فيديو يوتيوب هنا</span>
                    </div>
                    <!-- YouTube Video 2 -->
                    <div class="w-full h-56 bg-gray-200 rounded-xl overflow-hidden relative shadow-md placeholder-box">
                        <span class="text-red-500 text-4xl mb-2">▶️</span>
                        <span>ضع رابط فيديو يوتيوب آخر هنا</span>
                    </div>
                </div>
            </section>

            <!-- Text Reviews -->
            <section class="bg-white border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">التقييمات الكتابية</h2>
                <div class="space-y-4">
                    {{REVIEWS_HTML}}
                </div>
            </section>

            <!-- FAQ -->
            <section class="bg-gray-50 border-b border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ أسئلة متكررة</h2>
                <div class="space-y-3 text-right">
                    {{FAQ_HTML}}
                </div>
            </section>

            <!-- Guarantee -->
            <section class="bg-primary text-center pb-20 text-white rounded-t-3xl mt-4">
                <div class="text-6xl mb-4">🛡️</div>
                <h3 class="text-3xl font-black text-accent mb-4">{{GUARANTEE_TITLE}}</h3>
                <p class="text-lg font-bold text-gray-100">{{GUARANTEE_TEXT}}</p>
            </section>

            <!-- Sticky CTA -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-15px_30px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-6 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-3">
                        <span>🛒</span> {{CTA_BUTTON}}
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي لإنشاء الهيكلة والمحتوى
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
    except: pass
    st.session_state.valid_model_name = "gemini-pro"
    return "gemini-pro"

def generate_landing_page_json(api_key, product, category):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    أنت أعظم خبير كتابة نصوص بيعية (Copywriter) لصفحات الهبوط الموجهة للوطن العربي.
    المنتج: "{product}". 
    الفئة: {"مستحضرات تجميل وعناية" if "Cosmetics" in category else "أدوات وأجهزة ذكية"}.
    
    المطلوب: توليد نصوص قوية ومقنعة جداً تأخذ العميل خطوة بخطوة نحو الشراء.
    النصوص يجب أن تكون بـ "العربية الفصحى" حصراً، وبأسلوب مباشر يخاطب رغبات العميل.

    رد بصيغة JSON صالحة بهذا الهيكل:
    {{
        "hero_headline": "عنوان رئيسي يخطف الانتباه",
        "hero_subheadline": "عنوان فرعي يقدم وعداً بالحل",
        "problem_title": "عنوان قسم الألم (مثال: هل تعاني من..)",
        "problem_description": "فقرة تصف الإحباط أو المشكلة بدقة",
        "solution_title": "عنوان قسم الحل",
        "solution_description": "فقرة تشرح كيف يقدم المنتج الحل الجذري",
        "dynamic_items": [
            {{"title": "اسم ميزة أو مكون 1", "desc": "فائدة هذه الميزة للعميل"}},
            {{"title": "اسم ميزة أو مكون 2", "desc": "فائدة هذه الميزة للعميل"}},
            {{"title": "اسم ميزة أو مكون 3", "desc": "فائدة هذه الميزة للعميل"}}
        ],
        "dimensions": [
            "الطول: .. سم", "الوزن: .. جرام", "الخامة: .."
        ],
        "reviews": [
            {{"name": "سارة م.", "rating": 5, "comment": "تعليق واقعي وحقيقي جداً"}},
            {{"name": "أحمد ع.", "rating": 5, "comment": "تعليق يثني على الجودة والسرعة"}}
        ],
        "faq": [
            {{"q": "متى سألاحظ النتائج؟", "a": "إجابة مقنعة وواضحة"}},
            {{"q": "هل يوجد ضمان؟", "a": "نعم، نقدم ضمان..."}}
        ],
        "guarantee_title": "عنوان الضمان القوي",
        "guarantee_text": "نص تفصيلي للضمان يزيل أي شك لدى المشتري",
        "call_to_action": "نص زر الشراء (مثال: أضف للسلة الآن)"
    }}
    """
    
    response = model.generate_content(prompt, request_options={"timeout": 45.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

# ==========================================================
# 💉 الخطوة 3: تجميع وبناء صفحة الـ HTML
# ==========================================================
def inject_data_into_template(json_data, category, colors):
    template_key = "Cosmetics" if "Cosmetics" in category else "Gadgets"
    final_html = TEMPLATES[template_key]
    
    # 1. القسم الديناميكي (الميزات/المكونات/الخطوات)
    dynamic_html = ""
    for item in json_data.get('dynamic_items', [])[:3]:
        title = item.get('title', '')
        desc = item.get('desc', '')
        dynamic_html += f'''
        <div class="bg-white p-5 rounded-2xl border border-gray-100 flex items-start gap-4 text-right shadow-sm">
            <div class="w-12 h-12 rounded-full bg-blue-50 text-blue-500 flex items-center justify-center flex-shrink-0 text-xl font-black border border-blue-100">✓</div>
            <div>
                <h4 class="font-black text-gray-900 text-lg mb-1">{title}</h4>
                <p class="text-sm font-bold text-gray-600 leading-relaxed">{desc}</p>
            </div>
        </div>'''

    # 2. المقاسات (خاص بـ Gadgets)
    dimensions_html = ""
    for dim in json_data.get('dimensions', ["أبعاد المنتج", "وزن خفيف", "مواد عالية الجودة"])[:4]:
        dimensions_html += f'''
        <li class="flex items-center gap-3 font-bold text-gray-700">
            <span class="text-accent text-xl">📏</span> {dim}
        </li>'''

    # 3. التقييمات
    reviews_html = ""
    for rev in json_data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        reviews_html += f'''
        <div class="bg-gray-50 p-5 rounded-2xl border border-gray-100 shadow-sm text-right">
            <div class="flex justify-between items-center mb-2">
                <span class="font-black text-primary">{rev.get('name')}</span>
                <span class="text-accent text-sm tracking-tighter">{stars}</span>
            </div>
            <p class="text-gray-700 font-bold italic leading-relaxed text-sm">"{rev.get('comment')}"</p>
            <div class="mt-3 text-xs text-green-600 font-black flex items-center gap-1">
                <span>✅</span> مشتري موثق
            </div>
        </div>'''

    # 4. الأسئلة الشائعة
    faq_html = ""
    for faq in json_data.get('faq', [])[:4]:
        faq_html += f'''
        <details class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 group cursor-pointer mb-2">
            <summary class="font-black text-gray-900 text-base flex justify-between items-center outline-none">
                {faq.get('q')}
                <span class="text-accent group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <p class="text-gray-600 text-sm font-bold mt-3 border-t pt-3 border-gray-100">{faq.get('a')}</p>
        </details>'''

    # حقن كل المكونات في القالب
    final_html = final_html.replace("{{DYNAMIC_SECTION_HTML}}", dynamic_html)
    final_html = final_html.replace("{{DIMENSIONS_HTML}}", dimensions_html)
    final_html = final_html.replace("{{REVIEWS_HTML}}", reviews_html)
    final_html = final_html.replace("{{FAQ_HTML}}", faq_html)
    
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", ""))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", ""))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", ""))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", ""))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", ""))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", ""))
    
    final_html = final_html.replace("{{GUARANTEE_TITLE}}", json_data.get("guarantee_title", "ضمان الجودة"))
    final_html = final_html.replace("{{GUARANTEE_TEXT}}", json_data.get("guarantee_text", ""))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن"))
    
    return final_html

# ==========================================================
# 🎛️ واجهة المستخدم والقائمة الجانبية للتنقل
# ==========================================================
with st.sidebar:
    st.header("⚙️ القائمة الرئيسية")
    app_mode = st.radio("اختر الأداة:", ["🏗️ منشئ صفحات الهبوط", "💰 حاسبة التعادل المالي (Matrix)"])
    st.markdown("---")

if app_mode == "🏗️ منشئ صفحات الهبوط":
    with st.sidebar:
        st.subheader("إعدادات صفحة الهبوط")
        api_key = st.text_input("🔑 Gemini API Key", type="password")
        product_name = st.text_area("📦 تفاصيل المنتج", placeholder="مثال: جهاز تنظيف الوجه الحديث، أو سيروم للشعر.")
        product_category = st.selectbox("📦 الفئة (تحدد هيكل الصفحة)", ["💄 مستحضرات تجميل وعناية (Cosmetics)", "⚙️ أدوات وأجهزة ذكية (Gadgets)"])

        st.subheader("🎨 الألوان")
        col1, col2 = st.columns(2)
        with col1: color_primary = st.color_picker("أساسي", "#0f766e" if "Cosmetics" in product_category else "#1f2937")
        with col2: color_accent = st.color_picker("الزر", "#eab308" if "Cosmetics" in product_category else "#ef4444")
        color_secondary = st.color_picker("ثانوي", "#f8fafc")
        colors_dict = {'primary': color_primary, 'secondary': color_secondary, 'accent': color_accent}
        
        start_btn = st.button("🚀 توليد بنية الصفحة (محتوى + هيكل)", use_container_width=True)

    if start_btn:
        if not api_key or not product_name:
            st.error("أدخل المفتاح ووصف المنتج.")
        else:
            with st.spinner("🤖 جاري بناء الهيكلة وكتابة المحتوى التسويقي الجبار..."):
                try:
                    raw_json = generate_landing_page_json(api_key, product_name, product_category)
                    parsed_data = json.loads(raw_json)
                    st.session_state.final_page = inject_data_into_template(parsed_data, product_category, colors_dict)
                    st.session_state.json_data = parsed_data
                    st.success("🎉 نجاح! تم بناء الهيكل بالكامل. الصناديق جاهزة لاستقبال صورك.")
                except Exception as e:
                    st.error(f"🛑 خطأ: {str(e)}")

    if 'final_page' in st.session_state:
        tab1, tab2 = st.tabs(["📱 المعاينة البصرية", "💻 كود HTML (ضعه في متجرك)"])
        with tab1:
            st.info("💡 الأماكن الرمادية تمثل المساحات المصممة خصيصاً لوضع صورك وفيديوهاتك الحقيقية. تم تصميمها لترفع نسبة التحويل (CR) لأقصى حد.")
            components.html(st.session_state.final_page, height=1200, scrolling=True)
        with tab2:
            st.write("انسخ الكود، ضعه في متجرك (Youcan أو Shopify)، واستبدل فقط الصناديق بصورك وفيديوهات المراجعات.")
            st.code(st.session_state.final_page, language="html")

# ==========================================================
# 💰 القسم الجديد: حاسبة التعادل والمصفوفة المالية
# ==========================================================
elif app_mode == "💰 حاسبة التعادل المالي (Matrix)":
    st.subheader("💰 حاسبة نقطة التعادل والمصفوفة المالية (Break-Even Matrix)")
    st.write("هذه الأداة تغنيك عن ملفات الإكسل المعقدة. أدخل أرقامك لتعرف أقصى تكلفة يمكنك دفعها للإعلان دون التعرض لخسارة.")
    
    st.markdown("---")
    
    # 1. إدخال البيانات المالية
    col1, col2, col3 = st.columns(3)
    P = col1.number_input("سعر بيع المنتج للعميل (P)", value=200.0, step=10.0)
    C = col2.number_input("تكلفة المنتج + التوصيل (C)", value=80.0, step=5.0)
    actual_cpl = col3.number_input("تكلفة الليد الحالية في مدير الإعلانات (CPL)", value=20.0, step=1.0)

    # 2. إدخال نسب الأداء
    st.write("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    CR_percent = col4.slider("نسبة التأكيد (Confirmation Rate - CR) %", min_value=10, max_value=100, value=60)
    DR_percent = col5.slider("نسبة التسليم (Delivery Rate - DR) %", min_value=10, max_value=100, value=55)
    
    CR = CR_percent / 100.0
    DR = DR_percent / 100.0

    # 3. الحسابات
    gross_margin = P - C
    max_cpl = gross_margin * CR * DR
    max_cpa = gross_margin * DR
    profit_per_lead = max_cpl - actual_cpl

    # 4. عرض المؤشرات (KPIs)
    st.markdown("---")
    st.markdown("### 📊 المؤشرات الحيوية (KPIs)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("هامش الربح الإجمالي", f"{gross_margin:.2f}")
    m2.metric("أقصى تكلفة لليد (Max CPL)", f"{max_cpl:.2f}")
    m3.metric("أقصى تكلفة للمبيعة (Max CPA)", f"{max_cpa:.2f}")

    if profit_per_lead >= 0:
        m4.metric("حالة إعلانك الحالي", "✅ رابح", f"+ {profit_per_lead:.2f} ربح صافي لكل ليد")
    else:
        m4.metric("حالة إعلانك الحالي", "🚨 خاسر", f"{profit_per_lead:.2f} خسارة في كل ليد")

    # 5. مصفوفة الحساسية (Max CPL Matrix)
    st.markdown("---")
    st.markdown("### 🧮 مصفوفة الحساسية (Max CPL Matrix)")
    st.info("الجدول أدناه يوضح لك أقصى سعر ليد (Max CPL) يمكنك دفعه بناءً على تغير نسب التأكيد والتسليم. **(الأعمدة: التسليم DR، الصفوف: التأكيد CR)**")

    # بناء المصفوفة
    dr_list = [x/100.0 for x in range(30, 100, 5)]
    cr_list = [x/100.0 for x in range(30, 100, 5)]

    matrix_data = []
    for cr_val in cr_list:
        row = {'CR \\ DR': f"{int(cr_val*100)}%"}
        for dr_val in dr_list:
            row[f"{int(dr_val*100)}%"] = round(gross_margin * cr_val * dr_val, 2)
        matrix_data.append(row)

    df_matrix = pd.DataFrame(matrix_data)
    
    # عرض الجدول ملوناً تلقائياً
    st.dataframe(
        df_matrix.style.background_gradient(cmap='RdYlGn', subset=df_matrix.columns[1:]),
        use_container_width=True,
        hide_index=True
    )
