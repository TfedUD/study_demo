import streamlit as st
import streamlit.components.v1 as compo

import plotly as plt
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", 
                   page_title='Sensitivity Study Demo',
                   page_icon='8100464.png')

st.markdown('''For this study a PNLL reference building was selected to be subjected to a parametric study.  
         As the climate in question is 2A, the Cooling Load Intensity is the main subject of the sensitivity study.  
         The variables at play are horizontal slat angle, depth of slats independent to cardinal directions, and  
         the number of slats.
         3075 Annual Load Simulations were ran to compare the impact of all configurations.  
         After all simulations ran it was determined that the Cooling Load Intensity changed by 4.1536 kWh/m2  
         and the Heating Load Intensity by a marginal 0.76105 kWh/m2.
     
         ''')

df = pd.read_csv('data.csv')

df = df.rename(columns={'in:Angle':'Angle',
                        'in:North_shade_depth':'North Shade Depth',
                        'in:East_shade_depth':'East Shade Depth',
                        'in:South_shade_depth':'South Shade Depth',
                        'in:West_shade_depth':'West Shade Depth',
                        'in:shade_count':'Shade Count',
                        'out:cooling load intensity':'Cooling Load Intensity kWh/m2',
                        'out:heating load intensity':'Heating Load intensity kWh/m2'
                        })

fig = px.parallel_coordinates(df, color = 'Cooling Load Intensity kWh/m2', color_continuous_scale='Portland')

st.plotly_chart(fig, use_container_width=True)




html_file = open('model.html', 'r', encoding='utf-8')
source = html_file.read()
compo.html(source, height=800, width=800)