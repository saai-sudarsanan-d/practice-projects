import streamlit as st
import plotly.express as px
import pandas as pd
import pickle

infile = open("wine-model.pkl",'rb')
model = pickle.load(infile)
infile.close()

df=pd.read_csv("winequality-red.csv")

def get_res(x=[]):
    # fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol
    return model.predict([x])

st.title("Red Wine Quality and DashBoard")

c1 = st.beta_container()
c1.write("This is the data used to train the model")
c1.dataframe(df)


viz = st.beta_expander("Click Here to view Visualisations")

c2 = viz.beta_container()
# Hist Chart Plotter
c2.write("Histograms")
choice = c2.selectbox("",options = list(df.columns))
hist = px.histogram(df, x=choice)
c2.plotly_chart(hist)

# Pie Chart
c2.write("Pie Chart")
pie = px.pie(df,names="quality")
c2.plotly_chart(pie)

# Heatmap
c2.write("Heat Map")
hmap = px.imshow(df.corr())
c2.plotly_chart(hmap)

# Analyser

predictor = st.beta_expander("Click here to analyse a value")
c3 = predictor.beta_container()

did = c3.number_input("Enter ID",min_value=0,max_value=1598,step=1)
set_val = c3.button("Prest values from ID")
set_val = True
if set_val:
    vals=list(df.iloc[did,:].values)
else:
    vals=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    set_val = False
fixed_acidity = c3.number_input(label="Fixed Acidity",min_value=0.0,max_value=20.0,step=0.2,value=(vals[0]))
volatile_acidity = c3.number_input(label="Volatile Acidity",min_value=0.0,max_value=3.0,step=0.2,value=(vals[1]))
citric_acid = c3.number_input(label="Citric Acid",min_value=0.0,max_value=3.0,step=0.002,value=(vals[2]))
residual_sugar = c3.number_input(label="Residual Sugar",min_value=0.0,max_value=20.0,step=0.2,value=(vals[3]))
chlorides = c3.number_input(label="Chlorides",min_value=0.0,max_value=1.0,step=0.0002,value=(vals[4]))
free_sulfur_dioxide = c3.number_input(label="Free Sulfur Dioxide",min_value=0.0,max_value=200.0,step=2.0,value=(vals[5]))
total_sulfur_dioxide = c3.number_input(label="Total Sulfur Dioxide",min_value=0.0,max_value=300.0,step=2.0,value=(vals[6]))
density = c3.number_input(label="Density",min_value=0.000,max_value=2.000,step=0.0002,value=(vals[7]))
pH = c3.number_input(label="ph",min_value=0.0,max_value=7.0,step=0.2,value=(vals[8]))
sulphates = c3.number_input(label="Sulphates",min_value=0.0,max_value=5.0,step=0.2,value=(vals[9]))
alcohol = c3.number_input(label="Alcohol",min_value=0.0,max_value=20.0,step=0.2,value=(vals[10]))


analyse = c3.button("Analyse Result",key=0)
if analyse:
    st.write("Quality is "  + str(get_res([fixed_acidity,
                        volatile_acidity,
                        citric_acid,
                        residual_sugar,
                        chlorides,
                        free_sulfur_dioxide,
                        total_sulfur_dioxide,
                        density,
                        pH,
                        sulphates,
                        alcohol])[0]))