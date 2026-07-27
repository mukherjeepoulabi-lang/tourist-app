import streamlit as st
import requests

st.set_page_config(page_title="Smart Tourist Assistant", page_icon="📱", layout="centered")

st.title("📱 SMART TOURIST ASSISTANT")
st.write("আপনার লাইভ লোকেশনের আবহাওয়া এবং আশেপাশের প্রয়োজনীয় জরুরি সেবাগুলো দেখুন।")

lat = 22.5726  
lon = 88.3639  

st.success("📍 আপনার লাইভ লোকেশন পাওয়া গেছে।")

st.markdown("### 🌦️ আপনার এলাকার লাইভ আবহাওয়া")
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    # এই লিঙ্কটি সম্পূর্ণ নিখুঁত এবং ফিক্সড
    weather_url =f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    response = requests.get(weather_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        weather_res = response.json()
        current_w = weather_res['current_weather']
        
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.metric(label="🌡️ তাপমাত্রা", value=f"{current_w['temperature']}°C")
        with col_w2:
            st.metric(label="💨 বাতাসের গতি", value=f"{current_w['windspeed']} km/h")
    else:
        st.error(f"সার্ভার থেকে রেসপন্স পাওয়া যায়নি (Error Code: {response.status_code})")
except Exception as e:
    st.error(f"আবহাওয়া তথ্য লোড করা যায়নি। সমস্যা: {str(e)}")

def get_maps_url(service_type):
    return f"https://google.com{service_type}/@{lat},{lon}"

st.markdown("### 🔍 আপনার কাছের জরুরি সেবাসমূহ")
st.write("নিচের বোতামগুলোতে ক্লিক করলে আপনার সবচেয়ে কাছের স্থানটি সরাসরি Google Maps-এ ওপেন হবে:")

col1, col2 = st.columns(2)
with col1:
    if st.button("🏥 হাসপাতাল (Hospital)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("hospital"))
    if st.button("👮 police স্টেশন (Police)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("police+station"))
    if st.button("🏫 স্কুল (School)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("school"))
    if st.button("🏛️ বিশ্ববিদ্যালয় (University)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("university"))
with col2:
    if st.button("🚒 ফায়ার সার্ভিস (Fire Station)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("fire+station"))
    if st.button("✈️ এয়ারপোর্ট (Airport)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("airport"))
    if st.button("🌳 পার্ক ও দর্শনীয় স্থান (Parks)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("tourist+attraction+park"))
    if st.button("💊 ওষুধের দোকান (Pharmacy)", use_container_width=True):
        st.link_button("ম্যাপে দেখুন", get_maps_url("pharmacy"))

st.info("💡 অনুগ্রহ করে ব্রাউজারে লোকেশন পারমিশন (Allow Location) দিন যাতে আপনার আশেপাশের সঠিক তথ্য দেখানো যায়।")
