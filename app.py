import streamlit as st
import requests
from streamlit_js_eval import get_geolocation

# অ্যাপের কনফিগারেশন ও টাইটেল
st.set_page_config(page_title="স্মার্ট ট্যুরিস্ট গাইড", page_icon="🗺️", layout="centered")
st.title("🗺️ স্মার্ট ট্যুরিস্ট অ্যাসিস্ট্যান্ট অ্যাপ")
st.write("আপনার লাইভ লোকেশনের আবহাওয়া এবং আশেপাশের প্রয়োজনীয় জরুরি সেবাগুলো দেখুন।")

# ১. ব্রাউজার থেকে লাইভ GPS লোকেশন নেওয়া
location = get_geolocation()

if location:
    lat = location['coords']['latitude']
    lon = location['coords']['longitude']
    
    st.success("📍 আপনার লাইভ লোকেশন পাওয়া গেছে!")
    
    # ২. লাইভ আবহাওয়া সেকশন (সরাসরি GPS দিয়ে ওপেন-মেটিও এপিআই)
    st.subheader("🌦️ আপনার এলাকার লাইভ আবহাওয়া")
    try:
        # ব্রাউজারের জিপিএস ডাটা সরাসরি এই লিংকে পাঠিয়ে আবহাওয়ার তথ্য আনা হচ্ছে
        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true&relative_humidity_2m=true"
        response = requests.get(weather_url).json()
        current = response['current_weather']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("तापमात्र (Temperature)", f"{current['temperature']}°C")
        col2.metric("বাতাসের গতি (Wind Speed)", f"{current['windspeed']} km/h")
        
        # আবহাওয়ার সাধারণ অবস্থা বোঝানোর কোড
        w_code = current['weathercode']
        status = "স্বচ্ছ আকাশ" if w_code == 0 else "আংশিক মেঘলা" if w_code in [1,2,3] else "বৃষ্টির সম্ভাবনা" if w_code > 50 else "স্বাভাবিক"
        col3.metric("আবহাওয়ার অবস্থা", status)
        
    except Exception as e:
        st.error("আবহাওয়া তথ্য লোড করা যায়নি। অনুগ্রহ করে পেজটি একবার রিফ্রেশ (Refresh) করুন।")
        
    # ৩. আশেপাশের প্রয়োজনীয় স্থান খোঁজা (গুগল ম্যাপস লিংক)
    st.subheader("🔍 আপনার কাছের জরুরি সেবাসমূহ")
    st.write("নিচের বোতামগুলোতে ক্লিক করলে আপনার সবচেয়ে কাছের স্থানটি সরাসরি Google Maps-এ ওপেন হবে:")
    
    def get_maps_url(query):
        return f"https://google.com{query}&location={lat},{lon}"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("🏥 হাসপাতাল (Hospital)", get_maps_url("hospital"))
        st.link_button("👮 পুলিশ স্টেশন (Police)", get_maps_url("police+station"))
        st.link_button("🏫 স্কুল (School)", get_maps_url("school"))
        st.link_button("🎓 বিশ্ববিদ্যালয় (University)", get_maps_url("university"))
    with col_b:
        st.link_button("🚒 ফায়ার সার্ভিস (Fire Station)", get_maps_url("fire+station"))
        st.link_button("🛫 এয়ারপোর্ট (Airport)", get_maps_url("airport"))
        st.link_button("🏞️ পার্ক ও দর্শনীয় স্থান (Parks)", get_maps_url("tourist+attraction+park"))
        st.link_button("💊 ওষুধের দোকান (Pharmacy)", get_maps_url("pharmacy"))

else:
    st.info("👋 অনুগ্রহ করে ব্রাউজারে লোকেশন পারমিশন (Allow Location) দিন যাতে আপনার আশেপাশের তথ্য দেখানো যায়।")