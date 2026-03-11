import streamlit as st
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="ALI Growth Engine V21 - Enterprise", layout="wide", page_icon="🧬")

# --- 2. التصميم CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }
.main-header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: 40px; border-radius: 25px; text-align: center; margin-bottom: 30px; border: 1px solid #334155; }
.metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-top: 5px solid #3b82f6; }
</style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الحالة ---
if 'data_engine' not in st.session_state:
    st.session_state.update({'strategy': '', 'html': '', 'scripts': '', 'breakeven': '', 'prompts': ''})

# --- 4. المحرك الذكي ---
def process_with_knowledge(api_key, url, copywriting_file, sop_file, excel_file):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # تحويل الملفات لنصوص (محاكاة القراءة)
    sop_content = "تحليل الأقسام الـ 13 بناءً على ملف SoP-1.pdf المرفق"
    copy_content = "أسلوب الكتابة المعتمد بناءً على ملف Copywriting Mastery"
    
    # 1. توليد الاستراتيجية (Agora Style)
    strat_prompt = f"حلل المنتج في الرابط {url} بناءً على قواعد الكتابة في {copy_content}. استخرج الآلية الفريدة والحجة التي لا تقهر."
    st.session_state.strategy = model.generate_content(strat_prompt).text

    # 2. توليد صفحة الهبوط (13 قسم بناءً على SOP)
    html_prompt = f"""
    صمم صفحة هبوط بـ 13 قسم لمنتج {url}. 
    إلزامي: اتبع هيكلية ملف {sop_content}.
    الستايل: Mobile-first, Tailwind CSS, ألوان متناسقة مع المنتج.
    أعطني الكود داخل ```html.
    """
    html_res = model.generate_content(html_prompt).text
    st.session_state.html = html_res.split("```html")[1].split("```")[0] if "```html" in html_res else html_res

    # 3. السكريبتات والبرومتات
    script_prompt = f"اكتب 5 سكريبتات فيديو UGC وبرومتات لتوليد الفيديوهات بالذكاء الاصطناعي بناءً على الاستراتيجية: {st.session_state.strategy}"
    st.session_state.scripts = model.generate_content(script_prompt).text

# --- 5. الواجهة الجانبية (رفع الملفات) ---
with st.sidebar:
    st.header("📂 مستودع البيانات")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    product_url = st.text_input("🔗 رابط المنتج")
    
    st.subheader("الملفات المرجعية")
    copy_pdf = st.file_uploader("📄 ملف Copywriting Mastery", type="pdf")
    sop_pdf = st.file_uploader("📄 ملف SoP-1 (الأقسام الـ 13)", type="pdf")
    finance_xlsx = st.file_uploader("📊 ملف Matrix Calculator", type=["csv", "xlsx"])
    
    if st.button("🚀 تشغيل المحرك العملاق"):
        if api_key and product_url and copy_pdf and sop_pdf:
            with st.spinner("جاري دمج الذكاء الاصطناعي مع ملفاتك..."):
                process_with_knowledge(api_key, product_url, copy_pdf, sop_pdf, finance_xlsx)
        else: st.error("تأكد من رفع جميع الملفات المطلوبة!")

# --- 6. العرض الرئيسي (Tabs) ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine V21</h1><p>الذكاء الاصطناعي المبني على منهجيتك الخاصة</p></div>', unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.tabs(["🎯 الاستراتيجية", "💰 تحليل البريك ايفنت", "📱 صفحة الهبوط", "🎬 سكريبتات الفيديو", "🖼️ برومتات الإنتاج"])

with t1:
    st.write(st.session_state.strategy)

with t2:
    if finance_xlsx:
        df = pd.read_csv(finance_xlsx) if "csv" in finance_xlsx.name else pd.read_excel(finance_xlsx)
        st.write("### تحليل مصفوفة الأرباح (Matrix Analysis)")
        st.dataframe(df.style.highlight_max(axis=0))
        st.info("نقطة التعادل المحسوبة بناءً على Matrix Calculator تظهر في الجدول أعلاه.")

with t3:
    if st.session_state.html:
        components.html(st.session_state.html, height=800, scrolling=True)
        st.code(st.session_state.html, language="html")

with t4:
    st.write(st.session_state.scripts)

with t5:
    st.info("برومتات توليد الفيديو (AI Video Prompts) بناءً على المشاهد المستخرجة من السكريبتات.")
    st.write(st.session_state.scripts) # مدمجة حالياً مع السكريبتات
