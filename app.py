import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Game Rating Intelligence Dashboard", page_icon="🎮", layout="wide")

st.markdown("""
<style>
[data-testid="metric-container"]{
background:#1B2430;padding:12px;border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("games_cleaned.csv")

@st.cache_resource
def load_model():
    return joblib.load("random_forest_model.pkl")

df = load_data()
model = load_model()

menu = st.sidebar.radio("Navigation",[
"Executive Summary","Dataset Explorer","Market Analytics",
"Model Insights","Hidden Gems","Overrated Games","Prediction AI","About"
])

if menu=="Executive Summary":
    st.title("🎮 Game Rating Intelligence Dashboard")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Games",len(df))
    c2.metric("Avg Rating",round(df["Rating"].mean(),2))
    c3.metric("Avg Plays",f"{int(df['Plays'].mean()):,}")
    c4.metric("Years",f"{int(df['Year'].min())}-{int(df['Year'].max())}")
    st.plotly_chart(px.histogram(df,x="Rating",nbins=25),use_container_width=True)

elif menu=="Dataset Explorer":
    st.dataframe(df,use_container_width=True)

elif menu=="Market Analytics":
    st.plotly_chart(px.scatter(df,x="Plays",y="Rating",hover_name="Title"),use_container_width=True)
    st.plotly_chart(px.scatter(df,x="Wishlist",y="Rating",hover_name="Title"),use_container_width=True)

elif menu=="Model Insights":
    imp = pd.DataFrame({
        "Feature": model.feature_names_in_,
        "Importance": model.feature_importances_
    }).sort_values("Importance",ascending=False)

    st.subheader("Feature Importance")
    st.plotly_chart(px.bar(imp,x="Importance",y="Feature",orientation="h"),use_container_width=True)

    st.subheader("🧠 What Makes a Great Game?")
    top5=imp.head(5)
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=top5["Importance"],theta=top5["Feature"],fill="toself"))
    st.plotly_chart(fig,use_container_width=True)
    st.success(f"Most influential factor: {top5.iloc[0]['Feature']}")

elif menu=="Hidden Gems":
    X=df[["Plays","Number of Reviews","Times Listed","Backlogs","Wishlist","Year"]]
    df["Predicted"]=model.predict(X)
    df["Residual"]=df["Rating"]-df["Predicted"]
    st.dataframe(df.sort_values("Residual",ascending=False)[["Title","Rating","Predicted","Residual"]].head(20))

elif menu=="Overrated Games":
    X=df[["Plays","Number of Reviews","Times Listed","Backlogs","Wishlist","Year"]]
    df["Predicted"]=model.predict(X)
    df["Residual"]=df["Rating"]-df["Predicted"]
    st.dataframe(df.sort_values("Residual",ascending=True)[["Title","Rating","Predicted","Residual"]].head(20))

elif menu=="Prediction AI":
    plays=st.number_input("Plays",10000)
    reviews=st.number_input("Reviews",1000)
    listed=st.number_input("Times Listed",1000)
    backlogs=st.number_input("Backlogs",1000)
    wishlist=st.number_input("Wishlist",1000)
    year=st.number_input("Year",2024)
    if st.button("Predict"):
        X=pd.DataFrame([[plays,reviews,listed,backlogs,wishlist,year]],columns=[
            "Plays","Number of Reviews","Times Listed","Backlogs","Wishlist","Year"])
        pred=float(model.predict(X)[0])
        st.metric("Predicted Rating",round(pred,2))
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number",value=pred,gauge={"axis":{"range":[0,5]}})))

else:
    st.markdown("### Video Game Rating Prediction using Random Forest")
