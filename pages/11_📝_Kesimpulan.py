import streamlit as st
from utils.helpers import render_sidebar

st.set_page_config(page_title="Kesimpulan", page_icon="📝", layout="wide")
render_sidebar()

st.title("📝 Kesimpulan")

st.markdown("""
Dari 8 cerita data yang kita eksplorasi, beberapa temuan utama:

1. **Rating tertinggi** tidak selalu dimiliki oleh game yang paling populer
2. **Genre RPG dan Adventure** mendominasi baik dari segi jumlah maupun kualitas
3. **Korelasi antara popularitas dan rating** cenderung lemah --- banyak dimainkan bukan berarti berkualitas tinggi
4. **Wishlist tinggi** menandakan hype besar dari komunitas, namun belum tentu rating tinggi setelah dimainkan
5. **Tren produksi game** meningkat pesat sejak era 2010-an
6. Beberapa **studio besar** secara konsisten merilis banyak game dalam dataset ini
7. **Game klasik** seperti Chrono Trigger (1995) masih masuk Top 10 rating, membuktikan kualitas lintas generasi

Dataset ini menunjukkan bahwa industri game sangat dinamis, dan setiap metrik (rating, plays, wishlist) menceritakan cerita yang berbeda tentang kesuksesan sebuah game.
""")