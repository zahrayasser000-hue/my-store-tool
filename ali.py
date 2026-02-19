import streamlit as st
import pandas as pd
import google.generativeai as genai
import PyPDF2
from PIL import Image
import time

# --- 1. إعدادات الصفحة ---
USER_NAME = "ALI"
TOOL_NAME = f"{USER_NAME} Growth Engine"
TOOL_VERSION = "6.6 (Arabic Force)"

st.set_page_config(page_title=TOOL_NAME, layout="wide", page_icon="☪️", initial_sidebar_state="expanded")

# --- 2. التصميم (CSS - الإصلاح الشامل) ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

/* 1. القواعد العامة للصفحة (عربي) */
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], 
div, p, span, h1, h2, h3, h4, h5, h6, li, button {
    font-family: 'Tajawal', 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* 2. القائمة الجانبية */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

[data-testid="stSidebar"] input, 
[data-testid="stSidebar"] textarea, 
[data-testid="stSidebar"] select {
    color: #1a1a2e !important;       
    background-color: #ffffff !important; 
    border: 2px solid #667eea !important; 
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    text-align: center !important;
}

[data-testid="stSidebar"] .stNumberInput input {
    color: #1a1a2e !important;
    background: #ffffff !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    text-align: center !important;
}

/* 3. الهيدر والمربعات */
.main-header {
    background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
    color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
.main-header h1 { color: white !important; }

.metric-box {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    direction: rtl;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.metric-value { font-size: 28px; font-weight: 900; color: #4b6cb7; }
.metric-label { font-size: 14px; color: #666; font-weight: bold; }

/* 🛑 4. إصلاح الجدول (توسط كامل) 🛑 */
[data-testid="stDataFrame"], .stDataFrame {
    direction: ltr !important; 
}
[data-testid="stDataFrame"] div[data-testid="stTable"] div[role="columnheader"],
[data-testid="stDataFrame"] div[data-testid="stTable"] div[role="gridcell"] {
    text-align: center !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] div[data-testid="stTable"] div[role="columnheader"] {
    background-color: #f0f2f6 !important;
    color: #4b6cb7 !important;
    font-size: 17px !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- 3. الدوال ---
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df.columns = [str(c).strip() for c in df.columns]
        return df, None
    except Exception as e: return None, str(e)

def extract_pdf_text(file):
    if file:
        try:
            reader = PyPDF2.PdfReader(file)
            return "".join([p.extract_text() for p in reader.pages])
        except: return ""
    return ""

def find_working_model(api_key):
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in models: 
            if "flash" in m: return m
        for m in models:
            if "pro" in m: return m
        return models[0] if models else None
    except: return None

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align: center;'>☪️ {USER_NAME} V6.6</h1>", unsafe_allow_html=True)
    api_key = st.text_input("🔑 مفتاح Google API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🛍️ بيانات المنتج")
    product_name = st.text_input("اسم المنتج")
    product_link = st.text_input("رابط المنتج")
    product_img_file = st.file_uploader("صورة المنتج", type=['png', 'jpg', 'jpeg'])

    st.markdown("---")
    with st.expander("💰 المتغيرات المالية", expanded=True):
        P = st.number_input("سعر البيع (P)", value=250.0)
        C = st.number_input("تكلفة المنتج (C)", value=50.0)
        CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    
    st.markdown("---")
    uploaded_excel = st.file_uploader("ملف البيانات", type=['xlsx', 'csv'])
    uploaded_sop = st.file_uploader("ملف SOP", type=['pdf'])
    uploaded_copy = st.file_uploader("ملف Copywriting", type=['pdf'])
    
    manual_notes = st.text_area("✍️ ملاحظات يدوية")
    run_btn = st.button("🚀 تحميل المحرك")

# --- 5. الواجهة الرئيسية ---
st.markdown(f"""
<div class="main-header">
    <h1>{TOOL_NAME}</h1>
    <p>تم إجبار النتائج على اللغة العربية</p>
</div>
""", unsafe_allow_html=True)

# حساب نقطة التعادل
try:
    margin_per_sale = 0.95 * P - C - 4
    if margin_per_sale <= 0:
        global_be_text = "مستحيل (خسارة)"
        global_be_val = 1000
    else:
        numerator = 3800 * CPL + 11755.30
        denominator = 2470 * margin_per_sale
        global_be_val = numerator / denominator
        global_be_text = f"{round(global_be_val * 100, 2)}%"
except:
    global_be_text = "-"
    global_be_val = 0

# المربعات العلوية
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="metric-box"><div class="metric-label">سعر البيع</div><div class="metric-value">{P}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-box"><div class="metric-label">هامش الربح</div><div class="metric-value">{round(margin_per_sale, 2)}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-box" style="border-color: #dc3545; background: #fff5f5;"><div class="metric-label">نقطة التعادل (BEP)</div><div class="metric-value" style="color: #dc3545;">{global_be_text}</div></div>', unsafe_allow_html=True)

if run_btn or (api_key and uploaded_excel):
    if not uploaded_excel: st.warning("الرجاء رفع ملف Excel"); st.stop()

    df, err = load_data(uploaded_excel)
    if err: st.error(err); st.stop()

    model = None
    if api_key:
        m_name = find_working_model(api_key)
        if m_name: 
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(m_name)
    
    sop_txt = extract_pdf_text(uploaded_sop)
    copy_txt = extract_pdf_text(uploaded_copy)
    img_data = None
    if product_img_file:
        try: img_data = Image.open(product_img_file)
        except: pass

    col1, col2 = st.columns(2)
    with col1: country_col = st.selectbox("عمود الدولة", df.columns)
    with col2: delivery_col = st.selectbox("عمود معدل التسليم", df.columns)

    def ask_ai(prompt, image=None):
        try:
            content = [prompt]
            if image and model and ("vision" in model.model_name or "flash" in model.model_name):
                 content.append(image)
            return model.generate_content(content).text
        except Exception as e: return f"خطأ: {str(e)}"

    tabs = st.tabs(["💰 المالية", "🧠 الاستراتيجية", "🕵️ المنافسين", "📄 صفحة الهبوط", "🎬 السكربتات"])

    # 1. المالية
    with tabs[0]:
        st.markdown('<div class="card"><h3>📊 الجدول المالي</h3>', unsafe_allow_html=True)
        results = []
        for idx, row in df.iterrows():
            try:
                raw = str(row[delivery_col]).replace('%', '').strip()
                if not raw or raw.lower() == 'nan': continue
                dr = float(raw)
                if dr > 1: dr = dr / 100
                
                profit = (2470 * dr * margin_per_sale) - (3800 * CPL) - 11755.30
                status = "✅ رابح" if dr >= global_be_val else "🚨 خاسر"
                
                results.append({
                    "الدولة": row[country_col],
                    "معدل التسليم (DR)": f"{round(dr*100, 1)}%",
                    "صافي الربح": round(profit, 2),
                    "الوضعية": status
                })
            except: continue
        
        final_df = pd.DataFrame(results)
        st.dataframe(final_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. الاستراتيجية (بالعربية)
    with tabs[1]:
        st.markdown('<div class="card"><h3>🧠 تحليل الجمهور</h3>', unsafe_allow_html=True)
        if st.button("🧠 تحليل الجمهور"):
            if product_name and model:
                # 🛑 هنا التعديل: إجبار اللغة العربية 🛑
                prompt = f"""
                أنت خبير تسويق عربي. المنتج: {product_name}. الرابط: {product_link}.
                بناءً على ملف Copywriting: {copy_txt[:2000]}
                حلل جمهور هذا المنتج.
                ⚠️ هام جداً: اكتب التحليل باللغة العربية الفصحى فقط. لا تستخدم الفرنسية أو الإنجليزية.
                """
                with st.spinner("جاري التحليل بالعربية..."):
                    st.markdown(ask_ai(prompt, img_data))
            else: st.warning("تأكد من اسم المنتج و API Key")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. المنافسين (بالعربية)
    with tabs[2]:
        st.markdown('<div class="card"><h3>🕵️ المنافسين</h3>', unsafe_allow_html=True)
        if st.button("🕵️ كشف المنافسين"):
            if model:
                # 🛑 هنا التعديل: إجبار اللغة العربية 🛑
                prompt = f"""
                المنتج: {product_name}. الملاحظات: {manual_notes}.
                استخرج نقاط ضعف المنافسين.
                ⚠️ اكتب التقرير باللغة العربية فقط.
                """
                with st.spinner("تحليل بالعربية..."):
                    st.markdown(ask_ai(prompt))
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. صفحة الهبوط (بالعربية)
    with tabs[3]:
        st.markdown('<div class="card"><h3>📄 صفحة الهبوط</h3>', unsafe_allow_html=True)
        if st.button("📄 تصميم الصفحة"):
            if product_name and model:
                # 🛑 هنا التعديل: إجبار اللغة العربية 🛑
                prompt = f"""
                صمم محتوى صفحة هبوط لمنتج: {product_name}.
                استخدم هيكل الـ SOP التالي: {sop_txt[:2000]}
                ⚠️ التعليمات:
                1. اكتب المحتوى باللغة العربية المشوقة (يمكن استخدام اللهجة البيضاء).
                2. العناوين يجب أن تكون جذابة بالعربية.
                3. ممنوع استخدام الفرنسية نهائياً.
                """
                with st.spinner("تصميم الصفحة بالعربية..."):
                    st.markdown(ask_ai(prompt, img_data))
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. السكربتات (بالعربية)
    with tabs[4]:
        st.markdown('<div class="card"><h3>🎬 السكربتات</h3>', unsafe_allow_html=True)
        if st.button("🎬 كتابة السكربتات"):
            if product_name and model:
                # 🛑 هنا التعديل: إجبار اللغة العربية 🛑
                prompt = f"""
                اكتب 5 سكربتات إعلانية (UGC / TikTok) لمنتج {product_name}.
                ⚠️ الشرط: السكربتات يجب أن تكون باللغة العربية (أو اللهجة الدارجة المفهومة) فقط.
                لا تكتب أي كلمة بالفرنسية.
                """
                with st.spinner("كتابة السكربتات بالعربية..."):
                    st.markdown(ask_ai(prompt, img_data))
        st.markdown('</div>', unsafe_allow_html=True)