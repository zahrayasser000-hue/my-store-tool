import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V26", layout="wide")

# --- 2. الثوابت الصارمة (من ملفاتك) ---
SOP_STRUCTURE = """
1. Hero: Title + Subtitle + Product Image + Primary CTA
2. Trust Bar: 4 Icons (Free Shipping, Original, Safe Pay, Fast Delivery)
3. Problem: Pain point agitation based on PAS.
4. Solution: Introducing the product as the hero.
5. Unique Mechanism: Why this product is different (Agora style).
6. Benefits Grid: 4 Cards with icons.
7. Social Proof: Testimonials/Stars.
8. Risk Reversal: 100% Money back guarantee badge.
9. Sticky CTA: Button at the bottom for mobile.
"""

# --- 3. محرك الحسابات المالية (Break-even Engine) ---
def calculate_break_even(price, cost, shipping, cpl, conf_rate):
    # المعادلة المستخرجة من ملف Matrix الخاص بك
    # الربح = (سعر البيع * نسبة التأكيد * نسبة التسليم) - التكاليف
    # عند البريك ايفنت يكون الربح = 0
    if price * conf_rate == 0: return 0
    needed_delivery = ((cost + shipping + (cpl/conf_rate)) / price) * 100
    return round(needed_delivery, 2)

# --- 4. الواجهة الجانبية ---
with st.sidebar:
    st.header("🔑 التحكم المركزي")
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج")
    
    st.divider()
    st.header("💰 المعطيات المالية (Matrix)")
    p_price = st.number_input("سعر البيع (SAR)", value=250.0)
    p_cost = st.number_input("تكلفة المنتج (SAR)", value=50.0)
    p_shipping = st.number_input("الشحن والتغليف (SAR)", value=35.0)
    p_cpl = st.number_input("تكلفة الليد CPL (SAR)", value=15.0)
    p_conf = st.slider("نسبة التأكيد %", 0, 100, 80) / 100

# --- 5. العرض الرئيسي ---
st.markdown("<h1 style='text-align:center;'>🚀 ALI Growth Engine V26</h1>", unsafe_allow_html=True)

if st.button("🔥 توليد الإمبراطورية التسويقية الآن"):
    if not api_key or not product_url:
        st.error("أدخل المفتاح والرابط أولاً!")
    else:
        with st.spinner("جاري تصميم الصفحة والسكريبتات بناءً على SOP-1..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # برومت صارم جداً لضمان الحصول على كود فقط
            prompt = f"""
            Task: Create a High-Converting Landing Page for: {product_url}
            Framework: Use PAS and FAB from Copywriting Mastery.
            Structure: Build 13 sections exactly following this SOP: {SOP_STRUCTURE}
            Technical: Use Tailwind CSS, Mobile-First (480px width max), Cairo Font.
            Output: You MUST return ONLY the HTML code starting with <!DOCTYPE html> and ending with </html>. No conversational text.
            """
            
            response = model.generate_content(prompt)
            st.session_state.final_html = response.text
            
            # توليد السكريبتات
            script_prompt = f"اكتب 5 سكريبتات فيديو UGC وبرومتات بصرية لمنتج {product_url} بناءً على استراتيجية Agora."
            st.session_state.final_scripts = model.generate_content(script_prompt).text
            
            # حساب البريك ايفنت
            st.session_state.be_rate = calculate_break_even(p_price, p_cost, p_shipping, p_cpl, p_conf)

# --- 6. عرض النتائج الفوري ---
t1, t2, t3 = st.tabs(["📱 معاينة صفحة الهبوط", "🎬 سكريبتات الفيديو", "📊 تحليل البريك ايفنت"])

with t1:
    if 'final_html' in st.session_state:
        # تنظيف الكود من أي زوائد قد يضيفها الموديل
        clean_html = st.session_state.final_html.replace("```html", "").replace("```", "")
        components.html(clean_html, height=800, scrolling=True)
        st.code(clean_html, language="html")

with t2:
    if 'final_scripts' in st.session_state:
        st.markdown(f"```text\n{st.session_state.final_scripts}\n```")

with t3:
    if 'be_rate' in st.session_state:
        st.header("📊 مصفوفة نقطة التعادل")
        col1, col2 = st.columns(2)
        col1.metric("نسبة التسليم المطلوبة (BEP)", f"{st.session_state.be_rate}%")
        col2.info(f"إذا كانت نسبة تسليم طلبياتك في الدولة المستهدفة أقل من {st.session_state.be_rate}% فأنت تخسر مالاً.")
