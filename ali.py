import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine V35 - Visual Fix", layout="wide")

def clean_html_for_display(raw_text):
    """وظيفة حاسمة لتحويل النص إلى صفحة ويب حقيقية"""
    # إزالة أي نصوص توضيحية قد يضيفها Gemini في البداية
    clean = re.sub(r'^.*?<!DOCTYPE', '<!DOCTYPE', raw_text, flags=re.DOTALL | re.IGNORECASE)
    # إزالة علامات الماركداون البرمجية
    clean = clean.replace("```html", "").replace("```", "").strip()
    return clean

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    st.info("💡 تأكد من تشغيل الـ VPN كما فعلت الآن لأن الاتصال نجح!")

# --- 3. المحرك ---
if st.button("🚀 توليد العرض البصري النهائي"):
    if api_key and product_url:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("⏳ جاري تحويل البيانات إلى تصميم احترافي..."):
                # نطلب منه الالتزام بـ SOP-1 و Tailwind
                prompt = f"""
                Create a high-converting Landing Page for: {product_url}
                Framework: 13 sections (SOP-1).
                Design: Use Tailwind CSS, Cairo Font, High-end visuals.
                Important: Return ONLY the raw HTML code.
                """
                response = model.generate_content(prompt)
                
                # تخزين وتنظيف الكود
                st.session_state.v35_html = clean_html_for_display(response.text)
                st.success("✅ تم بناء التصميم بنجاح!")
        except Exception as e:
            st.error(f"خطأ: {e}")

# --- 4. العرض (هنا يكمن الحل) ---
if 'v35_html' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية الاحترافية", "💻 الكود المصدري"])
    
    with tab1:
        st.markdown("### المعاينة المباشرة (Mobile View)")
        # استخدام iframe بعرض مخصص للموبايل لضمان ظهور الـ 13 قسم بشكل صحيح
        components.html(st.session_state.v35_html, height=1200, scrolling=True)
        
    with tab2:
        st.code(st.session_state.v35_html, language="html")
