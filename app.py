import streamlit as st
import pandas as pd
import pickle
from io import BytesIO

# Load trained model
model = pickle.load(open('house_price_model.pkl', 'rb'))  # Your model file

# Streamlit Page Config
st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="wide")

# -- Sidebar ---
with st.sidebar:
    st.title("🏠 About This App")
    st.markdown("""
    Predict house selling price based on property features.
    
    **How to Use:**
    1. Fill out the property details.
    2. Click on 'Predict House Price 💰'.
    3. Download your prediction as a report!
                
    """)

    st.markdown("---")
    st.write("📧 Contact: mangalkhemraj@gmail.com")

# -- Title and Intro ---
st.title("🏡 Dream House Price Predictor")
st.caption("Fast and Accurate house price estimation in a few clicks!")

st.markdown("## 📋 Property Details")

# -- Columns Layout
left_col, right_col = st.columns(2)

with left_col:
    overall_qual = st.slider("🏆 Overall Quality (1=Very Poor, 10=Excellent)", 1, 10, 5)
    overall_cond = st.slider("🏆 Overall Condition (1=Very Poor, 9=Excellent)", 1, 9, 5)
    gr_liv_area = st.slider("🏠 Above Ground Living Area (sq ft)", 300, 4000, 1500)
    total_bsmt_sf = st.slider("🏠 Basement Area (sq ft)", 0, 3000, 800)
    first_flr_sf = st.slider("🏠 First Floor Area (sq ft)", 300, 3000, 1000)
    garage_area = st.slider("🚗 Garage Area (sq ft)", 0, 1500, 400)
    lot_area = st.slider("🏡 Lot Size (sq ft)", 1000, 30000, 8000)

with right_col:
    year_built = st.number_input("🛠️ Year Built", 1800, 2025, 2000)
    year_remod = st.number_input("🔨 Year Remodeled", 1800, 2025, 2005)
    
    neighborhood = st.selectbox(
        "📍 Neighborhood (encoded)", 
        options=list(range(0, 26)),
        format_func=lambda x: f"Neighborhood {x}"
    )
    
    bsmt_qual = st.selectbox("🏚️ Basement Quality (Encoded 1-5)", [1, 2, 3, 4, 5])
    bsmtfin_sf1 = st.slider("🏚️ Finished Basement Area (sq ft)", 0, 2000, 500)
    full_bath = st.selectbox("🛁 Full Bathrooms", [0, 1, 2, 3, 4])
    bsmt_full_bath = st.selectbox("🛁 Basement Full Bathrooms", [0, 1, 2])
    kitchen_qual = st.selectbox("🍽️ Kitchen Quality (Encoded 1-5)", [1, 2, 3, 4, 5])
    garage_cars = st.selectbox("🚗 Garage Capacity (cars)", [0, 1, 2, 3, 4])
    wood_deck_sf = st.slider("🪵 Wood Deck Area (sq ft)", 0, 800, 100)
    fireplaces = st.selectbox("🔥 Number of Fireplaces", [0, 1, 2, 3])

# Prediction Button
st.markdown("---")
st.markdown("## 🎯 Prediction Result")

if st.button('Predict House Price 💰'):
    input_data = pd.DataFrame([{
        'Overall Qual': overall_qual,
        'Overall Cond': overall_cond,
        'Gr Liv Area': gr_liv_area,
        'Total Bsmt SF': total_bsmt_sf,
        '1st Flr SF': first_flr_sf,
        'Garage Area': garage_area,
        'Lot Area': lot_area,
        'Year Built': year_built,
        'Year Remod/Add': year_remod,
        'Neighborhood': neighborhood,
        'Bsmt Qual': bsmt_qual,
        'BsmtFin SF 1': bsmtfin_sf1,
        'Full Bath': full_bath,
        'Bsmt Full Bath': bsmt_full_bath,
        'Kitchen Qual': kitchen_qual,
        'Garage Cars': garage_cars,
        'Wood Deck SF': wood_deck_sf,
        'Fireplaces': fireplaces
    }])
    with st.spinner('Predicting the price...'):
        prediction = model.predict(input_data)[0]
    low_range = prediction * 0.95
    high_range = prediction * 1.05

    st.success(f"🏡 Estimated House Price: **${prediction:,.2f}**")
    st.info(f"🔍 Confidence Range: ${low_range:,.0f} - ${high_range:,.0f}")

    st.balloons()

    st.markdown("### 🧾 Property Summary:")
    st.dataframe(input_data.style.highlight_max(axis=0))

    # Download prediction
    prediction_df = input_data.copy()
    prediction_df['Predicted Price'] = prediction

    # Create download button
    csv = prediction_df.to_csv(index=False)
    b64 = BytesIO(csv.encode()).getvalue()

    st.download_button(
        label="📥 Download Prediction Report",
        data=b64,
        file_name='house_price_prediction.csv',
        mime='text/csv'
    )


