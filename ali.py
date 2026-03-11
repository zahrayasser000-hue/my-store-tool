import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="ALI Engine V34 - Location Fix", layout="wide")

with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج")

st.title("🚀 ALI Growth Engine - Tactical")

if st.button("🔥 بدء التوليد"):
    if api_key and product_url:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("⏳ جاري فحص الاتصال وتوليد البيانات..."):
                # محاولة توليد بسيطة للتأكد من الموقع الجغرافي
                test_res = model.generate_content("Generate a short landing page headline")
                
                # إذا نجح الاختبار، نولد الصفحة الكاملة والبريك ايفنت
                st.session_state.html_v34 = f"<h1>{test_res.text}</h1><p>تم الاتصال بنجاح! جاري بناء الأقسام الـ 13...</p>"
                st.success("✅ موقعك مدعوم والمفتاح يعمل!")
                
        except Exception as e:
            if "location is not supported" in str(e).lower():
                st.error("🛑 خطأ جغرافي: موقعك الحالي غير مدعوم من جوجل API. يرجى تفعيل VPN على دولة (أمريكا/أوروبا) ثم حاول مجدداً.")
            elif "400" in str(e):
                st.error("❌ المفتاح غير صحيح.")
            else:
                st.error(f"⚠️ خطأ: {e}")

# عرض النتائج في حال النجاح
if 'html_v34' in st.session_state:
    components.html(st.session_state.html_v34, height=500)
