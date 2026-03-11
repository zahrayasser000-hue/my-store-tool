clean_code = clean_code.replace('```', '').strip()
        
        # استخراج كود الـ HTML فقط في حال كتب الذكاء الاصطناعي أي مقدمات
        match = re.search(r'(<!DOCTYPE.*?>)?\s*<html.*?>.*?</html>', clean_code, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).strip()
        
        return clean_code
    except Exception as e: return f"<h3>خطأ في التوليد: {str(e)}</h3>"

def generate_video_scripts(api_key, product_name, strategy_text):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""أنت خبير محتوى تسويقي و Copywriter محترف. 
        اكتب 5 سكريبتات مفصلة لفيديوهات (UGC) قصيرة لمنتج: {product_name}.
        المنصات: تيك توك، انستجرام ريلز، يوتيوب شورتس، سناب شات، فيسبوك.
        🧠 **اعتمد في كتابتك على هذه الاستراتيجية:** {strategy_text}
        ⚠️ الإطار الإلزامي: (AIDA). ركز على المشكلة في أول 3 ثواني، والنتيجة العاطفية في المنتصف."""
        return model.generate_content(prompt).text
    except Exception as e: return f"خطأ: {str(e)}"

def generate_image_prompts(api_key, product_name):
    try:
        model_name = get_working_model(api_key)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""اكتب 3 برومتات احترافية باللغة الإنجليزية لتوليد صور لمنتج: "{product_name}".
        1. Hero Shot
        2. Lifestyle Shot
        3. Macro Shot
        افصل بينها بـ: "---PROMPT_SEPARATOR---" """
        response = model.generate_content(prompt)
        prompts = response.text.split("---PROMPT_SEPARATOR---")
        return [p.strip() for p in prompts if p.strip()]
    except: return []

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ محرك علي V19.0")
    api_key = st.text_input("🔑 API Key", type="password")
    product_name = st.text_input("📦 اسم المنتج")
    product_color = st.text_input("🎨 ألوان المنتج (لتنسيق الصفحة)", placeholder="مثال: أسود مطفي وذهبي")
    
    st.markdown("---")
    st.markdown("### 💰 إعدادات المالية (نقطة التعادل)")
    P = st.number_input("سعر البيع (P)", value=250.0)
    C = st.number_input("التكلفة (C)", value=50.0)
    CPL = st.number_input("تكلفة الليد (CPL)", value=15.0)
    uploaded_file = st.file_uploader("📊 ارفع ملف الإكسل", type=['xlsx', 'csv'])

# --- 6. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>ALI Growth Engine - CRO Optimized (V19)</h1></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("الرجاء إدخال API Key في القائمة الجانبية للبدء.")
else:
    tabs = st.tabs(["🎯 الاستراتيجية", "📱 صفحة الهبوط (13 قسم)", "🎬 سكريبتات الفيديو", "🖼️ استوديو الصور", "💰 التحليل المالي"])
    
    with tabs[0]:
        st.subheader("دراسة السوق وبناء الحجة (Agora)")
        if st.button("🧠 استخراج الاستراتيجية"):
            if product_name:
                with st.spinner("جاري التحليل واستخراج الآلية الفريدة..."):
                    st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.marketing_strategy:
            st.text_area("نتائج الاستراتيجية (قابلة للنسخ والتمرير):", value=st.session_state.marketing_strategy, height=400)

    with tabs[1]:
        st.subheader("بناء صفحة هبوط بصرية بـ 13 قسم متوافق مع الهوية والاستراتيجية")
        if st.button("🚀 توليد الصفحة المتكاملة"):
            if product_name:
                color_theme = product_color if product_color else "ألوان عصرية احترافية وجذابة تناسب المنتج"
                
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس لتصميم الصفحة..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                
                with st.spinner("جاري دمج الاستراتيجية وبرمجة الأقسام الـ 13..."):
                    st.session_state.html_code = generate_html_page(api_key, product_name, st.session_state.marketing_strategy, color_theme)
            else: st.error("أدخل اسم المنتج!")
        
        if st.session_state.html_code:
            st.success("✅ الصفحة جاهزة! تم دمج الاستراتيجية التسويقية بنجاح مع الأقسام الـ 13.")
            components.html(st.session_state.html_code, height=750, scrolling=True)
            with st.expander("💻 عرض كود الـ HTML للنسخ"):
                st.code(st.session_state.html_code, language='html')

    with tabs[2]:
        st.subheader("توليد 5 سكريبتات فيديو")
        if st.button("🎬 توليد السكريبتات"):
            if product_name:
                if not st.session_state.marketing_strategy:
                    with st.spinner("جاري بناء الاستراتيجية كأساس للسكريبتات..."):
                        st.session_state.marketing_strategy = generate_strategy(api_key, product_name)
                        
                with st.spinner("جاري كتابة السكريبتات التسويقية..."):
                    st.session_state.video_scripts = generate_video_scripts(api_key, product_name, st.session_state.marketing_strategy)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.video_scripts:
            st.text_area("السكريبتات الـ 5 (قابلة للنسخ والتمرير):", value=st.session_state.video_scripts, height=500)

    with tabs[3]:
        st.subheader("أوامر توليد الصور")
        if st.button("🖼️ توليد البرومتات"):
            if product_name:
                with st.spinner("المخرج الفني يعمل..."):
                    st.session_state.image_prompts = generate_image_prompts(api_key, product_name)
            else: st.error("أدخل اسم المنتج!")
        if st.session_state.image_prompts and len(st.session_state.image_prompts) >= 3:
            for i, p in enumerate(st.session_state.image_prompts):
                st.markdown(f'<div class="image-prompt-box"><strong>البرومت {i+1}:</strong><br>{p}</div>', unsafe_allow_html=True)

    with tabs[4]:
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                break_even_dr = (C + CPL) / P
                st.info(f"💡 نقطة التعادل المحسوبة: **{round(break_even_dr * 100, 2)}%** من نسبة التسليم (DR).")
                col_a, col_b = st.columns(2)
                with col_a: country_col = st.selectbox("عمود الدولة:", df.columns)
                with col_b: dr_col = st.selectbox("عمود نسبة التسليم:", df.columns)
                results = []
                for _, row in df.iterrows():
                    try:
                        raw_dr = str(row[dr_col]).replace('%', '').strip()
                        val_dr = float(raw_dr)
                        if val_dr > 1: val_dr /= 100 
                        status = "✅ رابح" if val_dr >= break_even_dr else "🚨 خاسر"
                        results.append({"المنطقة": row[country_col], "التسليم (DR)": f"{round(val_dr*100, 1)}%", "التعادل المطلوب": f"{round(break_even_dr*100, 1)}%", "الحالة": status})
                    except: continue
                if results: st.table(pd.DataFrame(results))
            except Exception as e: st.error(f"خطأ: {str(e)}")
        else: st.info("ارفع ملف البيانات المالي لعرض التحليل.")
