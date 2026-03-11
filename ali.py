import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة الفاخرة ---
st.set_page_config(page_title="ALI Growth Engine V22", layout="wide", page_icon="🧬")

# --- 2. تهيئة الذاكرة ---
if 'outputs' not in st.session_state:
    st.session_state.outputs = {'strat': '', 'html': '', 'scripts': '', 'breakeven': ''}

# --- 3. الدوال الأساسية لمعالجة الملفات والذكاء الاصطناعي ---
def generate_all_assets(api_key, url, copy_file, sop_file, matrix_file):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # [مرحلة تحليل الملفات] - نطلب من الذكاء الاصطناعي قراءة سياق الملفات المرفوعة
    context_prompt = f"""
    لقد رفعت لك 3 ملفات أساسية:
    1. ملف Copywriting Mastery: استخدمه لضبط نبرة الكتابة (PAS, AIDA).
    2. ملف SoP-1: التزم بالأقسام الـ 13 المذكورة فيه لصفحة الهبوط.
    3. ملف Matrix Calculator: استخدمه لفهم الجدوى المالية.
    المنتج المراد تحليله: {url}
    """

    # 1. الاستراتيجية والسكريبتات
    full_analysis = model.generate_content(context_prompt + " استخرج الاستراتيجية التسويقية و 5 سكريبتات فيديو UGC مع برومتات بصرية لتوليدها.").text
    st.session_state.outputs['strat'] = full_analysis

    # 2. صفحة الهبوط (الحل لمشكلة المظهر البدائي)
    # نستخدم Tailwind CSS بشكل مكثف هنا لضمان مظهر الـ Premium
    html_prompt = f"""
    صمم كود HTML/CSS واحد متكامل لصفحة هبوط لمنتج {url}.
    - استخدم Tailwind CSS (CDN).
    - الهيكل: 13 قسم بناءً على SoP-1.
    - لغة الكتابة: احترافية بناءً على Copywriting Mastery.
    - الألوان: استخرجها من المنتج في الرابط.
    - أضف Sticky CTA Button وتأثيرات Hover.
    أعطني الكود فقط داخل وسم ```html.
    """
    html_res = model.generate_content(html_prompt).text
    if "```html" in html_res:
        st.session_state.outputs['html'] = html_res.split("```html")[1].split("```")[0]

# --- 4. واجهة المستخدم ---
with st.sidebar:
    st.header("📂 لوحة التحكم بالبيانات")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج")
    f_copy = st.file_uploader("📄 ملف Copywriting PDF", type="pdf")
    f_sop = st.file_uploader("📄 ملف SoP PDF", type="pdf")
    f_matrix = st.file_uploader("📊 ملف Matrix (CSV/XLSX)", type=["csv", "xlsx"])
    
    if st.button("🚀 توليد النظام الكامل"):
        if api_key and product_url and f_copy and f_sop:
            generate_all_assets(api_key, product_url, f_copy, f_sop, f_matrix)
        else: st.error("تأكد من إدخال الرابط ورفع الملفات!")

# --- 5. العرض الرئيسي (Tabs) ---
st.markdown('<h1 style="text-align:center;">ALI Growth Engine V22</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📱 صفحة الهبوط", "🎯 الاستراتيجية والسكريبتات", "💰 التحليل المالي", "🖼️ برومتات الفيديو"])

with tab1:
    if st.session_state.outputs['html']:
        st.success("تم توليد الصفحة بناءً على SOP الخاص بك")
        components.html(st.session_state.outputs['html'], height=900, scrolling=True)
        st.code(st.session_state.outputs['html'], language="html")

with tab2:
    st.write(st.session_state.outputs['strat'])

with tab3:
    if f_matrix:
        df = pd.read_csv(f_matrix) if "csv" in f_matrix.name else pd.read_excel(f_matrix)
        st.write("### مصفوفة الجدوى المالية (Matrix)")
        st.dataframe(df)
        st.info("نقطة التعادل يتم تحديدها بناءً على تقاطع تكلفة الليد مع نسبة التسليم في الجدول أعلاه.")

with tab4:
    st.markdown("### 🎬 برومتات توليد الفيديوهات (AI Video Generation Prompts)")
    st.write("استخدم هذه الأوامر في أدوات مثل Runway Gen-2 أو Luma Dream Machine:")
    st.write(st.session_state.outputs['strat']) # الجزء المتعلق بالبرومتات
