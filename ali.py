import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="ALI Engine - Original V1", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. دالة التوليد الأصلية ---
def generate_original_lp(api_key, product_url):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        أنت خبير تصميم صفحات هبوط ومسوق محترف.
        المطلوب: برمجة صفحة هبوط كاملة لمنتج من هذا الرابط: {product_url}
        
        المواصفات:
        - استخدم Tailwind CSS.
        - التصميم Mobile-First.
        - الألوان: يجب أن تكون متناسقة تماماً مع ألوان المنتج في الرابط.
        - الأقسام: Hero, Problem, Solution, Features, Testimonials, CTA.
        - الخط: Cairo.
        
        أعطني كود HTML فقط، بدون أي نصوص إضافية.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. واجهة المستخدم ---
st.title("🚀 ALI Growth Engine - النسخة الأصلية")

with st.sidebar:
    st.header("الإعدادات")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج (URL)")

if st.button("توليد الصفحة"):
    if api_key and product_url:
        with st.spinner("جاري التوليد..."):
            raw_result = generate_original_lp(api_key, product_url)
            
            # تنظيف الكود من علامات الماركداون لضمان العرض
            clean_html = raw_result.replace("```html", "").replace("```", "").strip()
            st.session_state.original_html = clean_html
            st.success("تم التوليد!")
    else:
        st.warning("يرجى إدخال API Key والرابط.")

# --- 4. عرض النتائج ---
if 'original_html' in st.session_state:
    tab1, tab2 = st.tabs(["📱 المعاينة", "💻 الكود"])
    
    with tab1:
        # عرض الصفحة داخل Iframe
        components.html(st.session_state.original_html, height=800, scrolling=True)
        
    with tab2:
        st.code(st.session_state.original_html, language="html")
