import streamlit as st

# -----------------------------------------
# Title and Introduction
# -----------------------------------------
st.title("🛏️ Hostel Campus Planner – 6,000 Students on 20 Acres")
st.write("""
Estimate infrastructure capacity, construction costs, and annual operating costs of a student hostel campus.
""")

# -----------------------------------------
# 1. User Inputs – Key Parameters
# -----------------------------------------
st.sidebar.header("Campus Configuration")

# Area & Capacity
land_acres = st.sidebar.number_input("Total Land Area (acres)", value=20.0, step=1.0)
students = st.sidebar.number_input("Total Students", value=6000, step=100)
library_acres = st.sidebar.number_input("Library Land Area (acres)", value=2.0, step=0.5)
floors = st.sidebar.slider("Number of Floors (G+?)", 1, 5, 4)

# Room sharing ratio
three_share_pct = st.sidebar.slider("3-Sharing Rooms (%)", 0, 100, 80)
single_room_pct = 100 - three_share_pct

# Construction Cost Inputs
st.sidebar.header("Construction Cost")
avg_cost_per_sqft = st.sidebar.number_input("Avg. Construction Cost (₹/sqft)", value=1800)
infra_cost_multiplier = st.sidebar.slider("Infra Cost (% of construction)", 0, 100, 20)

# Maintenance and Mess Cost
st.sidebar.header("Annual Operating Cost")
maintenance_cost_per_student = st.sidebar.number_input("Maintenance (₹/student/year)", value=9000)
food_cost_per_day = st.sidebar.number_input("Food (₹/student/day)", value=110)

# -----------------------------------------
# 2. Derived Parameters
# -----------------------------------------
SQFT_PER_ACRE = 43560
land_sqft = land_acres * SQFT_PER_ACRE
library_sqft = library_acres * SQFT_PER_ACRE
residential_land_sqft = land_sqft - library_sqft
built_up_footprint = 0.40 * residential_land_sqft
total_built_up_area = built_up_footprint * floors

# Room distribution
three_share_students = int(students * (three_share_pct / 100))
single_room_students = students - three_share_students
three_share_rooms = three_share_students // 3
single_rooms = single_room_students

# Area per student estimate
area_needed = (three_share_students * 200 + single_room_students * 250)
area_per_student = area_needed / students

# -----------------------------------------
# 3. Construction & Infra Cost
# -----------------------------------------
construction_cost = total_built_up_area * avg_cost_per_sqft
infra_cost = construction_cost * (infra_cost_multiplier / 100)
total_project_cost = construction_cost + infra_cost

# -----------------------------------------
# 4. Annual OPEX Estimation
# -----------------------------------------
maintenance_cost_total = maintenance_cost_per_student * students
mess_cost_total = food_cost_per_day * students * 365
total_opex = maintenance_cost_total + mess_cost_total
cost_per_student_per_month = total_opex / students / 12

# -----------------------------------------
# 5. Outputs – Results
# -----------------------------------------
st.subheader("📐 Land & Construction Summary")
st.markdown(f"""
- Total Land Area: **{land_acres} acres** ({int(land_sqft):,} sq ft)  
- Library Area: **{library_acres} acres**  
- Residential & Hostel Area: **{residential_land_sqft:,.0f} sq ft**  
- Built-up Footprint: **{built_up_footprint:,.0f} sq ft**  
- Total Built-up Area (G+{floors-1}): **{total_built_up_area:,.0f} sq ft**
""")

st.subheader("🛏️ Accommodation Plan")
st.markdown(f"""
- Total Students: **{students}**  
- 3-Sharing Rooms: **{three_share_rooms} rooms**  
- Single Rooms: **{single_rooms} rooms**  
- Total Rooms: **{three_share_rooms + single_rooms}**  
- Avg Built-up Area per Student: **{area_per_student:.2f} sq ft**
""")

st.subheader("💸 Construction & Infra Cost")
st.markdown(f"""
- Construction Cost: ₹ **{construction_cost/1e7:.2f} Cr**  
- Infra & External Dev: ₹ **{infra_cost/1e7:.2f} Cr**  
- **Total Project Cost:** ₹ **{total_project_cost/1e7:.2f} Cr**
""")

st.subheader("🧾 Annual Operating Costs")
st.markdown(f"""
- Maintenance: ₹ **{maintenance_cost_total/1e7:.2f} Cr/year**  
- Mess (Food): ₹ **{mess_cost_total/1e7:.2f} Cr/year**  
- **Total Opex:** ₹ **{total_opex/1e7:.2f} Cr/year**  
- Monthly Cost per Student: ₹ **{cost_per_student_per_month:,.0f}**
""")

# -----------------------------------------
# 6. Extras
# -----------------------------------------
with st.expander("📌 Additional Considerations"):
    st.markdown("""
- Add solar panels to reduce energy costs over time  
- Use STP/WTP to recycle water efficiently  
- Hire catering contractors vs in-house kitchen tradeoff  
- Optionally build for 3,000 students now and expand later  
- Add a financial model for ROI, breakeven, or hostel fees
    """)

# End
