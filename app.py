
import streamlit as st, pandas as pd, numpy as np, ast
import plotly.express as px, plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Game Rating Intelligence",layout="wide",page_icon="🎮")

st.markdown("""<style>
.block-container{padding-top:1rem}
[data-testid="metric-container"]{background:#161B22;border-radius:12px;padding:12px}
</style>""",unsafe_allow_html=True)

@st.cache_data
def load():
    df=pd.read_csv("games.csv")
    def conv(v):
        if isinstance(v,str) and v.endswith("K"):
            return float(v[:-1])*1000
        try:return float(str(v).replace(",",""))
        except:return np.nan
    for c in ['Plays','Playing','Backlogs','Wishlist','Times Listed','Number of Reviews']:
        if c in df: df[c]=df[c].apply(conv)
    df["Year"]=pd.to_datetime(df["Release Date"],errors="coerce").dt.year
    df=df.dropna(subset=["Rating"])
    return df
df=load()

st.sidebar.title("🎮 Game Rating Intelligence")
page=st.sidebar.radio("Menu",[
"Executive Summary","Market Analytics","Genre Intelligence",
"Model Performance","What Makes a Great Game",
"Hidden Gems","Prediction AI"
])

if page=="Executive Summary":
    st.title("🎮 Executive Dashboard")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Games",len(df))
    c2.metric("Avg Rating",round(df.Rating.mean(),2))
    c3.metric("Total Plays",f"{int(df.Plays.sum()):,}")
    c4.metric("Years",f"{int(df.Year.min())}-{int(df.Year.max())}")
    a,b=st.columns(2)
    with a:
        st.plotly_chart(px.histogram(df,x="Rating",title="Rating Distribution"),use_container_width=True)
    with b:
        yearly=df.groupby("Year").size().reset_index(name="Games")
        st.plotly_chart(px.area(yearly,x="Year",y="Games",title="Release Trend"),use_container_width=True)

elif page=="Market Analytics":
    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(px.scatter(df,x="Plays",y="Rating",hover_name="Title",color="Year"),use_container_width=True)
    with col2:
        st.plotly_chart(px.scatter(df,x="Wishlist",y="Rating",hover_name="Title"),use_container_width=True)

elif page=="Genre Intelligence":
    genres=[]
    for g in df["Genres"].dropna():
        try: genres.extend(ast.literal_eval(g))
        except: pass
    gdf=pd.Series(genres).value_counts().head(12).reset_index()
    gdf.columns=["Genre","Count"]
    st.plotly_chart(px.pie(gdf,names="Genre",values="Count",hole=.5,title="Top Genres"),use_container_width=True)

elif page=="Model Performance":
    feat=['Plays','Number of Reviews','Times Listed','Backlogs','Wishlist','Year']
    data=df.dropna(subset=feat+['Rating'])
    X=data[feat]; y=data['Rating']
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
    rf=RandomForestRegressor(n_estimators=100,random_state=42).fit(Xtr,ytr)
    lr=LinearRegression().fit(Xtr,ytr)
    from sklearn.metrics import r2_score
    comp=pd.DataFrame({
      "Model":["Linear Regression","Random Forest"],
      "R2":[r2_score(yte,lr.predict(Xte)),r2_score(yte,rf.predict(Xte))]
    })
    st.plotly_chart(px.bar(comp,x="Model",y="R2",title="Model Comparison"),use_container_width=True)

elif page=="What Makes a Great Game":
    feat=['Plays','Number of Reviews','Times Listed','Backlogs','Wishlist','Year']
    data=df.dropna(subset=feat+['Rating'])
    rf=RandomForestRegressor(n_estimators=100,random_state=42).fit(data[feat],data['Rating'])
    imp=pd.DataFrame({"Feature":feat,"Importance":rf.feature_importances_}).sort_values("Importance",ascending=False)
    st.plotly_chart(px.bar(imp,x="Importance",y="Feature",orientation="h"),use_container_width=True)
    top=imp.iloc[0]["Feature"]
    st.success(f"Faktor paling berpengaruh terhadap rating adalah {top}.")

elif page=="Hidden Gems":
    feat=['Plays','Number of Reviews','Times Listed','Backlogs','Wishlist','Year']
    data=df.dropna(subset=feat+['Rating']).copy()
    rf=RandomForestRegressor(n_estimators=100,random_state=42).fit(data[feat],data['Rating'])
    data["Predicted"]=rf.predict(data[feat])
    data["Residual"]=data["Rating"]-data["Predicted"]
    st.dataframe(data.sort_values("Residual",ascending=False)[["Title","Rating","Predicted","Residual"]].head(20))

elif page=="Prediction AI":
    plays=st.number_input("Plays",1000)
    reviews=st.number_input("Reviews",100)
    listed=st.number_input("Times Listed",100)
    backlogs=st.number_input("Backlogs",100)
    wishlist=st.number_input("Wishlist",100)
    year=st.number_input("Year",2024)
    feat=['Plays','Number of Reviews','Times Listed','Backlogs','Wishlist','Year']
    data=df.dropna(subset=feat+['Rating'])
    rf=RandomForestRegressor(n_estimators=100,random_state=42).fit(data[feat],data['Rating'])
    if st.button("Predict"):
        p=float(rf.predict(pd.DataFrame([[plays,reviews,listed,backlogs,wishlist,year]],columns=feat))[0])
        st.metric("Predicted Rating",round(p,2))
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number",value=p,gauge={"axis":{"range":[0,5]}})))
