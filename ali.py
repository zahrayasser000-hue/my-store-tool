import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="ALI Engine - Final Fix", layout="wide")

# دالة تنظيف الكود لضمان عدم وجود فراغ
def clean_html(text):
    if not text: return ""
    # إزالة علامات الماركداون
    text = re.sub(r'```html', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    return text.strip()

with st.sidebar:
    st.title("🛠️ الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج (URL)")

st.title("🚀 ALI Growth Engine")

if st.button("توليد صفحة الهبوط"):
    if api_key and product_url:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
                prompt = f"Create a full landing page HTML with Tailwind CSS for this product: {product_url}. Return ONLY the HTML code starting with <!DOCTYPE html>."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.session_state.html_content = clean_html(response.text)
                    st.success("✅ تم التوليد بنجاح!")
                else:
                    st.error("❌ الذكاء الاصطناعي لم يرجع أي محتوى.")
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
    else:
        st.warning("⚠️ أدخل المفتاح والرابط")

# عرض النتائج
if 'html_content' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة الحية", "💻 الكود المصدري"])
    
    with tab1:
        # إذا كان الكود موجود ولكنه لا يظهر، سنعرف السبب هنا
        if st.session_state.html_content:
            components.html(st.session_state.html_content, height=1000, scrolling=True)
        else:
            st.warning("المحتوى فارغ، حاول التوليد مرة أخرى.")
            
    with tab2:
        st.code(st.session_state.html_content, language="html")
