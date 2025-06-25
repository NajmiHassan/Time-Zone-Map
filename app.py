import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import pytz

# Page config
st.set_page_config(page_title="Canada Time Zone Map", layout="wide")

# Title
st.title("🇨🇦 Canada Time Zone Map")
st.markdown("Interactive map showing Canada's six time zones with current times")

# Define Canada's time zones with approximate boundaries (longitude)
time_zones = {
    'Pacific': {
        'tz': 'America/Vancouver',
        'utc_offset': -8,
        'color': '#FF6B6B',
        'lon_range': [-141, -120],
        'provinces': ['British Columbia', 'Yukon']
    },
    'Mountain': {
        'tz': 'America/Edmonton', 
        'utc_offset': -7,
        'color': '#4ECDC4',
        'lon_range': [-120, -110],
        'provinces': ['Alberta', 'Northwest Territories']
    },
    'Central': {
        'tz': 'America/Winnipeg',
        'utc_offset': -6, 
        'color': '#45B7D1',
        'lon_range': [-110, -90],
        'provinces': ['Saskatchewan', 'Manitoba', 'Nunavut (west)']
    },
    'Eastern': {
        'tz': 'America/Toronto',
        'utc_offset': -5,
        'color': '#96CEB4',
        'lon_range': [-90, -68],
        'provinces': ['Ontario', 'Quebec', 'Nunavut (east)']
    },
    'Atlantic': {
        'tz': 'America/Halifax',
        'utc_offset': -4,
        'color': '#FECA57',
        'lon_range': [-68, -60],
        'provinces': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island']
    },
    'Newfoundland': {
        'tz': 'America/St_Johns',
        'utc_offset': -3.5,
        'color': '#FF9FF3',
        'lon_range': [-60, -52],
        'provinces': ['Newfoundland and Labrador']
    }
}

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Create the map
    fig = go.Figure()
    
    # Add time zone regions as rectangles
    for zone_name, zone_data in time_zones.items():
        lon_min, lon_max = zone_data['lon_range']
        
        # Add rectangle for time zone
        fig.add_trace(go.Scatter(
            x=[lon_min, lon_max, lon_max, lon_min, lon_min],
            y=[41, 41, 84, 84, 41],
            fill='toself',
            fillcolor=zone_data['color'],
            opacity=0.6,
            line=dict(color=zone_data['color'], width=2),
            name=f"{zone_name} Time",
            hovertemplate=f"<b>{zone_name} Time Zone</b><br>" +
                         f"UTC{zone_data['utc_offset']:+g}<br>" +
                         f"Provinces: {', '.join(zone_data['provinces'])}<extra></extra>",
            showlegend=True
        ))
    
    # Major cities with their coordinates
    cities = [
        {'name': 'Vancouver', 'lat': 49.2827, 'lon': -123.1207, 'zone': 'Pacific'},
        {'name': 'Calgary', 'lat': 51.0447, 'lon': -114.0719, 'zone': 'Mountain'},
        {'name': 'Winnipeg', 'lat': 49.8951, 'lon': -97.1384, 'zone': 'Central'},
        {'name': 'Toronto', 'lat': 43.6532, 'lon': -79.3832, 'zone': 'Eastern'},
        {'name': 'Montreal', 'lat': 45.5017, 'lon': -73.5673, 'zone': 'Eastern'},
        {'name': 'Halifax', 'lat': 44.6488, 'lon': -63.5752, 'zone': 'Atlantic'},
        {'name': "St. John's", 'lat': 47.5615, 'lon': -52.7126, 'zone': 'Newfoundland'}
    ]
    
    # Add cities as markers
    for city in cities:
        zone_color = time_zones[city['zone']]['color']
        fig.add_trace(go.Scatter(
            x=[city['lon']],
            y=[city['lat']],
            mode='markers+text',
            marker=dict(size=12, color='white', line=dict(color=zone_color, width=3)),
            text=[city['name']],
            textposition='top center',
            textfont=dict(size=10, color='black'),
            name=city['name'],
            showlegend=False,
            hovertemplate=f"<b>{city['name']}</b><br>" +
                         f"Time Zone: {city['zone']}<extra></extra>"
        ))
    
    # Update layout
    fig.update_layout(
        title="Canada Time Zones",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue'
        ),
        xaxis=dict(title="Longitude", range=[-145, -50]),
        yaxis=dict(title="Latitude", range=[40, 85]),
        height=500,
        showlegend=True,
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.8)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Current Times")
    
    # Display current time for each zone
    for zone_name, zone_data in time_zones.items():
        try:
            tz = pytz.timezone(zone_data['tz'])
            current_time = datetime.now(tz)
            
            st.markdown(f"""
            <div style="background-color: {zone_data['color']}; 
                        padding: 10px; margin: 5px 0; border-radius: 5px; 
                        color: white; font-weight: bold;">
                <div style="font-size: 14px;">{zone_name}</div>
                <div style="font-size: 18px;">{current_time.strftime('%H:%M:%S')}</div>
                <div style="font-size: 12px;">UTC{zone_data['utc_offset']:+g}</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error(f"Could not get time for {zone_name}")

# Add information section
st.markdown("---")
st.subheader("About Canada's Time Zones")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    **Time Zone Facts:**
    - Canada spans 6 time zones from coast to coast
    - Newfoundland Time is unique with a 30-minute offset
    - Some provinces observe Daylight Saving Time
    - Saskatchewan mostly stays on standard time year-round
    """)

with col4:
    st.markdown("""
    **Geographic Coverage:**
    - **Pacific**: BC, Yukon
    - **Mountain**: Alberta, NWT  
    - **Central**: Saskatchewan, Manitoba
    - **Eastern**: Ontario, Quebec
    - **Atlantic**: Maritimes
    - **Newfoundland**: Newfoundland & Labrador
    """)

# Auto-refresh every minute
if st.button("🔄 Refresh Times"):
    st.rerun()
