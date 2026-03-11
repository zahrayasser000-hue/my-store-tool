import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Infographic Ultimate", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>💎 ALI Growth Engine (نظام الإنفوجرافيك البصري)</h1><p style="color:#94a3b8; margin:0;">صفحات هبوط مدججة بالصور، متوافقة مع ألوان منتجك 100%</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: نظام القوالب المتعددة (مع محرك الألوان الديناميكي)
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 🌟 القالب البصري الشامل (Infographic Style) - مُدجج بالصور
    # ---------------------------------------------------------
    "💎 الشامل (إنفوجرافيك - مدجج بالصور)": """
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
            
            /* إزالة الفراغات لتبدو كصورة إنفوجرافيك واحدة متصلة */
            section { padding: 0; margin: 0; position: relative; }
            .content-pad { padding: 2rem 1.5rem; }
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center">
        
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            
            <!-- 1. شريط الثقة العلوي -->
            <div class="bg-gray-900 text-white text-center py-2 text-xs font-bold tracking-wide flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span>
                <span>🔒 دفع آمن 100%</span>
            </div>

            <!-- 2. Hero Section (صورة كاملة + دمج متدرج) -->
            <section class="relative w-full">
                <!-- استبدل الرابط بصورة المنتج الرئيسية -->
                <img src="https://placehold.co/800x1000/292524/ffffff?text=Main+Hero+Image\n(Product+In+Action)" alt="Hero" class="w-full h-auto object-cover">
                
                <!-- تدرج لوني يدمج الصورة مع القسم التالي -->
                <div class="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-[var(--primary)] to-transparent"></div>
                
                <div class="absolute bottom-0 left-0 w-full p-6 text-white text-center z-10">
                    <div class="inline-block bg-accent text-white px-3 py-1 rounded-full text-xs font-black mb-3 border-2 border-white shadow-lg animate-pulse">حصرياً اليوم</div>
                    <h1 class="text-3xl md:text-4xl font-black mb-2 drop-shadow-md leading-tight">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg font-bold text-gray-100 drop-shadow mb-4">{{HERO_SUB}}</p>
                </div>
            </section>

            <!-- 3. Problem Section (ألم العميل) -->
            <section class="bg-primary text-white text-center pb-8 pt-4 px-4 rounded-b-3xl shadow-md z-20 relative">
                <h2 class="text-2xl font-black mb-4 text-accent">⚠️ {{PROBLEM_TITLE}}</h2>
                <!-- استبدل بصورة GIF للمشكلة -->
                <img src="https://placehold.co/600x400/ef4444/ffffff?text=GIF+Problem\n(Agitation)" class="w-full rounded-2xl border-4 border-white shadow-lg mb-4 object-cover">
                <p class="text-base font-bold">{{PROBLEM_DESC}}</p>
            </section>

            <!-- 4. Before & After (مقارنة بصرية قوية) -->
            <section class="content-pad bg-secondary text-center">
                <h2 class="text-3xl font-black text-gray-900 mb-6 drop-shadow-sm">تحول مذهل تلاحظه فوراً!</h2>
                <div class="flex gap-2 mb-2 relative">
                    <div class="w-1/2 relative">
                        <img src="https://placehold.co/400x500/d1d5db/475569?text=Before" class="w-full h-48 object-cover rounded-r-2xl border-2 border-red-500">
                        <div class="absolute bottom-2 right-2 bg-red-600 text-white px-2 py-1 text-xs font-bold rounded">قبل</div>
                    </div>
                    <div class="w-1/2 relative">
                        <img src="https://placehold.co/400x500/d1d5db/475569?text=After" class="w-full h-48 object-cover rounded-l-2xl border-2 border-green-500">
                        <div class="absolute bottom-2 left-2 bg-green-600 text-white px-2 py-1 text-xs font-bold rounded">بعد</div>
                    </div>
                    <!-- سهم التحول بالمنتصف -->
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-accent text-white w-10 h-10 flex items-center justify-center rounded-full border-4 border-white shadow-lg font-black text-xl z-10">
                        >
                    </div>
                </div>
            </section>

            <!-- 5. Solution & Mechanism (الحل والآلية) -->
            <section class="content-pad bg-white text-center">
                <h2 class="text-3xl font-black text-primary mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg text-gray-700 font-bold mb-6">{{SOLUTION_DESC}}</p>
                <!-- استبدل بصورة الإنفوجرافيك للآلية -->
                <img src="https://placehold.co/800x600/f3f4f6/1e293b?text=Infographic/GIF\n(How+it+works)" class="w-full rounded-2xl shadow-md border border-gray-100 mb-4">
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-200">
                    <h3 class="font-black text-gray-800">⚙️ {{MECHANISM_TITLE}}</h3>
                    <p class="text-sm font-medium text-gray-600">{{MECHANISM_DESC}}</p>
                </div>
            </section>

            <!-- 6. Ingredients / Features (خصائص دائرية مثل صورك) -->
            <section class="bg-primary text-white content-pad text-center">
                <h2 class="text-2xl font-black text-accent mb-8">مكونات/خصائص فائقة</h2>
                <div class="flex justify-center gap-4 flex-wrap">
                    {{INGREDIENTS_HTML}}
                </div>
            </section>

            <!-- 7. Benefits Grid (الفوائد المرئية) -->
            <section class="content-pad bg-secondary">
                <h2 class="text-3xl font-black text-center text-gray-900 mb-8">نتائج سريعة ومضمونة</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{BENEFITS_HTML}}
                </div>
            </section>

            <!-- 8. Authority & Proof (خبير وتقييمات) -->
            <section class="content-pad bg-white border-t-8 border-primary relative overflow-hidden">
                <!-- صورة خلفية خفيفة للشهادة -->
                <div class="absolute -right-10 top-0 opacity-10 text-9xl">❞</div>
                <div class="relative z-10 flex flex-col items-center text-center mb-8">
                    <img src="https://placehold.co/300x300/e2e8f0/64748b?text=Doctor/Expert\nImage" class="w-28 h-28 object-cover rounded-full border-4 border-primary shadow-lg -mt-16 bg-white mb-4">
                    <h4 class="font-black text-primary text-xl">ينصح به الخبراء</h4>
                    <p class="text-base font-bold text-gray-700 italic mt-2">"{{EXPERT_QUOTE}}"</p>
                </div>
                
                <!-- تقييمات العملاء الوهمية (Social Proof) -->
                <img src="https://placehold.co/800x400/f8fafc/334155?text=Customer+Reviews+Collage\n(Images+of+happy+clients)" class="w-full rounded-2xl shadow-sm border border-gray-200">
            </section>

            <!-- 9. Steps (خطوات الاستخدام) -->
            <section class="content-pad bg-gray-900 text-white text-center">
                <h2 class="text-2xl font-black text-accent mb-8">طريقة الاستخدام (بسيطة جداً)</h2>
                <div class="space-y-4 text-right">
                    {{STEPS_HTML}}
                </div>
            </section>

            <!-- 10. Risk Reversal (الضمان) -->
            <section class="content-pad bg-secondary text-center pb-12">
                <img src="https://placehold.co/400x400/fbbf24/854d0e?text=Guarantee\nBadge" class="w-32 h-32 mx-auto object-cover rounded-full shadow-lg border-4 border-white mb-4">
                <h3 class="text-2xl font-black text-gray-900 mb-3">ضمان استرجاع الأموال 100%</h3>
                <p class="text-base font-bold text-gray-700">{{GUARANTEE}}</p>
            </section>

            <!-- Sticky Urgency CTA (الزر العائم) -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-3 shadow-[0_-10px_20px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-2 border-accent">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <div class="text-gray-800 text-xs font-black mb-1 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-red-600 animate-ping"></span>
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
# 🧠 الخطوة 1: المحرك اللفظي
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
    أنت أعظم Copywriter تسويقي لصفحات الهبوط البصرية (Infographic Sales Pages).
    المنتج: "{product}".
    
    المطلوب: توليد نصوص قصيرة جداً، قوية، ومناسبة لتصميم مليء بالصور.
    رد حصراً بصيغة JSON صالحة (Valid JSON) بهذا الهيكل الدقيق:
    {{
        "hero_headline": "عنوان رئيسي قصير وصادم (مثال: وداعاً للشعر الزائد)",
        "hero_subheadline": "عنوان فرعي يبرز النتيجة النهائية",
        "problem_title": "عنوان المشكلة (مثال: هل تعانين من الجروح؟)",
        "problem_description": "وصف المشكلة في سطر واحد",
        "solution_title": "عنوان الحل المبتكر",
        "solution_description": "كيف يحل المنتج المشكلة فوراً",
        "mechanism_title": "عنوان الآلية (كيف يعمل؟)",
        "mechanism_description": "وصف الآلية العلمية أو التقنية للمنتج باختصار",
        "ingredients": ["المكون/الخاصية 1", "المكون/الخاصية 2", "المكون/الخاصية 3"],
        "benefits": ["النتيجة المبهرة الأولى", "النتيجة المبهرة الثانية", "توفير الوقت والمال"],
        "expert_quote": "اقتباس مقنع جداً على لسان خبير أو طبيب",
        "steps": ["الخطوة الأولى: جهزي..", "الخطوة الثانية: استخدمي..", "الخطوة الثالثة: استمتعي.."],
        "guarantee": "نص قصير لضمان استرجاع الأموال",
        "call_to_action": "نص زر الشراء (مثال: اطلب الآن بخصم 50%)"
    }}
    لا تكتب أي حرف خارج الـ JSON.
    """
    response = model.generate_content(prompt, request_options={"timeout": 20.0})
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match: return match.group(0)
    return clean_text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن المتقدم (ألوان + نصوص + HTML)
# ==========================================================
def inject_data_into_template(json_data, template_name, colors):
    # 1. تجهيز الفوائد
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        benefits_html += f'''
        <div class="bg-white p-4 rounded-xl flex items-center gap-4 shadow-sm border border-gray-200">
            <div class="w-12 h-12 flex-shrink-0 bg-secondary rounded-full flex items-center justify-center">
                <span class="text-2xl text-primary">✓</span>
            </div>
            <p class="font-bold text-gray-800 text-right">{benefit}</p>
        </div>'''

    # 2. تجهيز المكونات/الخصائص الدائرية (مثل صورة الشامبو)
    ingredients_html = ""
    ingredients_list = json_data.get('ingredients', ["خاصية 1", "خاصية 2", "خاصية 3"])
    for ing in ingredients_list[:3]:
        ingredients_html += f'''
        <div class="flex flex-col items-center w-[30%]">
            <img src="https://placehold.co/200x200/ffffff/111827?text=Icon" class="w-20 h-20 rounded-full mb-2 shadow-lg border-4 border-accent object-cover">
            <p class="text-sm font-black text-center leading-tight">{ing}</p>
        </div>'''

    # 3. تجهيز الخطوات
    steps_html = ""
    steps_list = json_data.get('steps', ["خطوة 1", "خطوة 2", "خطوة 3"])
    for i, step in enumerate(steps_list[:3], 1):
        steps_html += f'''
        <div class="flex items-center gap-4 bg-gray-800 p-4 rounded-xl border border-gray-700">
            <div class="w-10 h-10 flex items-center justify-center bg-accent text-white font-black rounded-full flex-shrink-0 text-xl shadow-lg">{i}</div>
            <p class="font-bold text-gray-100">{step}</p>
        </div>'''

    # جلب القالب
    final_html = TEMPLATES[template_name]
    
    # حقن الألوان (المحرك الديناميكي)
    final_html = final_html.replace("{{COLOR_PRIMARY}}", colors['primary'])
    final_html = final_html.replace("{{COLOR_SECONDARY}}", colors['secondary'])
    final_html = final_html.replace("{{COLOR_ACCENT}}", colors['accent'])

    # الحقن النصي
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
    final_html = final_html.replace("{{EXPERT_QUOTE}}", json_data.get("expert_quote", "أنصح به بشدة لكل من يبحث عن الجودة."))
    final_html = final_html.replace("{{INGREDIENTS_HTML}}", ingredients_html)
    final_html = final_html.replace("{{STEPS_HTML}}", steps_html)
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج", placeholder="مثال: شامبو طبيعي لنمو الشعر")
    
    st.markdown("---")
    st.subheader("🎨 تخصيص ألوان المنتج")
    st.write("اختر الألوان لكي تتطابق الصفحة مع هوية منتجك:")
    
    col1, col2 = st.columns(2)
    with col1:
        # لون رئيسي (للخلفيات البارزة، مثل الأخضر الغامق للشامبو)
        color_primary = st.color_picker("اللون الأساسي", "#0f766e")
    with col2:
        # لون التنبيهات (للأزرار والعروض، مثل الذهبي أو الأحمر)
        color_accent = st.color_picker("لون الزر/التنبيه", "#eab308")
    
    # لون ثانوي (للخلفيات الفاتحة)
    color_secondary = st.color_picker("اللون الثانوي (خلفيات خفيفة)", "#f1f5f9")
    
    colors_dict = {
        'primary': color_primary,
        'secondary': color_secondary,
        'accent': color_accent
    }
    
    st.markdown("---")
    selected_template = st.selectbox("القوالب المتاحة:", list(TEMPLATES.keys()))
    start_btn = st.button("⚡ توليد / تحديث الصفحة", use_container_width=True)
    
    if 'json_data' in st.session_state:
        st.markdown("---")
        change_theme_btn = st.button("🔄 تطبيق الألوان فقط (بدون توليد)", use_container_width=True)
        if change_theme_btn:
            st.session_state.final_page = inject_data_into_template(st.session_state.json_data, selected_template, colors_dict)
            st.rerun()

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج أولاً.")
    else:
        with st.spinner("1️⃣ جاري استخراج العقول التسويقية..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                with st.spinner("2️⃣ جاري تلوين الصفحة ودمج الصور..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data, selected_template, colors_dict)
                    st.session_state.json_data = parsed_data
                    st.session_state.current_colors = colors_dict
                    
                st.success("🎉 اكتمل بناء الصفحة الإنفوجرافيك! انظر التبويبات.")
            except json.JSONDecodeError:
                st.error("⚠️ حدث خطأ في قراءة الاستجابة. المحاولة مرة أخرى ستحلها.")
            except Exception as e:
                st.error(f"🛑 خطأ: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية الحية", "💻 كود HTML (جاهز للصور)"])
    
    with tab1:
        st.info("💡 الأماكن الرمادية المكتوب عليها [صورة...] هي الأماكن التي ستضع فيها صور منتجك الحقيقية. الكود مهيأ تماماً كإنفوجرافيك!")
        components.html(st.session_state.final_page, height=1200, scrolling=True)
        
    with tab2:
        st.write("انسخ هذا الكود، ثم ابحث عن `https://placehold.co/` واستبدلها بروابط صور منتجك.")
        st.code(st.session_state.final_page, language="html")
