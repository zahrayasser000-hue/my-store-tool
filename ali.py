import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re
import urllib.parse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - AI Visual Ultimate", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>💎 ALI Growth Engine (نظام الإنفوجرافيك + الذكاء الصوري)</h1><p style="color:#94a3b8; margin:0;">صفحات هبوط مدججة بالصور المولدة تلقائياً، مع آراء العملاء والأسئلة الشائعة</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: نظام القوالب المتعددة
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 🌟 القالب البصري الشامل (Infographic Style) - مطور بالكامل
    # ---------------------------------------------------------
    "💎 الشامل (إنفوجرافيك - صور تلقائية، مراجعات، و FAQ)": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: {{COLOR_PRIMARY}};
                --secondary: {{COLOR_SECONDARY}};
                --accent: {{COLOR_ACCENT}};
            }
            body { font-family: 'Cairo', sans-serif; background-color: #e5e7eb; scroll-behavior: smooth; }
            .bg-primary { background-color: var(--primary); }
            .bg-secondary { background-color: var(--secondary); }
            .bg-accent { background-color: var(--accent); }
            .text-primary { color: var(--primary); }
            .text-accent { color: var(--accent); }
            .border-primary { border-color: var(--primary); }
            .border-accent { border-color: var(--accent); }
            
            section { padding: 0; margin: 0; position: relative; }
            .content-pad { padding: 3rem 1.5rem; }
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            
            <!-- 1. شريط الثقة العلوي -->
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold tracking-wide flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span>
                <span>🔒 دفع آمن 100%</span>
            </div>

            <!-- 2. Hero Section -->
            <section class="relative w-full">
                <!-- صورة ذكية مولدة تلقائياً -->
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_HERO}}?width=800&height=1000&nologo=true" alt="Hero" class="w-full h-[500px] object-cover">
                <div class="absolute bottom-0 left-0 w-full h-2/3 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <div class="inline-block bg-accent text-white px-3 py-1 rounded-full text-xs font-black mb-3 shadow-lg animate-pulse">عرض حصري</div>
                    <h1 class="text-3xl md:text-4xl font-black mb-2 drop-shadow-md leading-tight">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 drop-shadow mb-4">{{HERO_SUB}}</p>
                </div>
            </section>

            <!-- 3. Problem Section -->
            <section class="bg-primary text-white text-center pb-8 pt-4 px-4 rounded-b-3xl shadow-md z-20 relative">
                <h2 class="text-2xl font-black mb-4 text-accent">⚠️ {{PROBLEM_TITLE}}</h2>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_PROBLEM}}?width=600&height=400&nologo=true" class="w-full h-48 object-cover rounded-2xl border-4 border-white shadow-lg mb-4">
                <p class="text-base font-bold leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>

            <!-- 4. Solution & Mechanism -->
            <section class="content-pad bg-white text-center">
                <h2 class="text-3xl font-black text-primary mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg text-gray-700 font-bold mb-6">{{SOLUTION_DESC}}</p>
                <img src="https://image.pollinations.ai/prompt/{{IMAGE_SOLUTION}}?width=800&height=600&nologo=true" class="w-full h-64 object-cover rounded-2xl shadow-md border border-gray-100 mb-6">
                
                <div class="bg-gray-50 p-5 rounded-2xl border border-gray-200 text-right">
                    <h3 class="font-black text-gray-900 text-xl mb-2">⚙️ {{MECHANISM_TITLE}}</h3>
                    <p class="text-sm font-bold text-gray-600 leading-relaxed">{{MECHANISM_DESC}}</p>
                </div>
            </section>

            <!-- 5. Ingredients Section (المكونات الديناميكية) -->
            <section class="bg-primary text-white content-pad text-center">
                <h2 class="text-3xl font-black text-accent mb-8">السر في مكوناتنا</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{INGREDIENTS_HTML}}
                </div>
            </section>

            <!-- 6. Benefits Grid (الفوائد المرئية) -->
            <section class="content-pad bg-secondary">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">نتائج سريعة ومضمونة</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{BENEFITS_HTML}}
                </div>
            </section>

            <!-- 7. Customer Reviews (آراء العملاء) -->
            <section class="content-pad bg-white border-t border-gray-100">
                <h2 class="text-3xl font-black text-center text-primary mb-8">ماذا يقول عملاؤنا؟</h2>
                <div class="space-y-4">
                    {{REVIEWS_HTML}}
                </div>
            </section>

            <!-- 8. FAQ Section (الأسئلة الشائعة) -->
            <section class="content-pad bg-gray-50 border-t border-gray-200">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">❓ الأسئلة الشائعة</h2>
                <div class="space-y-4 text-right">
                    {{FAQ_HTML}}
                </div>
            </section>

            <!-- 9. Expert & Risk Reversal -->
            <section class="content-pad bg-primary text-center pb-16 text-white">
                <h3 class="text-3xl font-black text-accent mb-4">ضمان ذهبي 100%</h3>
                <p class="text-lg font-bold text-gray-100 mb-8">{{GUARANTEE}}</p>
            </section>

            <!-- Sticky Urgency CTA (الزر العائم) -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-3 shadow-[0_-10px_20px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-4 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <div class="text-gray-800 text-sm font-black mb-2 flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-red-600 animate-ping"></span>
                        العرض ينتهي قريباً! الدفع عند الاستلام
                    </div>
                    <a href="#buy" class="bg-accent hover:opacity-90 text-white font-black py-4 px-4 rounded-xl text-2xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-2">
                        🛒 {{CTA_BUTTON}}
                    </a>
                </div>
            </div>

        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي المعزز بإنشاء الصور والأقسام الجديدة
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

def generate_landing_page_json(api_key, product):
    genai.configure(api_key=api_key, transport="rest")
    model_name = get_fast_working_model(api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    أنت أعظم خبير تسويق لصفحات الهبوط (Infographic Sales Pages).
    المنتج: "{product}".
    
    المطلوب: توليد نصوص قوية ووصف لصور باللغة الإنجليزية لتوليدها بالذكاء الاصطناعي.
    رد حصراً بصيغة JSON صالحة (Valid JSON) بهذا الهيكل الدقيق:
    {{
        "hero_headline": "عنوان رئيسي قصير وصادم",
        "hero_subheadline": "عنوان فرعي يبرز الفائدة",
        "image_hero_prompt": "English prompt for AI image generator showing the product in a beautiful, elegant, professional studio shot. highly detailed",
        "problem_title": "عنوان المشكلة",
        "problem_description": "وصف قصير للمشكلة",
        "image_problem_prompt": "English prompt for AI image showing a person frustrated with the problem, photography, emotional",
        "solution_title": "عنوان الحل",
        "solution_description": "كيف يحل المنتج المشكلة",
        "image_solution_prompt": "English prompt for AI image showing a happy person with perfect results after using the product",
        "mechanism_title": "كيف يعمل؟",
        "mechanism_description": "وصف الآلية باختصار",
        "ingredients": [
            {{"name": "اسم المكون 1", "desc": "فائدة هذا المكون"}}
        ],
        "benefits": ["النتيجة الأولى", "النتيجة الثانية", "توفير الجهد والمال"],
        "reviews": [
            {{"name": "سارة م.", "rating": 5, "comment": "تعليق إيجابي واقعي وقصير"}},
            {{"name": "أمينة ع.", "rating": 5, "comment": "تعليق يركز على سرعة النتيجة"}}
        ],
        "faq": [
            {{"q": "سؤال شائع 1؟", "a": "إجابة مقنعة."}},
            {{"q": "سؤال حول الضمان والتوصيل؟", "a": "إجابة تطمئن العميل."}}
        ],
        "guarantee": "نص ضمان استرجاع الأموال",
        "call_to_action": "نص زر الشراء القصير (مثال: اطلب بخصم 50%)"
    }}
    لا تكتب أي حرف خارج الـ JSON.
    """
    response = model.generate_content(prompt, request_options={"timeout": 30.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن المتقدم (ألوان + نصوص + صور + HTML)
# ==========================================================
def inject_data_into_template(json_data, template_name, colors):
    # 1. تجهيز الفوائد
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        benefits_html += f'''
        <div class="bg-white p-5 rounded-2xl flex items-center gap-4 shadow-sm border-r-4 border-accent">
            <div class="w-10 h-10 flex-shrink-0 bg-green-100 rounded-full flex items-center justify-center">
                <span class="text-xl text-green-600">✓</span>
            </div>
            <p class="font-bold text-gray-800 text-right text-lg">{benefit}</p>
        </div>'''

    # 2. تجهيز المكونات (الآن أصبحت متقدمة مع اسم ووصف)
    ingredients_html = ""
    for ing in json_data.get('ingredients', [])[:3]:
        name = ing.get('name', '')
        desc = ing.get('desc', '')
        # توليد صورة للمكون بناء على اسمه
        ing_prompt = urllib.parse.quote(f"macro photography of {name}, natural, isolated on white background, highly detailed")
        ingredients_html += f'''
        <div class="bg-white/10 backdrop-blur-sm p-4 rounded-2xl border border-white/20 flex items-center gap-4 text-right">
            <img src="https://image.pollinations.ai/prompt/{ing_prompt}?width=200&height=200&nologo=true" class="w-20 h-20 rounded-full shadow-lg border-2 border-accent object-cover">
            <div>
                <h4 class="font-black text-accent text-lg mb-1">{name}</h4>
                <p class="text-sm font-medium text-gray-100">{desc}</p>
            </div>
        </div>'''

    # 3. تجهيز التقييمات (Reviews)
    reviews_html = ""
    for rev in json_data.get('reviews', [])[:3]:
        stars = '⭐' * int(rev.get('rating', 5))
        reviews_html += f'''
        <div class="bg-gray-50 p-5 rounded-2xl border border-gray-200">
            <div class="flex justify-between items-center mb-3">
                <span class="font-black text-primary">{rev.get('name')}</span>
                <span class="text-accent text-sm">{stars}</span>
            </div>
            <p class="text-gray-600 font-medium italic">"{rev.get('comment')}"</p>
            <div class="mt-3 text-xs text-green-600 font-bold flex items-center gap-1">
                <span>✅</span> مشتري موثق
            </div>
        </div>'''

    # 4. تجهيز الأسئلة الشائعة (FAQ)
    faq_html = ""
    for faq in json_data.get('faq', [])[:3]:
        faq_html += f'''
        <div class="bg-white p-5 rounded-2xl shadow-sm border-l-4 border-primary">
            <h4 class="font-black text-gray-900 mb-2 text-lg">❓ {faq.get('q')}</h4>
            <p class="text-gray-700 text-sm font-bold leading-relaxed">{faq.get('a')}</p>
        </div>'''

    # جلب القالب
    final_html = TEMPLATES[template_name]
    
    # حقن الألوان
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    # تجهيز روابط الصور بالذكاء الاصطناعي
    img_hero = urllib.parse.quote(json_data.get("image_hero_prompt", "beautiful product photography"))
    img_prob = urllib.parse.quote(json_data.get("image_problem_prompt", "sad person having a problem"))
    img_sol = urllib.parse.quote(json_data.get("image_solution_prompt", "happy successful person"))

    # الحقن النصي والصوري
    final_html = final_html.replace("{{IMAGE_HERO}}", img_hero)
    final_html = final_html.replace("{{IMAGE_PROBLEM}}", img_prob)
    final_html = final_html.replace("{{IMAGE_SOLUTION}}", img_sol)
    
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", "اكتشف الحل الأمثل"))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", "المنتج الذي سيغير حياتك."))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", "هل تعاني من هذه المشكلة؟"))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", "وصف المشكلة..."))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", "الحل النهائي"))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", "وصف الحل..."))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", "ضمان استرجاع الأموال."))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن"))
    final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)
    final_html = final_html.replace("{{MECHANISM_TITLE}}", json_data.get("mechanism_title", "كيف يعمل؟"))
    final_html = final_html.replace("{{MECHANISM_DESC}}", json_data.get("mechanism_description", "تقنية مبتكرة لحل مشكلتك."))
    
    final_html = final_html.replace("{{INGREDIENTS_HTML}}", ingredients_html)
    final_html = final_html.replace("{{REVIEWS_HTML}}", reviews_html)
    final_html = final_html.replace("{{FAQ_HTML}}", faq_html)
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج", placeholder="مثال: شامبو طبيعي لنمو الشعر")
    
    st.markdown("---")
    st.subheader("🎨 تخصيص ألوان المنتج")
    col1, col2 = st.columns(2)
    with col1:
        color_primary = st.color_picker("اللون الأساسي", "#0f766e")
    with col2:
        color_accent = st.color_picker("لون الزر/التنبيه", "#eab308")
    color_secondary = st.color_picker("اللون الثانوي (خلفيات)", "#f8fafc")
    
    colors_dict = {
        'primary': color_primary,
        'secondary': color_secondary,
        'accent': color_accent
    }
    
    st.markdown("---")
    selected_template = st.selectbox("القوالب المتاحة:", list(TEMPLATES.keys()))
    start_btn = st.button("⚡ توليد الصفحة الذكية", use_container_width=True)
    
    if 'json_data' in st.session_state:
        st.markdown("---")
        change_theme_btn = st.button("🔄 تحديث الألوان/التصميم فقط", use_container_width=True)
        if change_theme_btn:
            st.session_state.final_page = inject_data_into_template(st.session_state.json_data, selected_template, colors_dict)
            st.rerun()

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج أولاً.")
    else:
        with st.spinner("1️⃣ جاري هندسة المحتوى وكتابة أوامر الصور (يستغرق 15 ثانية)..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                with st.spinner("2️⃣ جاري تجميع الصفحة وتوليد الصور تلقائياً..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data, selected_template, colors_dict)
                    st.session_state.json_data = parsed_data
                    st.session_state.current_colors = colors_dict
                    
                st.success("🎉 اكتمل بناء صفحة الإنفوجرافيك الخارقة! انظر التبويبات.")
            except json.JSONDecodeError:
                st.error("⚠️ حدث خطأ في قراءة الاستجابة. المحاولة مرة أخرى ستحلها.")
            except Exception as e:
                st.error(f"🛑 خطأ: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية الحية", "💻 كود HTML للنسخ"])
    
    with tab1:
        st.info("💡 تم توليد الصور تلقائياً بواسطة الذكاء الاصطناعي بناءً على وصف منتجك! (قد تستغرق الصور ثواني للتحميل في أول مرة)")
        components.html(st.session_state.final_page, height=1200, scrolling=True)
        
    with tab2:
        st.write("انسخ هذا الكود بالكامل، ستجد أن روابط الصور قد تم توليدها برمجياً بالفعل.")
        st.code(st.session_state.final_page, language="html")
