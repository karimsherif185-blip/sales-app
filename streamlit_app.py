import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(page_title="Dynamic Sales Analytics", layout="wide", page_icon="📈")

st.title("📈 لوحة تحكم المبيعات التفاعلية")
st.markdown("قم بتعديل الأرقام، إضافة صفوف جديدة، أو حذفها من الجدول أدناه. جميع الرسوم البيانية والمؤشرات سيتم تحديثها تلقائياً.")
st.divider()

# 2. البيانات الأساسية (تُحمل مرة واحدة)
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Laptops": [15000, 18000, 22000, 19000, 25000, 30000],
        "Accessories": [4000, 5500, 5000, 7000, 8000, 9500],
        "Monitors": [8000, 9000, 11000, 10500, 13000, 16000]
    })

# 3. الجدول التفاعلي (يتيح الإضافة والحذف والتعديل)
st.subheader("📝 قاعدة البيانات (قابلة للتعديل)")
edited_df = st.data_editor(
    st.session_state.sales_data, 
    use_container_width=True, 
    num_rows="dynamic" # يسمح بإضافة وحذف الصفوف
)

# تحديث العمليات الحسابية بناءً على الجدول المعدل
edited_df["Total Sales"] = edited_df["Laptops"] + edited_df["Accessories"] + edited_df["Monitors"]

st.divider()

# 4. مؤشرات الأداء الرئيسية (KPIs)
st.subheader("📊 مؤشرات الأداء الحالية")
col1, col2, col3, col4 = st.columns(4)

total_revenue = edited_df["Total Sales"].sum()
best_month = edited_df.loc[edited_df["Total Sales"].idxmax()]["Month"] if not edited_df.empty else "N/A"
top_sales_value = edited_df["Total Sales"].max() if not edited_df.empty else 0

laptop_total = edited_df["Laptops"].sum()
acc_total = edited_df["Accessories"].sum()
mon_total = edited_df["Monitors"].sum()

categories = {"اللابتوبات": laptop_total, "الإكسسوارات": acc_total, "الشاشات": mon_total}
top_category = max(categories, key=categories.get) if categories else "N/A"

col1.metric("إجمالي الإيرادات", f"${total_revenue:,}")
col2.metric("أفضل شهر", str(best_month))
col3.metric("مبيعات أفضل شهر", f"${top_sales_value:,}")
col4.metric("المنتج الأكثر مبيعاً", str(top_category))

st.divider()

# 5. الرسوم البيانية التفاعلية
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 اتجاه المبيعات الشهري")
    if not edited_df.empty:
        fig_line = px.line(edited_df, x="Month", y=["Laptops", "Accessories", "Monitors"], markers=True)
        fig_line.update_layout(xaxis_title="الشهر", yaxis_title="قيمة المبيعات", legend_title="المنتجات")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("لا توجد بيانات لعرض الرسم البياني.")

with col_chart2:
    st.subheader("🥧 نسبة مبيعات الأقسام")
    if not edited_df.empty:
        pie_data = pd.DataFrame({
            "Category": ["Laptops", "Accessories", "Monitors"],
            "Sales": [laptop_total, acc_total, mon_total]
        })
        fig_pie = px.pie(pie_data, names="Category", values="Sales", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("لا توجد بيانات لعرض الرسم البياني.")

st.divider()

# 6. زر تحميل البيانات كملف CSV (إضافة قوية للـ CV)
st.subheader("💾 تصدير البيانات")
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="تحميل البيانات الحالية (CSV)",
    data=csv,
    file_name='updated_sales_data.csv',
    mime='text/csv',
)