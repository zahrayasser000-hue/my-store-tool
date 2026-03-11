import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import base64

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Engine V29", layout="wide")

# --- 2. نظام الذاكرة الحديدية (Persistence) ---
# هذا الجزء يضمن عدم ضياع البيانات عند أي Rerun
if 'final_html' not in st.session_state: st.session_state.final_html = None
if 'final_strat' not in st.session_state: st.session_state.final_strat = None
if 'be_rate' not in st.session_state: st.session_state.be_rate = 0

# --- 3. محرك العرض الآمن ---
def safe_display(html_content):
    if html_content:
        # تنظيف صارم للكود
        clean = html_content.replace("```html", "").replace("```", "").strip()
        b64 = base64.b64encode(clean.encode('utf-8')).decode('utf-8')
        src = f"data:text/html;base64,{b64}"
        components.iframe(src, height=1200, scrolling=True)

# --- 4. القائمة الجانبية (المدخلات) ---
with st.sidebar:
    st.title("🏗️ ALI Engine V29")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    
    st.divider()
    st.header("💰 الحسابات المالية")
    price = st.number_input("سعر البيع", value=250)
    costs = st.number_input("التكاليف الإجمالية", value=120)
    conf = st.slider("نسبة التأكيد %", 10, 100, 80) / 100
    
    if st.button("🔥 توليد وحفظ البيانات"):
        if api_key and product_url:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                with st.spinner("⏳ جاري العمل... لا تلمس المتصفح"):
                    # توليد الاستراتيجية أولاً
                    strat_res = model.generate_content(f"اكتب استراتيجية Agora وسكريبتات فيديو لمنتج {product_url}")
                    st.session_state.final_strat = strat_res.text
                    
                    # توليد صفحة الهبوط (SOP-1)
                    html_prompt = f"صمم صفحة هبوط 13 قسم (Tailwind CSS) لمنتج {product_url}. ابدأ بـ <html> وانته بـ </html>. لا تكتب نصاً خارج الكود."
                    html_res = model.generate_content(html_prompt)
                    st.session_state.final_html = html_res.text
                    
                    # حساب البريك ايفنت
                    st.session_state.be_rate = round(((costs / (price * conf)) * 100), 2) if (price * conf) > 0 else 0
                    
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
        else:
            st.warning("أدخل البيانات أولاً")

# --- 5. عرض النتائج (Tabs) ---
tab1, tab2, tab3 = st.tabs(["📱 صفحة الهبوط (SOP-1)", "🎯 الاستراتيجية والسكريبتات", "📊 المصفوفة المالية"])

with tab1:
    if st.session_state.final_html:
        st.success("✅ تم التثبيت بنجاح")
        safe_display(st.session_state.final_html)
    else:
        st.info("اضغط على الزر في الجانب لبدء التوليد")

with tab2:
    if st.session_state.final_strat:
        st.markdown(st.session_state.final_strat)

with tab3:
    st.metric("نقطة التعادل (Delivery Rate Required)", f"{st.session_state.be_rate}%")
    st.write(f"يجب أن تكون نسبة التسليم أعلى من **{st.session_state.be_rate}%** لضمان الربح.")

