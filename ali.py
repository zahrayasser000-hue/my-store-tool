import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V12.1", layout="wide", page_icon="https://i.postimg.cc/xCt20gWj/image.png")

# --- 2. التصميم (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}
.main-header { background: #182848; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
.image-prompt-box { background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ffbd45; }
.stDataFrame div[data-testid="stTable"] { direction: ltr !important; }
.stDataFrame td, .stDataFrame th { text-align: center !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة (لمنع اختفاء النتائج) ---
if 'html_code' not in st.session_state: st.session_state.html_code = ""
if 'image_prompts' not in st.session_state: st.session_state.image_prompts = []
if 'video_scripts' not in st.session_state: st.session_state.video_scripts = ""
if 'marketing_strategy' not in st.session_state: st.session_state.marketing_strategy = ""
if 'active_model' not in st.session_state: st.session_state.active_model = None

# --- 4. دوال الذكاء الاصطناعي (مع الرادار التلقائي لمعالجة خطأ 404) ---
def get_working_model(api_key):
    # إذا كان قد وجد الموديل مسبقاً، استخدمه فوراً لتسريع الأداة
    if st.session_state.active_model: return st.session_state.active_model
    
    try:
        genai.configure(api_key=api_key)
        # البحث التلقائي عن الموديل المتاح في حسابك
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name.lower():
                    st.session_state.active_model = m.name
                    return m.name
        st.session_state.active_model = "gemini-pro"
        return "gemini-pro"
    except:
        return "gemini-pro" # الخطة البديلة الآمنة جداً

def generate_html_page(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير برمجة واجهات ومسوق إلكتروني.
        المطلوب: برمجة صفحة هبوط كاملة (HTML & CSS مدمج) لمنتج: {product_name}.
        1. لغة الصفحة: العربية (RTL) بخط 'Cairo'.
        2. التصميم: حديث وسريع التجاوب (Responsive).
        3. الأقسام: Hero Section مع صورة مؤقتة، 4 فوائد، 3 تقييمات خليجية، زر عائم للطلب.
        ⚠️ شرط صارم: أعطني فقط كود الـ HTML والـ CSS الكامل داخل علامتي ```html و ```."""
        response = model.generate_content(prompt)
        code = response.text
        if "```html" in code: code = code.split("```html")[1].split("```")[0]
        elif "```" in code: code = code.split("```")[1]
        return code.strip()
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات (Prompts) احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. صورة الهيرو (Hero Shot)
        2. صورة نمط الحياة (Lifestyle Shot)
        3. صورة تفصيلية (Macro Shot)
        افصل بينها بـ: "---PROMPT_SEPARATOR---" """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

def ask_ai(api_key, prompt):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"أجب بالعربية الفصحى فقط: {prompt}")
        return response.text
    except Exception as e: return f"خطأ في الاتصال: {str(e)}"

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V12.1")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل (المالية)", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - الأتمتة الكاملة (مستقر)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["📄 صفحة الهبوط", "🎬 سكريبتات الفيديو", "🖼️ استوديو الصور", "🎯 الاستراتيجية", "💰 التحليل المالي"])
    
    # --- التبويب 1: صفحة الهبوط ---
    with tabs[0]:
        st.subheader("بناء صفحة الهبوط (HTML)")
        if st.button("🚀 توليد/تحديث صفحة الهبوط"):
            if product_name:
                with st.spinner("الرادار يبحث عن الموديل المناسب... جاري برمجة الصفحة..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
            
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة!")
            components.html(st.session_state.html_code, height=500, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    # --- التبويب 2: سكريبتات الفيديو ---
    with tabs[1]:
        st.subheader("توليد 5 سكريبتات للفيديوهات الترويجية (UGC)")
        if st.button("🎬 توليد السكريبتات الـ 5"):
            if product_name:
                with st.spinner("جاري كتابة السكريبتات..."):
                    prompt = f"""أنت خبير محتوى تسويقي. اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
                    خصص كل سكريبت لمنصة مختلفة: 1. تيك توك، 2. انستجرام ريلز، 3. يوتيوب شورتس، 4. سناب شات، 5. فيسبوك.
                    لكل سكريبت حدد: المشهد البصري، التعليق الصوتي (Voiceover)، والنص المكتوب على الشاشة. ركز على الثواني الأولى (Hook)."""
                    st.session_state.video_scripts = ask_ai(api_key, prompt)
            else: st.error("أدخل اسم المنتج أولاً!")
            
        if st.session_state.video_scripts:
            st.markdown(st.session_state.video_scripts)

    # --- التبويب 3: استوديو الصور ---
    with tabs[2]:
        st.subheader("أوامر توليد الصور (لنانو بنانا)")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج أولاً!")
            
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            st.markdown(f'<div class="image-prompt-box"><strong>1️⃣ Hero Shot:</strong><br>{st.session_state.image_prompts[0]}</div>', unsafe_allow_html=True)
            st.code(st.session_state.image_prompts[0], language="text")
            st.markdown(f'<div class="image-prompt-box"><strong>2️⃣ Lifestyle Shot:</strong><br>{st.session_state.image_prompts[1]}</div>', unsafe_allow_html=True)
            st.code(st.session_state.image_prompts[1], language="text")
            st.markdown(f'<div class="image-prompt-box"><strong>3️⃣ Macro Shot:</strong><br>{st.session_state.image_prompts[2]}</div>', unsafe_allow_html=True)
            st.code(st.session_state.image_prompts[2], language="text")

    # --- التبويب 4: الاستراتيجية ---
    with tabs[3]:
        st.subheader("الاستراتيجية التسويقية")
        if st.button("🎯 توليد الاستراتيجية"):
            if product_name:
                with st.spinner("جاري التفكير..."):
                    st.session_state.marketing_strategy = ask_ai(api_key, f"اعطني استراتيجية تسويق لمنتج {product_name} للسوق الخليجي.")
            else: st.error("أدخل اسم المنتج أولاً!")
            
        if st.session_state.marketing_strategy:
            st.markdown(st.session_state.marketing_strategy)

    # --- التبويب 5: التحليل المالي ---
    with tabs[4]:
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                
                break_even_dr = (C + CPL) / P
                st.info(f"💡 نقطة التعادل المحسوبة: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")

                col_a, col_b = st.columns(2)
                with col_a: country_col = st.selectbox("عمود الدولة/المنطقة:", df.columns)
                with col_b: dr_col = st.selectbox("عمود نسبة التسليم (DR):", df.columns)
                
                results = []
                for _, row in df.iterrows():
                    try:
                        raw_dr = str(row[dr_col]).replace('%', '').strip()
                        val_dr = float(raw_dr)
                        if val_dr > 1: val_dr /= 100 
                        
                        status = "✅ رابح" if val_dr >= break_even_dr else "🚨 خاسر"
                        results.append({
                            "المنطقة": row[country_col],
                            "التسليم (DR)": f"{round(val_dr*100, 1)}%",
                            "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%",
                            "الحالة": status
                        })
                    except: continue

                if results:
                    st.table(pd.DataFrame(results))
            except Exception as e:
                st.error(f"خطأ في قراءة ملف البيانات: {str(e)}")
        else:
            st.info("ارفع ملف البيانات المالي لعرض التحليل. بيانات الأقسام الأخرى محفوظة ولن تختفي.")
