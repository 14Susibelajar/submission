import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
def load_data():
    file_path = "dashboard/data_all.csv"  # Pastikan path file benar
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df['Tanggal'] = df['datetime'].dt.date
    df['temp_category'] = pd.cut(df['TEMP'], bins=5).astype(str)  # Konversi Interval ke String
    df['wind_category'] = pd.cut(df['WSPM'], bins=5).astype(str)
    return df

df_all = load_data()

# Sidebar untuk filter
# Tambahkan judul 
st.sidebar.markdown("## 🌍 Pengaturan Tampilan")

# Pemisah untuk estetika
st.sidebar.divider()

# Tampilkan deskripsi tambahan
st.sidebar.markdown(
    "🔎 **Gunakan filter di bawah ini untuk menyesuaikan tampilan data kualitas udara.**"
)

# Input rentang tanggal 
date_range = st.sidebar.date_input(
    "📅 Pilih Rentang Tanggal", 
    [df_all['datetime'].min().date(), df_all['datetime'].max().date()],
    min_value=df_all['datetime'].min().date(),
    max_value=df_all['datetime'].max().date()
)

# Pemisah agar lebih rapi
st.sidebar.divider()

# Tambahkan sedikit dekorasi menggunakan Markdown dan CSS
st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 15px;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Judul Dashboard
st.markdown(
    """
    <h1 style='text-align: center;'>🌍 Dashboard Kualitas Udara</h1>
    <h3 style='text-align: center;'>Pengaruh Cuaca terhadap Polusi Udara & Tren Kualitas Udara</h3>
    """, 
    unsafe_allow_html=True
)

# CSS  latar belakang
st.markdown(
    """
    <style>
    /* Warna latar belakang halaman */
    body {
        background: linear-gradient(to right, #f4f4f4, #e3f2fd); /* Gradasi warna */
        color: #333333; /* Warna teks */
    }
    
    /* Warna sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 15px;
    }

    /* Warna header */
    h1, h2, h3 {
        color: #2c3e50;
        text-align: center;
    }

    /* Warna teks di sidebar */
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #2c3e50;
    }

    /* Gaya tambahan untuk tampilan lebih modern */
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #e3f2fd);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Box Plot PM2.5 berdasarkan Kategori Suhu
fig_temp = px.box(
    df_all, 
    x='temp_category', 
    y='PM2.5', 
    title='Distribusi PM2.5 Berdasarkan Suhu',
    labels={'temp_category': 'Kategori Suhu', 'PM2.5': 'Konsentrasi PM2.5'}, 
    color='temp_category'
)

#  tampilan
fig_temp.update_layout(
    title_x=0.3,  # Menengahkan judul
    title_font=dict(size=18, family="Arial", color="black"),  # Memperbesar dan mengatur font
    xaxis_title="Kategori Suhu",  # Menambah label sumbu X
    yaxis_title="Konsentrasi PM2.5",  # Menambah label sumbu Y
    template="plotly_white"  # Menggunakan tema bersih agar lebih menarik
)

st.plotly_chart(fig_temp)

# Diagram batang Rata-rata PM2.5 & PM10 berdasarkan Kecepatan Angin
wind_avg = df_all.groupby('wind_category')[['PM2.5', 'PM10']].mean().reset_index()

fig_wind = px.bar(
    wind_avg, 
    x='wind_category', 
    y=['PM2.5', 'PM10'], 
    title='Rata-rata PM2.5 & PM10 Berdasarkan Kecepatan Angin',
    labels={'wind_category': 'Kecepatan Angin', 'value': 'Konsentrasi Polutan'}, 
    barmode='group'
)

# tampilan
fig_wind.update_layout(
    title_x=0.2, 
    title_font=dict(size=18, family="Arial", color="black"),
    xaxis_title="Kecepatan Angin",
    yaxis_title="Konsentrasi Polutan",
    template="plotly_white"
)

st.plotly_chart(fig_wind)

# Tren PM2.5 per Tahun
yearly_avg = df_all.groupby(df_all['datetime'].dt.year)['PM2.5'].mean().reset_index()

fig_trend = px.line(
    yearly_avg, 
    x='datetime', 
    y='PM2.5', 
    markers=True,
    title='Tren Rata-rata PM2.5 per Tahun', 
    labels={'datetime': 'Tahun'}
)

# Menengahkan judul dan memperbaiki tampilan
fig_trend.update_layout(
    title_x=0.3, 
    title_font=dict(size=18, family="Arial", color="black"),
    xaxis_title="Tahun",
    yaxis_title="Konsentrasi PM2.5",
    template="plotly_white"
)

st.plotly_chart(fig_trend)

# Bar plot rata-rata polutan per bulan
monthly_avg = df_all.groupby(df_all['datetime'].dt.month)[['PM2.5', 'PM10']].mean().reset_index()

fig_month = px.bar(
    monthly_avg, 
    x='datetime', 
    y=['PM2.5', 'PM10'], 
    barmode='group',
    title='Rata-rata PM2.5 dan PM10 per Bulan', 
    labels={'datetime': 'Bulan'}
)

# tampilan
fig_month.update_layout(
    title_x=0.3, 
    title_font=dict(size=18, family="Arial", color="black"),
    xaxis_title="Bulan",
    yaxis_title="Konsentrasi Polutan",
    template="plotly_white"
)

st.plotly_chart(fig_month)


st.write("### 📌 Kesimpulan")
st.write("- Konsentrasi PM2.5 dan PM10 lebih tinggi saat suhu rendah.")
st.write("- Kecepatan angin tinggi membantu menyebarkan polusi.")
st.write("- Tren PM2.5 mengalami fluktuasi dari tahun ke tahun.")
