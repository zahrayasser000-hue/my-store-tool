import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Multi-Template System", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #1e293b, #0f172a); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⚙️ ALI Growth Engine (نظام القوالب المتعددة)</h1><p style="color:#94a3b8; margin:0;">اختر القالب، ولد المحتوى، وانطلق!</p></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: نظام القوالب المتعددة (Multi-Template Engine)
# قوالب مبرمجة مسبقاً، لا تنكسر، ومصممة بـ Tailwind CSS
# ==========================================================

TEMPLATES = {
    # ---------------------------------------------------------
    # 1. القالب الأنيق (لمنتجات التجميل والعناية بالبشرة) - وردي ناعم
    # ---------------------------------------------------------
    "🌸 الأنيق (لمنتجات التجميل والعناية)": """
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
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">{{BENEFITS_HTML}}</div>
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
    """,

    # ---------------------------------------------------------
    # 2. القالب الهجومي (للعروض المحدودة والمنتجات الرخيصة) - أسود وأحمر
    # ---------------------------------------------------------
    "🔥 الهجومي (عروض وخصومات)": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap" rel="stylesheet">
        <style>body { font-family: 'Cairo', sans-serif; background-color: #f3f4f6; scroll-behavior: smooth; }</style>
    </head>
    <body class="text-gray-900 antialiased relative pb-24">
        <div class="bg-red-600 text-white text-center py-3 text-base font-black tracking-widest uppercase animate-pulse">
            🚨 عرض محدود: الكمية توشك على النفاذ! 🚨
        </div>
        <section class="bg-gray-900 text-white py-20 px-4 border-b-8 border-yellow-400">
            <div class="max-w-3xl mx-auto text-center">
                <h1 class="text-4xl md:text-6xl font-black text-yellow-400 mb-6 leading-tight drop-shadow-lg">{{HERO_HEADLINE}}</h1>
                <p class="text-2xl text-gray-300 mb-8 font-bold">{{HERO_SUB}}</p>
                <a href="#buy" class="bg-red-600 hover:bg-red-500 text-white font-black py-5 px-14 rounded-lg text-2xl inline-block shadow-[0_0_20px_rgba(220,38,38,0.6)] transition transform hover:scale-105">{{CTA_BUTTON}}</a>
            </div>
        </section>
        <section class="py-16 px-4 bg-white text-center border-b border-gray-200">
            <div class="max-w-3xl mx-auto">
                <h2 class="text-4xl font-black text-red-600 mb-6">🛑 {{PROBLEM_TITLE}}</h2>
                <p class="text-xl text-gray-800 font-bold leading-relaxed">{{PROBLEM_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4 bg-yellow-400 text-center border-b border-yellow-500">
            <div class="max-w-3xl mx-auto">
                <h2 class="text-4xl font-black text-gray-900 mb-6">🔥 {{SOLUTION_TITLE}}</h2>
                <p class="text-xl text-gray-800 font-bold leading-relaxed">{{SOLUTION_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4 bg-gray-100">
            <div class="max-w-5xl mx-auto text-center">
                <h2 class="text-4xl font-black text-gray-900 mb-12 uppercase">المميزات الجبارة</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{{BENEFITS_HTML}}</div>
            </div>
        </section>
        <section class="bg-black text-white py-16 px-4 text-center mt-12 border-t-8 border-red-600">
            <div class="max-w-3xl mx-auto">
                <h3 class="text-4xl font-black text-yellow-400 mb-6">⚠️ ضمان حديدي 100%</h3>
                <p class="text-xl font-bold leading-relaxed text-gray-300">{{GUARANTEE}}</p>
            </div>
        </section>
        <div id="buy" class="fixed bottom-0 left-0 w-full bg-black p-4 text-center flex justify-center z-50 border-t-4 border-yellow-400">
            <a href="#buy" class="bg-red-600 hover:bg-red-500 text-white font-black py-4 px-10 rounded-lg text-2xl w-full max-w-lg shadow-[0_0_20px_rgba(220,38,38,0.8)] transition animate-pulse">{{CTA_BUTTON}}</a>
        </div>
    </body>
    </html>
    """,

    # ---------------------------------------------------------
    # 3. القالب الحديث (للمنتجات التقنية والمنزلية) - أزرق ورمادي
    # ---------------------------------------------------------
    "💼 الحديث (احترافي وموثوق)": """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>body { font-family: 'Cairo', sans-serif; background-color: #f8fafc; scroll-behavior: smooth; }</style>
    </head>
    <body class="text-gray-800 antialiased relative pb-24">
        <div class="bg-slate-900 text-white text-center py-2 text-sm font-bold tracking-wide">
            🚚 شحن مجاني اليوم | 💳 دفع عند الاستلام | 🛡️ ضمان ذهبي
        </div>
        <section class="bg-white py-20 px-4 shadow-sm border-b border-gray-200">
            <div class="max-w-3xl mx-auto text-center">
                <h1 class="text-4xl md:text-5xl font-black text-blue-900 mb-6 leading-tight">{{HERO_HEADLINE}}</h1>
                <p class="text-xl text-gray-600 mb-10 font-medium">{{HERO_SUB}}</p>
                <a href="#buy" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-12 rounded-xl text-xl inline-block shadow-lg transition transform hover:-translate-y-1">{{CTA_BUTTON}}</a>
            </div>
        </section>
        <section class="py-16 px-4 bg-slate-50 text-center border-b border-slate-200">
            <div class="max-w-3xl mx-auto">
                <h2 class="text-3xl font-bold text-red-600 mb-4">⚠️ {{PROBLEM_TITLE}}</h2>
                <p class="text-lg text-gray-700 font-medium leading-relaxed">{{PROBLEM_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4 bg-blue-50 text-center border-b border-blue-100">
            <div class="max-w-3xl mx-auto">
                <h2 class="text-3xl font-bold text-blue-700 mb-4">💡 {{SOLUTION_TITLE}}</h2>
                <p class="text-lg text-gray-700 font-medium leading-relaxed">{{SOLUTION_DESC}}</p>
            </div>
        </section>
        <section class="py-16 px-4 bg-white">
            <div class="max-w-5xl mx-auto text-center">
                <h2 class="text-3xl font-black text-gray-800 mb-12">لماذا يختاره الجميع؟</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{{BENEFITS_HTML}}</div>
            </div>
        </section>
        <section class="bg-slate-900 text-white py-16 px-4 text-center mt-8 rounded-t-2xl shadow-inner">
            <div class="max-w-3xl mx-auto">
                <div class="text-6xl mb-4">🛡️</div>
                <h3 class="text-3xl font-bold text-blue-400 mb-4">ضمان ذهبي 100%</h3>
                <p class="text-lg font-medium leading-relaxed text-slate-300">{{GUARANTEE}}</p>
            </div>
        </section>
        <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.1)] text-center flex justify-center border-t border-gray-200 z-50">
            <a href="#buy" class="bg-blue-600 hover:bg-blue-700 text-white font-black py-3 px-10 rounded-xl text-xl w-full max-w-md shadow-lg transition animate-pulse">{{CTA_BUTTON}}</a>
        </div>
    </body>
    </html>
    """
}

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي السريع (JSON Generator)
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
    أنت أعظم Copywriter تسويقي. اكتب محتوى قوي لمنتج: "{product}".
    رد حصراً بـ JSON صالح (Valid JSON) بهذا الهيكل الدقيق:
    {{
        "hero_headline": "عنوان رئيسي صادم ومثير للاهتمام",
        "hero_subheadline": "عنوان فرعي مقنع يشرح الفائدة",
        "problem_title": "عنوان قسم المشكلة",
        "problem_description": "وصف ألم العميل بشكل عاطفي",
        "solution_title": "عنوان قسم الحل",
        "solution_description": "كيف يحل هذا المنتج المشكلة بالآلية الفريدة",
        "benefits": ["الفائدة الأولى", "الفائدة الثانية", "الفائدة الثالثة"],
        "guarantee": "نص عكس المخاطرة وضمان استرجاع الأموال",
        "call_to_action": "نص زر الشراء السريع"
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
# 💉 الخطوة 3: محرك الحقن الذكي (Smart Data Binding)
# يغير تصميم الفوائد بناءً على القالب المختار
# ==========================================================
def inject_data_into_template(json_data, template_name):
    # تنسيق الفوائد بناءً على القالب المختار
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        if "الأنيق" in template_name:
            benefits_html += f'<div class="bg-white p-6 rounded-3xl shadow-lg border border-rose-50 text-center"><div class="text-4xl mb-4">✨</div><p class="font-bold text-rose-900 text-lg">{benefit}</p></div>'
        elif "الهجومي" in template_name:
            benefits_html += f'<div class="bg-gray-900 p-6 rounded-lg shadow-xl border-b-4 border-red-600 text-center"><div class="text-4xl mb-4">⚡</div><p class="font-black text-white text-xl">{benefit}</p></div>'
        else: # الحديث
            benefits_html += f'<div class="bg-slate-50 p-6 rounded-xl shadow-sm border border-slate-200 text-center"><div class="text-4xl mb-4">✅</div><p class="font-bold text-slate-800 text-lg">{benefit}</p></div>'
    
    # جلب القالب المناسب
    final_html = TEMPLATES[template_name]
    
    # الحقن
    final_html = final_html.replace("{{HERO_HEADLINE}}", json_data.get("hero_headline", "اكتشف الحل الأمثل"))
    final_html = final_html.replace("{{HERO_SUB}}", json_data.get("hero_subheadline", "المنتج الذي سيغير حياتك للأفضل."))
    final_html = final_html.replace("{{PROBLEM_TITLE}}", json_data.get("problem_title", "هل تعاني من هذه المشكلة؟"))
    final_html = final_html.replace("{{PROBLEM_DESC}}", json_data.get("problem_description", "الكثير يعانون من نفس المشكلة يومياً..."))
    final_html = final_html.replace("{{SOLUTION_TITLE}}", json_data.get("solution_title", "الحل النهائي أصبح بين يديك"))
    final_html = final_html.replace("{{SOLUTION_DESC}}", json_data.get("solution_description", "بفضل تقنيتنا الفريدة، ستحصل على نتائج فورية."))
    final_html = final_html.replace("{{GUARANTEE}}", json_data.get("guarantee", "نضمن لك استرجاع أموالك بالكامل إذا لم تكن راضياً."))
    final_html = final_html.replace("{{CTA_BUTTON}}", json_data.get("call_to_action", "اطلب الآن واستفد من العرض"))
    final_html = final_html.replace("{{BENEFITS_HTML}}", benefits_html)
    
    return final_html

# --- واجهة المستخدم (Sidebar & Main) ---
with st.sidebar:
    st.header("⚙️ إعدادات المحرك")
    api_key = st.text_input("🔑 أدخل API Key", type="password")
    product_name = st.text_input("📦 اسم/وصف المنتج", placeholder="مثال: جهاز Flawless لإزالة الشعر")
    
    # ✨ الإضافة الجديدة: اختيار القالب
    st.markdown("---")
    st.subheader("🎨 اختر تصميم الصفحة")
    selected_template = st.selectbox("القوالب المتاحة:", list(TEMPLATES.keys()))
    
    start_btn = st.button("⚡ توليد الصفحة الجديدة", use_container_width=True)
    
    # زر إضافي لتغيير التصميم فقط (بدون طلب كلمات جديدة من الذكاء الاصطناعي)
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
        with st.spinner("1️⃣ جاري توليد المحتوى التسويقي..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                with st.spinner(f"2️⃣ جاري تجميع وتلوين الصفحة باستخدام [{selected_template}]..."):
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
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة الحية", "💻 كود HTML", "📝 المحتوى (JSON)"])
    
    with tab1:
        st.info(f"💡 أنت تشاهد الآن: **{st.session_state.get('current_template', selected_template)}**")
        components.html(st.session_state.final_page, height=900, scrolling=True)
        
    with tab2:
        st.code(st.session_state.final_page, language="html")
        
    with tab3:
        st.write("هذه هي النصوص التي تم حقنها في القالب المختار:")
        st.json(st.session_state.json_data)
