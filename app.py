import streamlit as st
import streamlit.components.v1 as compo
from honeybee.model import Model
from honeybee.room import Room
from utils.utils import add_louver_shade
import plotly as plt
import plotly.express as px
import pandas as pd
import uuid
from honeybee_display.model import model_to_vis_set
from ladybug_vtk.visualization_set import VisualizationSet as VTKVisualizationSet
from pollination_streamlit_viewer import viewer
from pathlib import Path

st.set_page_config(layout="wide", 
                   page_title='Sensitivity Study',
                   page_icon='8100464.png')

st.markdown('''For this study a PNNL prototype building was selected to be subjected to a parametric study.  
         As the climate in question is 2A, the Cooling Load Intensity is the main subject of the sensitivity study.  
         The variables at play are horizontal slat angle, depth of slats independent to cardinal directions, and  
         the number of slats.
         3075 Annual Load Simulations were ran to compare the impact of all configurations.  
         After all simulations ran it was determined that the Cooling Load Intensity changed by 4.1536 kWh/m2  
         and the Heating Load Intensity by a marginal 0.76105 kWh/m2.
     
         ''')

df = pd.read_csv('data.csv')

df = df.rename(columns={'in:Angle':'            Angle',
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

st.subheader('Model Configuration')

angle = st.selectbox("Louver Angle",(0, 25, 45, 65))
n_depth = st.selectbox("North Depth", (.1,.2,.3,.4))
e_depth = st.selectbox("East Depth", (.1,.2,.3,.4))
s_depth = st.selectbox("South Depth", (.1,.2,.3,.4))
w_depth = st.selectbox("West Depth", (.1,.2,.3,.4))
s_count = st.selectbox("Shade Count", (2,4,6))


configure = st.toggle("Configure Model")

if configure:
    model = Model.from_hbjson('multi_fam.hbjson')
    rooms_list = []
    for room in model.rooms: 
        rooms_list.append(add_louver_shade(objs=room, _depth=[n_depth, e_depth, s_depth, w_depth], _shade_count_=[s_count], _angle_=[angle]))
    rooms = []
    for obj in rooms_list:
        rooms.append(Room(identifier=uuid.uuid4().hex, faces=obj))   
    
    new_model = Model(identifier='NewModel', rooms=rooms, orphaned_shades=model.shades)
    
    
    vis_set = model_to_vis_set(new_model)
    vis_s = VTKVisualizationSet.from_visualization_set(vis_set)
    output = vis_s.to_vtkjs(folder='.', name='model_vtkjs')
    content = Path('model_vtkjs.vtkjs').read_bytes()
    
    viewer(
        content = content,
        key = 'vtkjs viewer',
        subscribe = False,
        style={
            'height':'800px',
            'width': '800px'
        }
        
    )

    
elif not configure:
    # html_file = open('model.html', 'r', encoding='utf-8')
    # source = html_file.read()
    # compo.html(source, height=800, width=800)
    model = Model.from_hbjson('multi_fam.hbjson')
    vis_set = model_to_vis_set(model)
    vtk_set = VTKVisualizationSet.from_visualization_set(vis_set)
    output = vtk_set.to_vtkjs(folder='.', name='base_model_vtkjs')
    content = Path('base_model_vtkjs.vtkjs').read_bytes()
    
    viewer(
        content = content,
        key = 'demo_viewer',
        subscribe = False,
        style={
            'height':'800px',
            'width': '800px'
        }
    )