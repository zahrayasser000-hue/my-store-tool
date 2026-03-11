import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Visual Ultimate", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>💎 ALI Growth Engine (نظام القوالب البصرية 13-SOP)</h1><p style="color:#94a3b8; margin:0;">صفحات هبوط مدججة بالصور والفيديوهات مصممة للتحويل العالي</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: نظام القوالب المتعددة
# تم إضافة قالب الـ 13 قسم البصري المكثف (Visual Ultimate)
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 🌟 القالب البصري الشامل (13 قسم - SOP-1) - الجديد والمستوحى من طلبك
    # ---------------------------------------------------------
    "💎 الشامل (13 قسم - بصري مكثف جداً)": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }
            /* محاكاة عرض الموبايل لزيادة التحويل كما في الصور */
            .mobile-wrapper { max-w-xl; mx-auto; bg-white; shadow-2xl; overflow-hidden; position: relative; }
            .img-placeholder { display: flex; align-items: center; justify-content: center; font-weight: bold; color: #64748b; background-color: #e2e8f0; text-align: center; }
        </style>
    </head>
    <body class="text-gray-800 antialiased pb-24 flex justify-center bg-gray-100">
        
        <div class="w-full max-w-lg bg-white shadow-2xl relative overflow-hidden">
            
            <!-- 1. شريط الثقة العلوي -->
            <div class="bg-green-700 text-white text-center py-2 text-xs font-bold tracking-wide flex justify-center gap-4">
                <span>🚚 شحن سريع مجاني</span>
                <span>🔒 دفع آمن 100%</span>
            </div>

            <!-- 2. Hero Section (فيديو/صورة البطل) -->
            <section class="relative bg-gray-900 text-white text-center">
                <div class="w-full h-80 img-placeholder bg-gray-800 text-gray-400 flex-col border-b-4 border-yellow-400">
                    <span class="text-4xl mb-2">📸 / 🎥</span>
                    <span>[ضع صورة أو فيديو مبهر للمنتج هنا]</span>
                </div>
                <div class="p-6 -mt-10 relative z-10 bg-gradient-to-t from-gray-900 to-transparent">
                    <h1 class="text-3xl font-black text-yellow-400 mb-3 leading-tight">{{HERO_HEADLINE}}</h1>
                    <p class="text-lg text-gray-200 mb-6 font-medium">{{HERO_SUB}}</p>
                    <a href="#buy" class="bg-green-600 hover:bg-green-500 text-white font-black py-4 px-8 rounded-full text-xl w-full block shadow-[0_0_15px_rgba(22,163,74,0.6)] animate-pulse">{{CTA_BUTTON}}</a>
                </div>
            </section>

            <!-- 3. Problem Section (GIF المشكلة) -->
            <section class="py-10 px-6 bg-red-50 text-center border-b border-red-100">
                <h2 class="text-2xl font-black text-red-600 mb-4">⚠️ {{PROBLEM_TITLE}}</h2>
                <div class="w-full h-48 img-placeholder rounded-xl mb-4 border-2 border-red-200 border-dashed">
                    <span>[صورة GIF متحركة توضح ألم العميل]</span>
                </div>
                <p class="text-base text-gray-700 font-bold leading-relaxed">{{PROBLEM_DESC}}</p>
            </section>

            <!-- 4. Solution Section (GIF الحل) -->
            <section class="py-10 px-6 bg-green-50 text-center border-b border-green-100">
                <h2 class="text-2xl font-black text-green-700 mb-4">✨ {{SOLUTION_TITLE}}</h2>
                <div class="w-full h-48 img-placeholder rounded-xl mb-4 border-2 border-green-200 border-dashed">
                    <span>[صورة GIF متحركة توضح سحر المنتج]</span>
                </div>
                <p class="text-base text-gray-700 font-bold leading-relaxed">{{SOLUTION_DESC}}</p>
            </section>

            <!-- 5. Unique Mechanism (كيف يعمل؟) -->
            <section class="py-10 px-6 bg-white text-center">
                <h2 class="text-2xl font-black text-gray-900 mb-4">⚙️ {{MECHANISM_TITLE}}</h2>
                <div class="w-full h-40 img-placeholder rounded-xl mb-4 bg-blue-50 text-blue-400">
                    <span>[صورة إنفوجرافيك تشرح التقنية/الآلية]</span>
                </div>
                <p class="text-sm text-gray-600 font-medium">{{MECHANISM_DESC}}</p>
            </section>

            <!-- 6. Comparison (قبل وبعد) -->
            <section class="py-10 px-6 bg-gray-50 text-center border-t border-b border-gray-200">
                <h2 class="text-2xl font-black text-gray-900 mb-6">تحول مذهل تلاحظه فوراً!</h2>
                <div class="flex gap-2 mb-4">
                    <div class="w-1/2">
                        <div class="h-40 img-placeholder rounded-lg bg-gray-300 border-b-4 border-red-500">صورة (قبل)</div>
                        <p class="mt-2 font-bold text-red-600">قبل الاستخدام</p>
                    </div>
                    <div class="w-1/2">
                        <div class="h-40 img-placeholder rounded-lg bg-gray-300 border-b-4 border-green-500">صورة (بعد)</div>
                        <p class="mt-2 font-bold text-green-600">بعد الاستخدام</p>
                    </div>
                </div>
            </section>

            <!-- 7. Ingredients / Features (الخصائص 3 دوائر) -->
            <section class="py-10 px-6 bg-white text-center">
                <h2 class="text-2xl font-black text-gray-900 mb-8">مكونات/خصائص فائقة</h2>
                <div class="flex justify-between gap-4">
                    {{INGREDIENTS_HTML}}
                </div>
            </section>

            <!-- 8. Benefits Grid (الفوائد) -->
            <section class="py-10 px-6 bg-gray-900 text-white">
                <h2 class="text-2xl font-black text-center text-yellow-400 mb-8">لماذا يعتبر الخيار الأول؟</h2>
                <div class="grid grid-cols-1 gap-4">
                    {{BENEFITS_HTML}}
                </div>
            </section>

            <!-- 9. Social Proof (ريلز وتجارب) -->
            <section class="py-10 px-6 bg-white text-center">
                <h2 class="text-2xl font-black text-gray-900 mb-6">آراء عملائنا (تجارب حقيقية)</h2>
                <div class="flex gap-3 overflow-x-auto pb-4">
                    <div class="min-w-[140px] h-64 img-placeholder rounded-xl bg-gray-100 flex-shrink-0">📱 ريلز 1</div>
                    <div class="min-w-[140px] h-64 img-placeholder rounded-xl bg-gray-100 flex-shrink-0">📱 ريلز 2</div>
                    <div class="min-w-[140px] h-64 img-placeholder rounded-xl bg-gray-100 flex-shrink-0">📱 ريلز 3</div>
                </div>
            </section>

            <!-- 10. Expert Authority (رأي الخبير) -->
            <section class="py-10 px-6 bg-blue-50 border-t border-blue-100 relative">
                <div class="flex items-center gap-4 bg-white p-4 rounded-2xl shadow-md border-r-4 border-blue-600">
                    <div class="w-20 h-20 rounded-full img-placeholder flex-shrink-0 bg-blue-100 text-blue-500 rounded-full">👨‍⚕️ صورة خبير</div>
                    <div class="text-right">
                        <h4 class="font-black text-blue-900 text-lg">ينصح به الخبراء</h4>
                        <p class="text-sm font-medium text-gray-600 italic">"{{EXPERT_QUOTE}}"</p>
                    </div>
                </div>
            </section>

            <!-- 11. How to Use (خطوات الاستخدام) -->
            <section class="py-10 px-6 bg-white text-center">
                <h2 class="text-2xl font-black text-gray-900 mb-8">سهل الاستخدام في 3 خطوات</h2>
                <div class="space-y-4">
                    {{STEPS_HTML}}
                </div>
            </section>

            <!-- 12. Risk Reversal (ضمان استرجاع الأموال) -->
            <section class="bg-gray-900 text-white py-12 px-6 text-center border-t-4 border-yellow-400">
                <div class="w-32 h-32 mx-auto img-placeholder rounded-full bg-yellow-100 text-yellow-600 mb-4 border-4 border-yellow-400">🛡️ ختم الضمان</div>
                <h3 class="text-2xl font-black text-yellow-400 mb-3">ضمان استرجاع الأموال 100%</h3>
                <p class="text-base font-medium leading-relaxed text-gray-300">{{GUARANTEE}}</p>
            </section>

            <!-- 13. Sticky Urgency CTA (الزر العائم) -->
            <div id="buy" class="fixed bottom-0 left-0 w-full bg-white p-3 shadow-[0_-10px_20px_rgba(0,0,0,0.15)] flex justify-center z-50 border-t-2 border-red-500">
                <div class="w-full max-w-lg flex flex-col items-center">
                    <div class="text-red-600 text-xs font-black mb-1 animate-pulse flex items-center gap-1">
                        ⏳ العرض ينتهي قريباً! سارع بالطلب
                    </div>
                    <a href="#buy" class="bg-red-600 hover:bg-red-700 text-white font-black py-4 px-4 rounded-xl text-xl w-full text-center shadow-lg transition transform hover:scale-[1.02] flex justify-center items-center gap-2">
                        🛒 {{CTA_BUTTON}}
                    </a>
                </div>
            </div>

        </div>
    </body>
    </html>
    """,
    
    # ---------------------------------------------------------
    # 🌸 القالب الأنيق (للمنتجات النسائية والتجميل)
    # ---------------------------------------------------------
    "🌸 الأنيق (كلاسيكي - وردي)": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap" rel="stylesheet">
        <style>body { font-family: 'Cairo', sans-serif; background-color: #fff1f2; scroll-behavior: smooth; }</style>
    </head>
    <body class="text-gray-800 antialiased relative pb-24">
        <div class="bg-rose-900 text-rose-50 text-center py-2 text-sm font-semibold tracking-wide shadow-sm">
            ✨ توصيل مجاني وسريع | 💳 الدفع عند الاستلام 
        </div>
        <section class="bg-gradient-to-b from-rose-50 to-white py-20 px-4 rounded-b-[3rem] shadow-sm mb-10">
            <div class="max-w-3xl mx-auto text-center">
                <h1 class="text-4xl md:text-5xl font-extrabold text-rose-900 mb-6 leading-tight">{{HERO_HEADLINE}}</h1>
                <p class="text-xl text-rose-700 mb-10 font-medium">{{HERO_SUB}}</p>
                <a href="#buy" class="bg-rose-500 hover:bg-rose-600 text-white font-bold py-4 px-12 rounded-full text-xl inline-block shadow-lg shadow-rose-200 transition transform hover:-translate-y-1">{{CTA_BUTTON}}</a>
            </div>
        </section>
        <section class="py-16 px-4 text-center">
            <div class="max-w-3xl mx-auto bg-white p-10 rounded-[2rem] shadow-xl shadow-rose-100/50">
                <h2 class="text-3xl font-bold text-gray-800 mb-4">⚠️ {{PROBLEM_TITLE}}</h2>
                <p class="text-lg text-gray-600 font-medium leading-relaxed">{{PROBLEM_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4 text-center">
            <div class="max-w-3xl mx-auto bg-rose-500 text-white p-10 rounded-[2rem] shadow-xl">
                <h2 class="text-3xl font-bold mb-4 text-rose-100">✨ {{SOLUTION_TITLE}}</h2>
                <p class="text-lg font-medium leading-relaxed">{{SOLUTION_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4">
            <div class="max-w-5xl mx-auto text-center">
                <h2 class="text-3xl font-extrabold text-rose-900 mb-12">لماذا تعشقه عميلاتنا؟</h2>
                <div class="grid grid-cols-1 gap-4 max-w-2xl mx-auto">{{BENEFITS_HTML}}</div>
            </div>
        </section>
        <section class="bg-rose-100 py-16 px-4 text-center mt-8 rounded-t-[3rem]">
            <div class="max-w-3xl mx-auto">
                <div class="text-6xl mb-4">👑</div>
                <h3 class="text-3xl font-bold text-rose-900 mb-4">ضمان الرضا 100%</h3>
                <p class="text-lg font-medium text-rose-800 leading-relaxed">{{GUARANTEE}}</p>
            </div>
        </section>
        <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/90 backdrop-blur-md p-4 shadow-[0_-10px_20px_rgba(0,0,0,0.05)] text-center flex justify-center z-50">
            <a href="#buy" class="bg-rose-600 hover:bg-rose-700 text-white font-bold py-4 px-10 rounded-full text-xl w-full max-w-md shadow-lg transition animate-pulse">{{CTA_BUTTON}}</a>
        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي (JSON Generator المطور للـ 13 قسم)
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
    
    # تحديث البرومت ليغطي الأقسام البصرية الجديدة (مكونات، خطوات، خبير، إلخ)
    prompt = f"""
    أنت أعظم Copywriter تسويقي لصفحات الهبوط البصرية (Infographic Sales Pages).
    المنتج: "{product}".
    
    المطلوب: توليد نصوص قصيرة، قوية، وخاطفة تناسب التصميم البصري.
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
# 💉 الخطوة 3: محرك الحقن الذكي الشامل (Smart Data Binding)
# يجهز الـ HTML المعقد (دوائر، خطوات، شبكات) بناءً على القالب
# ==========================================================
def inject_data_into_template(json_data, template_name):
    # 1. تجهيز الفوائد (Benefits)
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        if "الشامل" in template_name:
            benefits_html += f'<div class="bg-gray-800 p-4 rounded-xl flex items-center gap-4 border border-gray-700"><div class="text-3xl">🎯</div><p class="font-bold text-gray-100 text-right">{benefit}</p></div>'
        else:
            benefits_html += f'<div class="bg-white p-6 rounded-3xl shadow-lg border border-rose-50 text-center"><div class="text-4xl mb-4">✨</div><p class="font-bold text-rose-900 text-lg">{benefit}</p></div>'

    # 2. تجهيز المكونات/الخصائص (Ingredients - للنموذج الشامل فقط)
    ingredients_html = ""
    ingredients_list = json_data.get('ingredients', ["خاصية رائعة", "آمن تماماً", "جودة عالية"])
    for ing in ingredients_list[:3]:
        ingredients_html += f'<div class="flex flex-col items-center w-1/3"><div class="w-20 h-20 rounded-full img-placeholder mb-2 shadow-inner bg-green-100 text-green-500 border-4 border-white shadow-lg text-2xl">🌿</div><p class="text-xs font-bold text-gray-700">{ing}</p></div>'

    # 3. تجهيز الخطوات (Steps - للنموذج الشامل فقط)
    steps_html = ""
    steps_list = json_data.get('steps', ["خطوة 1", "خطوة 2", "خطوة 3"])
    for i, step in enumerate(steps_list[:3], 1):
        steps_html += f'<div class="flex items-center gap-4 bg-gray-50 p-3 rounded-lg border border-gray-200"><div class="w-12 h-12 flex items-center justify-center bg-blue-600 text-white font-black rounded-full flex-shrink-0 text-xl">{i}</div><p class="font-bold text-gray-800 text-right text-sm">{step}</p></div>'

    # جلب القالب المناسب
    final_html = TEMPLATES[template_name]
    
    # الحقن الأساسي
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", "اكتشف الحل الأمثل"))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", "المنتج الذي سيغير حياتك للأفضل."))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", "هل تعاني من هذه المشكلة؟"))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", "الكثير يعانون من نفس المشكلة يومياً..."))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", "الحل النهائي أصبح بين يديك"))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", "بفضل تقنيتنا الفريدة، ستحصل على نتائج فورية."))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", "نضمن لك استرجاع أموالك بالكامل."))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن واستفد من العرض"))
    final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)
    
    # الحقن الخاص بالقالب الشامل (13 قسم)
    if "الشامل" in template_name:
        final_html = final_html.replace("{{MECHANISM_TITLE}}", json_data.get("mechanism_title", "كيف يعمل؟"))
        final_html = final_html.replace("{{MECHANISM_DESC}}", json_data.get("mechanism_description", "تقنية مبتكرة لحل مشكلتك من الجذور."))
        final_html = final_html.replace("{{EXPERT_QUOTE}}", json_data.get("expert_quote", "هذا المنتج هو الأفضل في فئته، أنصح به بشدة لكل من يبحث عن الجودة."))
        final_html = final_html.replace("{{INGREDIENTS_HTML}}", ingredients_html)
        final_html = final_html.replace("{{STEPS_HTML}}", steps_html)
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج", placeholder="مثال: جهاز Flawless لإزالة الشعر")
    
    st.markdown("---")
    st.subheader("🎨 اختر تصميم الصفحة")
    # تم وضع القالب البصري الشامل كخيار أول افتراضي
    selected_template = st.selectbox("القوالب المتاحة:", list(TEMPLATES.keys()))
    
    start_btn = st.button("⚡ توليد الصفحة الجديدة", use_container_width=True)
    
    if 'json_data' in st.session_state:
        st.markdown("---")
        change_theme_btn = st.button("🔄 تغيير التصميم فقط (سريع)", use_container_width=True)
        if change_theme_btn:
            st.session_state.final_page = inject_data_into_template(st.session_state.json_data, selected_template)
            st.rerun()

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج أولاً.")
    else:
        with st.spinner("1️⃣ جاري توليد المحتوى التسويقي (يستغرق 10-15 ثانية)..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                with st.spinner(f"2️⃣ جاري حقن البيانات في قالب [{selected_template}]..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data, selected_template)
                    st.session_state.json_data = parsed_data
                    st.session_state.current_template = selected_template
                    
                st.success("🎉 اكتمل بناء الصفحة بنجاح! راجع التبويبات بالأسفل.")
            except json.JSONDecodeError:
                st.error("⚠️ حدث خطأ في قراءة استجابة الذكاء الاصطناعي. الرجاء المحاولة مرة أخرى.")
            except Exception as e:
                st.error(f"🛑 خطأ في الاتصال: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة البصرية الحية", "💻 كود HTML (جاهز للصور)", "📝 المحتوى (JSON)"])
    
    with tab1:
        st.info("💡 لاحظ الصناديق الرمادية المكتوب عليها [ضع صورة...]، هذا هو المكان الذي ستستبدله بصور/GIF منتجك الحقيقي في الكود.")
        components.html(st.session_state.final_page, height=1000, scrolling=True)
        
    with tab2:
        st.write("انسخ هذا الكود لموقعك، ثم قم بتغيير الروابط (src) داخل وسوم الصور والفيديوهات.")
        st.code(st.session_state.final_page, language="html")
        
    with tab3:
        st.write("النصوص المستخرجة والتي تغذي الأقسام الـ 13:")
        st.json(st.session_state.json_data)
