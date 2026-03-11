import streamlit as st
import google.generativeai as genai
import json
import streamlit.components.v1 as components
import re

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine - Template System", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: #1e293b; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⚙️ ALI Growth Engine (نظام القوالب الصاروخي)</h1></div>', unsafe_allow_html=True)

# ==========================================================
# 🧱 الخطوة 2: القالب الصلب (Hard-Coded HTML Template)
# ==========================================================
MASTER_TEMPLATE = """
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
    
    <!-- شريط الثقة -->
    <div class="bg-gray-900 text-white text-center py-2 text-sm font-bold tracking-wide">
        🚚 شحن مجاني اليوم | 💳 دفع عند الاستلام | 🛡️ ضمان ذهبي
    </div>

    <!-- Hero Section -->
    <section class="bg-white py-16 px-4 shadow-sm border-b border-gray-100">
        <div class="max-w-3xl mx-auto text-center">
            <h1 class="text-4xl md:text-5xl font-black text-blue-900 mb-6 leading-tight">{{HERO_HEADLINE}}</h1>
            <p class="text-xl text-gray-600 mb-8 font-medium">{{HERO_SUB}}</p>
            <a href="#buy" class="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-12 rounded-full text-xl inline-block shadow-lg transition transform hover:-translate-y-1">{{CTA_BUTTON}}</a>
        </div>
    </section>

    <!-- Problem Section -->
    <section class="py-16 px-4 bg-red-50 text-center">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-red-600 mb-4">⚠️ {{PROBLEM_TITLE}}</h2>
            <p class="text-lg text-gray-700 font-medium leading-relaxed">{{PROBLEM_DESC}}</p>
        </div>
    </section>

    <!-- Solution Section -->
    <section class="py-16 px-4 bg-green-50 text-center border-t border-green-100">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-green-600 mb-4">✨ {{SOLUTION_TITLE}}</h2>
            <p class="text-lg text-gray-700 font-medium leading-relaxed">{{SOLUTION_DESC}}</p>
        </div>
    </section>

    <!-- Benefits Grid -->
    <section class="py-16 px-4 bg-white">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-3xl font-black text-center text-gray-800 mb-10">لماذا يختاره الجميع؟</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {{BENEFITS_HTML}}
            </div>
        </div>
    </section>

    <!-- Guarantee -->
    <section class="bg-blue-900 text-white py-16 px-4 text-center mt-8 rounded-t-3xl shadow-inner">
        <div class="max-w-3xl mx-auto">
            <div class="text-6xl mb-4">🛡️</div>
            <h3 class="text-3xl font-bold text-yellow-400 mb-4">ضمان ذهبي 100%</h3>
            <p class="text-lg font-medium leading-relaxed">{{GUARANTEE}}</p>
        </div>
    </section>

    <!-- Sticky Footer CTA -->
    <div id="buy" class="fixed bottom-0 left-0 w-full bg-white/95 backdrop-blur-sm p-4 shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.1)] text-center flex justify-center border-t border-gray-200 z-50">
        <a href="#buy" class="bg-green-600 hover:bg-green-500 text-white font-black py-3 px-10 rounded-xl text-xl w-full max-w-md shadow-[0_0_15px_rgba(22,163,74,0.5)] transition animate-pulse">{{CTA_BUTTON}}</a>
    </div>

</body>
</html>
"""

# ==========================================================
# 🧠 الخطوة 1: المحرك اللفظي السريع (JSON Generator)
# ==========================================================
def get_fast_working_model(api_key):
    # استخدام الذاكرة لتسريع العملية بعد أول ضغطة
    if 'valid_model_name' in st.session_state:
        return st.session_state.valid_model_name
        
    genai.configure(api_key=api_key, transport="rest")
    try:
        # البحث عن أفضل موديل متاح لحسابك لمنع خطأ 404
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.valid_model_name = m.name
                return m.name
    except:
        pass
        
    # الموديل الاحتياطي الآمن جداً
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
    
    # تمت إزالة القيود الصارمة للـ JSON لتتوافق مع كل الموديلات وتمنع الأخطاء
    response = model.generate_content(
        prompt,
        request_options={"timeout": 20.0}
    )
    
    # تنظيف النص بأمان تام
    tb = chr(96) * 3 
    clean_text = re.sub(f'{tb}(?:json|JSON)?', '', response.text, flags=re.IGNORECASE)
    clean_text = clean_text.replace(tb, '').strip()
    
    # محاولة استخراج كود JSON فقط في حال قام الموديل بإضافة نصوص أخرى
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match:
        return match.group(0)
        
    return clean_text

# ==========================================================
# 💉 الخطوة 3: محرك الحقن (Data Binding Engine)
# ==========================================================
def inject_data_into_template(json_data):
    benefits_html = ""
    for benefit in json_data.get('benefits', []):
        benefits_html += f"""
        <div class="bg-gray-50 p-6 rounded-2xl shadow-sm border border-gray-100 text-center hover:shadow-md transition duration-300">
            <div class="text-4xl mb-4">✅</div>
            <p class="font-bold text-gray-800 text-lg">{benefit}</p>
        </div>
        """
    
    final_html = MASTER_TEMPLATE
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
    product_name = st.text_input("📦 اسم/وصف المنتج (مثال: حذاء طبي مريح)")
    start_btn = st.button("⚡ توليد الصفحة (سريع جداً)")
    st.info("💡 تم تفعيل بروتوكول REST لضمان عدم انقطاع الاتصال وتوفير سرعة قصوى.")

if start_btn:
    if not api_key or not product_name:
        st.error("يرجى إدخال المفتاح واسم المنتج أولاً.")
    else:
        with st.spinner("1️⃣ جاري توليد المحتوى التسويقي..."):
            try:
                raw_json = generate_landing_page_json(api_key, product_name)
                parsed_data = json.loads(raw_json)
                
                with st.spinner("2️⃣ جاري تجميع وتلوين الصفحة..."):
                    st.session_state.final_page = inject_data_into_template(parsed_data)
                    st.session_state.json_data = parsed_data
                    
                st.success("🎉 اكتمل بناء الصفحة بنجاح! راجع التبويبات بالأسفل.")
            except json.JSONDecodeError:
                st.error("⚠️ حدث خطأ في قراءة استجابة الذكاء الاصطناعي. الرجاء المحاولة مرة أخرى.")
            except Exception as e:
                st.error(f"🛑 خطأ في الاتصال: {str(e)}")

# --- العرض (التبويبات) ---
if 'final_page' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📱 المعاينة الحية", "💻 كود HTML للنسخ", "📝 المحتوى (JSON)"])
    
    with tab1:
        st.info("💡 هذه المعاينة حية ومبنية بنظام القوالب (لا يمكن أن تنكسر).")
        components.html(st.session_state.final_page, height=900, scrolling=True)
        
    with tab2:
        st.code(st.session_state.final_page, language="html")
        
    with tab3:
        st.write("هذه هي النصوص التي استخرجها الذكاء الاصطناعي وقام بحقنها في التصميم:")
        st.json(st.session_state.json_data)
