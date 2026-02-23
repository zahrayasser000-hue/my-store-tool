import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V18", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

# --- 2. التصميم (CSS) لحل مشاكل التداخل ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}
.main-header { background: #182848; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
.image-prompt-box { background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ffbd45; direction: ltr; text-align: left; }
.stDataFrame div[data-testid="stTable"] { direction: ltr !important; }
.stDataFrame td, .stDataFrame th { text-align: center !important; }
/* تحسين شكل صناديق النصوص لمنع التداخل */
div.stTextArea textarea { font-family: 'Cairo', sans-serif !important; font-size: 16px; direction: rtl; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
if 'html_code' not in st.session_state: st.session_state.html_code = ""
if 'image_prompts' not in st.session_state: st.session_state.image_prompts = []
if 'video_scripts' not in st.session_state: st.session_state.video_scripts = ""
if 'marketing_strategy' not in st.session_state: st.session_state.marketing_strategy = ""
if 'active_model' not in st.session_state: st.session_state.active_model = None

# --- 4. دوال الذكاء الاصطناعي ---
def get_working_model(api_key):
    if st.session_state.active_model: return st.session_state.active_model
    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                st.session_state.active_model = m.name
                return m.name
        st.session_state.active_model = "gemini-pro"
        return "gemini-pro"
    except: return "gemini-pro"

def generate_strategy(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير أبحاث تسويقية من مدرسة Agora العملاقة.
        المطلوب: دراسة سوق لمنتج: {product_name}.
        ⚠️ ركز على: 1. الآلية الفريدة، 2. الحجة التي لا تقهر، 3. المعتقدات الأساسية، 4. فجوات السوق.
        اكتب باللغة العربية الفصحى بشكل منظم وواضح."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_html_page(api_key, product_name, strategy_text):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""أنت أعظم مبرمج ومصمم لصفحات الهبوط البصرية (Visual-First).
        المطلوب: برمجة كود HTML و CSS متكامل لصفحة هبوط لمنتج: {product_name}.
        
        🧠 **[هام جداً]: ابنِ النصوص بناءً على هذه الاستراتيجية:** {strategy_text}
        
        ⚠️ قوانين التصميم الإلزامية:
        - ابدأ الكود بـ <html lang="ar" dir="rtl"> إجبارياً.
        - النصوص عربية فقط، بخط 'Cairo'، وقليلة جداً (عناوين فقط). الباقي مساحات للصور والفيديوهات (استخدم Placeholders).
        - التصميم (Mobile First) بعرض أقصى 480px متمركز في المنتصف.
        
        ⚠️ الأقسام الـ 12 الإلزامية (لا تحذف أي قسم):
        1. <section id="hero">: فيديو خلفية مع عنوان خطاف مبني على الحجة، وزر طلب.
        2. <section id="problem">: صورة GIF توضح المشكلة والألم مع عنوان قصير.
        3. <section id="solution">: صورة GIF توضح الحل بالمنتج مع عنوان جذاب.
        4. <section id="unique-mechanism">: صورة مقطعية تشرح الآلية الفريدة (Agora).
        5. <section id="benefits-grid">: شبكة من 4 صور مربعة تبرز النتائج العاطفية (FAB).
        6. <section id="comparison">: جدول أو صورتين متجاورتين (نحن مقابل الآخرين).
        7. <section id="ingredients">: 3 أيقونات تشرح المكونات أو جودة الصناعة.
        8. <section id="social-proof">: 3 حاويات (فيديوهات ريلز طولية) لآراء العملاء.
        9. <section id="expert-authority">: صورة لخبير/طبيب/مؤثر مع اقتباس قصير يعزز الثقة.
        10. <section id="how-to-use">: 3 خطوات بسيطة مصورة (GIFs أو أيقونات) لطريقة الاستخدام.
        11. <section id="risk-reversal">: ختم ضمان ذهبي كبير جداً لضمان الاسترجاع.
        12. <section id="urgency-cta">: عداد تنازلي GIF، وزر عائم بالأسفل (Sticky CTA) يتحرك ببطء.
        
        أعطني فقط كود الـ HTML والـ CSS المدمج داخل علامتي ```html و ```."""
        
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_video_scripts(api_key, product_name, strategy_text):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        المنصات: تيك توك، انستجرام ريلز، يوتيوب شورتس، سناب شات، فيسبوك.
        
        🧠 **اعتمد في كتابتك على هذه الاستراتيجية:** {strategy_text}
        
        ⚠️ الإطار الإلزامي: (AIDA). ركز على المشكلة في أول 3 ثواني، والنتيجة العاطفية في المنتصف.
        اكتب باللغة العربية، ونسق النص ليكون واضحاً وسهل القراءة."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. Hero Shot
        2. Lifestyle Shot
        3. Macro Shot
        افصل بينها بـ: "---PROMPT_SEPARATOR---" """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V18.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - المحرك البصري بـ 12 قسماً (V18)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية", "📱 صفحة الهبوط (12 قسم)", "🎬 سكريبتات الفيديو", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة (Agora)")
        if st.button("🧠 استخراج الاستراتيجية"):
            if product_name:
                with st.spinner("جاري التحليل واستخراج الآلية الفريدة..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.marketing_strategy:
            # استخدام st.text_area لحل مشكلة التداخل وجعل التصفح خفيفاً
            st.text_area("نتائج الاستراتيجية (قابلة للنسخ والتمرير):", value=st.session_state.marketing_strategy, height=400)

    with tabs[1]:
        st.subheader("بناء صفحة هبوط بصرية متكاملة (12 قسم)")
        if st.button("🚀 توليد الصفحة المتكاملة"):
            if product_name:
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس لتصميم الصفحة..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                
                with st.spinner("جاري برمجة وتصميم الصفحة بـ 12 قسماً بصرياً..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name, st.session_state.marketing_strategy)
            else: st.error("أدخل اسم المنتج!")
        
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة بـ 12 قسماً!")
            components.html(st.session_state.html_code, height=750, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو")
        if st.button("🎬 توليد السكريبتات"):
            if product_name:
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس للسكريبتات..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                        
                with st.spinner("جاري كتابة السكريبتات التسويقية..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name, st.session_state.marketing_strategy)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.video_scripts:
            # استخدام st.text_area لحل مشكلة التداخل وجعل التصفح خفيفاً
            st.text_area("السكريبتات الـ 5 (قابلة للنسخ والتمرير):", value=st.session_state.video_scripts, height=500)

    with tabs[3]:
        st.subheader("أوامر توليد الصور")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            for i, p in enumerate(st.session_state.image_prompts):
                st.markdown(f'<div class="image-prompt-box"><strong>البرومت {i+1}:</strong><br>{p}</div>', unsafe_allow_html=True)

    with tabs[4]:
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                break_even_dr = (C + CPL) / P
                st.info(f"💡 نقطة التعادل المحسوبة: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")
                col_a, col_b = st.columns(2)
                with col_a: country_col = st.selectbox("عمود الدولة:", df.columns)
                with col_b: dr_col = st.selectbox("عمود نسبة التسليم:", df.columns)
                results = []
                for _, row in df.iterrows():
                    try:
                        raw_dr = str(row[dr_col]).replace('%', '').strip()
                        val_dr = float(raw_dr)
                        if val_dr > 1: val_dr /= 100 
                        status = "✅ رابح" if val_dr >= break_even_dr else "🚨 خاسر"
                        results.append({"المنطقة": row[country_col], "التسليم (DR)": f"{round(val_dr*100, 1)}%", "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%", "الحالة": status})
                    except: continue
                if results: st.table(pd.DataFrame(results))
            except Exception as e: st.error(f"خطأ: {str(e)}")
        else: st.info("ارفع ملف البيانات المالي لعرض التحليل.")
