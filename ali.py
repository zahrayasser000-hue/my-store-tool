import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components

# --- إعدادات الواجهة ---
st.set_page_config(page_title="ALI Growth Engine V25", layout="wide")

# --- برومتات صارمة (مستوحاة من ملفاتك) ---
COPYWRITING_RULES = """
- استخدم إطار PAS (Problem, Agitation, Solution).
- ركز على الفوائد (Benefits) وليس الميزات (Features) بناءً على FAB.
- لغة عربية فصحى بيضاء، عناوين قصيرة وصادمة.
- كسر الاعتراضات قبل ظهورها.
"""

SOP_13_SECTIONS = """
1. Hero (Video/Image + Hook + CTA)
2. Trust Bar (Iconic Trust)
3. Problem (Pain Agitation)
4. Solution (The Savior)
5. Unique Mechanism (Agora Style)
6. Benefits Grid (4 Items)
7. Comparison (Us vs Them)
8. Ingredients/Features
9. Social Proof (UGC Style)
10. Expert Authority
11. How to use (3 Steps)
12. Risk Reversal (Guarantee)
13. Sticky Footer CTA
"""

# --- دالة التوليد ---
def generate_mega_content(api_key, url, p_price, p_cost, ads_cost):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    أنت خبير تسويق استراتيجي. المنتج هو: {url}
    قواعد الكتابة الصارمة: {COPYWRITING_RULES}
    هيكل الصفحة الإلزامي (13 قسم): {SOP_13_SECTIONS}
    
    المطلوب:
    1. كود HTML/CSS (Tailwind) احترافي جداً (Mobile-First).
    2. 5 سكريبتات فيديو UGC وبرومتات بصرية.
    3. تحليل الاستراتيجية.
    أعطني الكود داخل ```html.
    """
    return model.generate_content(prompt).text

# --- الواجهة الرئيسية ---
st.title("🚀 ALI Growth Engine V25: The Hard-Coded Beast")

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    product_url = st.text_input("رابط المنتج")
    st.divider()
    st.header("💰 الحسابات المالية")
    selling_price = st.number_input("ثمن البيع (Price)", value=250.0)
    product_cost = st.number_input("تكلفة المنتج (COGS)", value=50.0)
    shipping_cost = st.number_input("تكلفة الشحن (Shipping)", value=30.0)
    cpl = st.number_input("تكلفة الليد (CPL)", value=15.0)
    conf_rate = st.slider("نسبة التأكيد المتوقعة (%)", 0, 100, 80) / 100

if st.button("🔥 توليد الإمبراطورية التسويقية"):
    if api_key and product_url:
        with st.spinner("جاري التوليد..."):
            # حساب البريك ايفنت
            total_fixed_cost = product_cost + shipping_cost + (cpl / conf_rate)
            be_delivery = (total_fixed_cost / selling_price) * 100
            st.session_state.be_result = round(be_delivery, 2)
            
            # توليد المحتوى
            res = generate_mega_content(api_key, product_url, selling_price, product_cost, cpl)
            if "```html" in res:
                st.session_state.v25_html = res.split("```html")[1].split("```")[0]
                st.session_state.v25_strat = res.split("```")[2] if len(res.split("```")) > 2 else res
            st.success("تم بنجاح!")

# --- العرض ---
t1, t2, t3 = st.tabs(["📱 صفحة الهبوط", "🎬 الاستراتيجية والسكريبتات", "📊 التحليل المالي"])

with t1:
    if 'v25_html' in st.session_state:
        components.html(st.session_state.v25_html, height=900, scrolling=True)

with t2:
    if 'v25_strat' in st.session_state:
        st.write(st.session_state.v25_strat)

with t3:
    if 'be_result' in st.session_state:
        st.metric("نقطة التعادل (Delivery Rate Required)", f"{st.session_state.be_result}%")
        st.write(f"لتحقيق الربح، يجب أن تكون نسبة التسليم لديك أعلى من **{st.session_state.be_result}%**.")
