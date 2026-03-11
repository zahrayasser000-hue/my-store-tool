import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine V36", layout="wide")

def force_clean_html(text):
    """تنظيف النص الخام وتحويله إلى كود HTML قابل للتنفيذ"""
    if not text: return ""
    # 1. إزالة أي نص قبل <!DOCTYPE أو <html
    start_match = re.search(r'<(!DOCTYPE|html)', text, re.IGNORECASE)
    if start_match:
        text = text[start_match.start():]
    # 2. إزالة أي نص بعد </html>
    end_match = re.search(r'</html>', text, re.IGNORECASE)
    if end_match:
        text = text[:end_match.end()]
    # 3. تنظيف علامات الماركداون المعروفة
    text = text.replace("```html", "").replace("```", "").strip()
    return text

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")

# --- 3. المحرك ---
st.header("🚀 ALI Growth Engine - Visual Fix")

if st.button("توليد العرض الاحترافي"):
    if api_key and product_url:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("جاري بناء الصفحة..."):
                # البرومت الصارم لضمان 13 قسم بناءً على SOP-1
                prompt = f"""
                Write a HIGH-CONVERTING Landing Page for {product_url}.
                Framework: Strictly 13 sections (SOP-1).
                Design: Full Tailwind CSS classes, Cairo font, professional images.
                Output: Return ONLY the HTML starting with <!DOCTYPE html>.
                """
                response = model.generate_content(prompt)
                
                # معالجة النتيجة وتخزينها
                st.session_state.v36_html = force_clean_html(response.text)
                st.success("تم التوليد بنجاح!")
        except Exception as e:
            st.error(f"خطأ: {e}")

# --- 4. عرض النتائج (الحل البصري) ---
if 'v36_html' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة البصرية", "💻 كود الصفحة"])
    
    with tab1:
        # إذا كان الكود سليماً، سيظهر هنا كصفحة ويب
        # قمنا بزيادة الارتفاع لضمان عدم ضياع الأقسام
        components.html(st.session_state.v36_html, height=1500, scrolling=True)
        
    with tab2:
        st.code(st.session_state.v36_html, language="html")
