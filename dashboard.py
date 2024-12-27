# bike_sharing_dashboard.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the title of the dashboard
st.title("Proyek Analisis Data Bike Sharing")

# Load data
hour_data = pd.read_csv('main_data/hour.csv')
day_data = pd.read_csv('main_data/day.csv')

# Display the first few rows of the datasets
st.subheader("Data Hour")
st.write(hour_data.head())
st.subheader("Data Day")
st.write(day_data.head())

# Data Assessment
st.subheader("Assessment of Hour Data")
st.write(hour_data.info())
st.write("Missing values in hour data:")
st.write(hour_data.isna().sum())
st.write("Number of duplicates in hour data:", hour_data.duplicated().sum())
st.write(hour_data.describe())

st.subheader("Assessment of Day Data")
st.write(day_data.info())
st.write("Missing values in day data:")
st.write(day_data.isna().sum())
st.write("Number of duplicates in day data:", day_data.duplicated().sum())
st.write(day_data.describe())

# Data Cleaning
hour_data.drop_duplicates(inplace=True)
day_data.drop_duplicates(inplace=True)

# Exploratory Data Analysis
st.subheader("Exploratory Data Analysis")

# Average rentals by hour
average_hourly_rentals = hour_data.groupby('hr')['cnt'].mean().reset_index()
average_hourly_rentals.columns = ['Jam', 'Rata-rata Penyewaan']

# Total rentals by weather situation
weather_rentals_hour = hour_data.groupby('weathersit')['cnt'].sum().reset_index()
weather_rentals_hour.columns = ['Situasi Cuaca', 'Total Penyewaan']

# Average rentals by holiday
holiday_rentals_hour = hour_data.groupby('holiday')['cnt'].mean().reset_index()
holiday_rentals_hour['holiday'] = holiday_rentals_hour['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'})

# Total rentals by season
seasonal_rentals_hour = hour_data.groupby('season')['cnt'].sum().reset_index()
seasonal_rentals_hour.columns = ['Musim', 'Total Penyewaan']

# Average rentals by temperature
temperature_rentals = hour_data.groupby(pd.cut(hour_data['temp'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1]))['cnt'].mean().reset_index()
temperature_rentals.columns = ['Rentang Suhu', 'Rata-rata Penyewaan']

# Visualizations
st.subheader("Visualizations")

# Boxplot for weather situation
plt.figure(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=day_data)
plt.title('Jumlah Sewa Sepeda Berdasarkan Situasi Cuaca')
plt.xlabel('Situasi Cuaca')
plt.ylabel('Jumlah Sewa')
st.pyplot(plt)

# Barplot for average rentals by month
monthly_rentals = day_data.groupby('mnth')['cnt'].mean().reset_index()
monthly_rentals.columns = ['Bulan', 'Rata-rata Penyewaan']
plt.figure(figsize=(10, 6))
sns.barplot(x='Bulan', y='Rata-rata Penyewaan', data=monthly_rentals, palette='viridis')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(monthly_rentals['Bulan'])
st.pyplot(plt)

# Barplot for total rentals by season
plt.figure(figsize=(10, 6))
sns.barplot(x='Musim', y='Total Penyewaan', data=seasonal_rentals_hour, palette='coolwarm')
plt.title('Total Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan')
plt.xticks(seasonal_rentals_hour['Musim'])
st.pyplot(plt)


# Barplot for total rentals by weather situation
plt.figure(figsize=(10, 6))
sns.barplot(x='Situasi Cuaca', y='Total Penyewaan', data=weather_rentals_hour, palette='Set2')
plt.title('Total Penyewaan Sepeda Berdasarkan Situasi Cuaca')
plt.xlabel('Situasi Cuaca')
plt.ylabel('Total Penyewaan')
st.pyplot(plt)

# Line plot for average rentals by hour
plt.figure(figsize=(10, 6))
sns.lineplot(x='Jam', y='Rata-rata Penyewaan', data=average_hourly_rentals, marker='o')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(average_hourly_rentals['Jam'])  # Menampilkan semua jam pada sumbu x
plt.grid()
st.pyplot(plt)

# Conclusion
st.subheader("Kesimpulan")
st.write("""
1. Pada kondisi tertentu, sepeda banyak disewa pada pagi hari (7-9) dan sore ke malam (16-20).
2. Sepeda jarang disewa pada tengah malam hingga dini pagi dan pada cuaca buruk (hujan badai).
""")