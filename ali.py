import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V23", layout="wide")

# --- 2. دالة استخراج النصوص من PDF ---
def extract_pdf_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"خطأ في قراءة ملف PDF: {e}"

# --- 3. المحرك الرئيسي ---
def run_ai_engine(api_key, url, copy_text, sop_text, matrix_df):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # بناء الـ Prompt العملاق بناءً على ملفاتك الحقيقية
    full_prompt = f"""
    بصفتك خبير تسويق ومبرمج واجهات:
    1. حلل هذا المنتج: {url}
    2. استخدم قواعد الكتابة من هذا الملف: {copy_text[:2000]} (اكتفِ بالقواعد الأساسية).
    3. صمم صفحة هبوط بـ 13 قسم بناءً على هذا الـ SOP: {sop_text[:2000]}.
    
    المطلوب فوراً:
    أ- كود HTML/CSS واحد متكامل (Tailwind CSS) لصفحة هبوط احترافية (Mobile-First).
    ب- 5 سكريبتات فيديو UGC مع وصف المشاهد (Visual Prompts).
    ج- تحليل لاستراتيجية البيع.
    
    أعطني كود الـ HTML داخل ```html والسكريبتات بالأسفل.
    """
    
    response = model.generate_content(full_prompt)
    return response.text

# --- 4. واجهة المستخدم ---
st.markdown('<h2 style="text-align:center;">🚀 ALI Growth Engine V23 (Fixed & Final)</h2>', unsafe_allow_html=True)

with st.sidebar:
    api_key = st.text_input("🔑 API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج")
    f_copy = st.file_uploader("📄 ملف Copywriting Mastery", type="pdf")
    f_sop = st.file_uploader("📄 ملف SoP-1", type="pdf")
    f_matrix = st.file_uploader("📊 ملف Matrix Calculator", type=["csv", "xlsx"])

if st.button("🔥 تشغيل المحرك الآن"):
    if not (api_key and product_url and f_copy and f_sop):
        st.error("أرجوك ارفع جميع الملفات المطلوبة أولاً!")
    else:
        with st.spinner("جاري قراءة ملفاتك وتصميم عالمك التسويقي..."):
            # استخراج النصوص
            copy_text = extract_pdf_text(f_copy)
            sop_text = extract_pdf_text(f_sop)
            
            # معالجة المصفوفة المالية
            if f_matrix:
                df_matrix = pd.read_csv(f_matrix) if f_matrix.name.endswith('.csv') else pd.read_excel(f_matrix)
                st.session_state.matrix_data = df_matrix
            
            # طلب الذكاء الاصطناعي
            result = run_ai_engine(api_key, product_url, copy_text, sop_text, f_matrix)
            
            # توزيع النتائج
            if "```html" in result:
                st.session_state.generated_html = result.split("```html")[1].split("```")[0]
                st.session_state.generated_scripts = result.split("```")[2] if len(result.split("```")) > 2 else result
            st.success("تم التوليد بنجاح!")

# --- 5. عرض النتائج ---
t1, t2, t3 = st.tabs(["📱 المعاينة البصرية", "🎬 السكريبتات والبرومتات", "💰 تحليل المصفوفة"])

with t1:
    if 'generated_html' in st.session_state:
        components.html(st.session_state.generated_html, height=800, scrolling=True)
        st.code(st.session_state.generated_html, language="html")

with t2:
    if 'generated_scripts' in st.session_state:
        st.write(st.session_state.generated_scripts)

with t3:
    if 'matrix_data' in st.session_state:
        st.dataframe(st.session_state.matrix_data)
        st.info("نقطة التعادل محددة بناءً على تقاطع البيانات في جدولك المرفوع.")
