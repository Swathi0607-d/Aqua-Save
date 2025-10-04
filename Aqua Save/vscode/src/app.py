import streamlit as st
import pandas as pd
import joblib
import datetime as dt
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

BASE = os.path.join(os.path.dirname(__file__), '..')
DATA_PATH = os.path.join(BASE, 'data', 'processed_water.csv')
MODEL_PATH = os.path.join(BASE, 'models', 'rf_model.joblib')

st.set_page_config(page_title='AquaSave', layout='wide')
st.title('💧 AquaSave - Water Usage Dashboard')

 # Load data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    return df

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

df = load_data()
model = load_model()

 # UI controls
households = df['household_id'].unique().tolist()
selected = st.selectbox('Choose a household', households)
reduction = st.slider('Select % reduction in daily usage (for simulation)',5, 50, 10, step=5)

 # Household slice
hdf = df[df['household_id'] == selected].sort_values('date')
st.subheader('Historical daily usage (last 90 days)')
st.line_chart(hdf.set_index('date')['water_liters'].tail(90))
 
 # Forecast 7 days
last_date = hdf['date'].max()
future_dates = [last_date + dt.timedelta(days=i) for i in range(1, 8)]
future_df = pd.DataFrame ({
    'date': future_dates,
    'day': [d.day for d in future_dates],
    'month': [d.month for d in future_dates],
    'day_of_week': [d.weekday() for d in future_dates],
    'household_code':hdf['household_id'].astype('category').cat.codes.iloc[0],
    'household_size': hdf['household_size'].iloc[-1]
})

future_df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

future_df['predicted_liters'] = model.predict(future_df[['household_code','household_size','day','month','day_of_week','is_weekend']])
future_df['saved_liters'] = future_df['predicted_liters'] * (reduction / 100)
future_df['new_usage'] = future_df['predicted_liters']-future_df['saved_liters']

st.subheader('7-Day Forecast for ' + selected)
st.table(future_df[['date','predicted_liters']].round(2))

 # Plot
fig, ax = plt.subplots()
ax.plot(hdf['date'].tail(30), hdf['water_liters'].tail(30), label='Actual')
ax.plot(future_df['date'], future_df['predicted_liters'], label='Forecast',linestyle='--', marker='o')
ax.set_title(f'Actual (last 30 days) + 7-day Forecast for {selected}')
ax.set_ylabel('Liters')
ax.legend()
st.pyplot(fig)

 # Household saving summary
total_saved = future_df['saved_liters'].sum()
st.write(f'💡 If {selected} reduces usage by **{reduction}%**, they can save **{total_saved:.2f} liters** in the next 7 days.')

 # City-level impact
st.subheader('🏙️ City-Level Impact (all households)')
all_preds = []
for h in df['household_id'].unique():
    hcode = df[df['household_id']==h]['household_id'].astype('category').cat.codes.iloc[0]
    hsize = df[df['household_id']==h]['household_size'].iloc[-1]
    temp = pd.DataFrame({
        'date': future_dates,
        'household_id': h,
        'household_code': hcode,
        'household_size': hsize,
        'day': [d.day for d in future_dates],
        'month': [d.month for d in future_dates],
        'day_of_week': [d.weekday() for d in future_dates]
    })
    temp['is_weekend'] = temp['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    
    temp['predicted_liters'] = model.predict(temp[['household_code','household_size','day','month','day_of_week','is_weekend']])
    all_preds.append(temp)
    
    all_future = pd.concat(all_preds)
    all_future['saved_liters'] = all_future['predicted_liters'] * (reduction /100)
    all_future['new_usage'] = all_future['predicted_liters']-all_future['saved_liters']
    
    city_total_normal = all_future['predicted_liters'].sum()
    city_total_saved = all_future['saved_liters'].sum()
 
st.write(f'🌍 If **all households** reduce usage by **{reduction}%**, the community saves **{city_total_saved:.2f} liters** in 7 days (from {city_total_normal:.2f} → {city_total_normal-city_total_saved:.2f}liters).')

 # City plot
city_summary = all_future.groupby('date')[['predicted_liters','new_usage']].sum().reset_index()
fig2, ax2 = plt.subplots()
ax2.plot(city_summary['date'], city_summary['predicted_liters'], marker='o',label='Normal Forecast')
ax2.plot(city_summary['date'], city_summary['new_usage'], marker='o',linestyle='--', label=f'Reduced (-{reduction}%)')
ax2.set_title('City-Level Water Usage Forecast (All Households)')
ax2.set_ylabel('Liters (All Households)')
ax2.legend()
st.pyplot(fig2)

 # ----------------------
# PDF report generator
 # ----------------------
st.subheader('📄 Generate PDF Report')

def generate_report(household, reduction, future_df_local, all_future_local):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(tmp_file.name)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph('AquaSave - Eco Impact Report', styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Household: {household}', styles['Heading2']))
    story.append(Paragraph(f'Reduction simulated: {reduction}%',styles['Normal']))
    story.append(Spacer(1, 12))
    
 # Household chart
    fig, ax = plt.subplots()
    ax.plot(future_df_local['date'], future_df_local['predicted_liters'],
    marker='o', label='Forecast')
    ax.plot(future_df_local['date'], future_df_local['new_usage'],
    marker='o', linestyle='--', label=f'Reduced (-{reduction}%)')
    ax.set_title(f'Household {household} Forecast')
    ax.legend()
    chart_path = tempfile.NamedTemporaryFile(delete=False,
suffix='.png').name
    fig.savefig(chart_path, bbox_inches='tight')
    plt.close(fig)
    story.append(Image(chart_path, width=400, height=200))
    story.append(Spacer(1, 12))
    story.append(Paragraph('City-wide impact', styles['Heading2']))
    total_saved = all_future_local['saved_liters'].sum()
    story.append(Paragraph(f'Community saving (7 days): {total_saved:.2f}liters', styles['Normal']))

 # City chart
    city_summary_local = all_future_local.groupby('date')[['predicted_liters','new_usage']].sum().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.plot(city_summary_local['date'],
    city_summary_local['predicted_liters'], marker='o', label='Normal')
    ax2.plot(city_summary_local['date'], city_summary_local['new_usage'],
    marker='o', linestyle='--', label='Reduced')
    ax2.set_title('City Forecast')
    ax2.legend()
    chart_path2 = tempfile.NamedTemporaryFile(delete=False,
    suffix='.png').name
    fig2.savefig(chart_path2, bbox_inches='tight')
    plt.close(fig2)
    story.append(Image(chart_path2, width=400, height=200))
 
    doc.build(story)
    return tmp_file.name

if st.button('📥 Create PDF Report'):
    pdf_path = generate_report(selected, reduction, future_df, all_future)
    with open(pdf_path, 'rb') as f:
        st.download_button('⬇️ Download PDF', f,file_name='AquaSave_Report.pdf', mime='application/pdf')
st.info('Run Generate Data -> Preprocess -> Train Model first if you don\'t have data/models yet.')