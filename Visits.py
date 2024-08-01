import streamlit as st
import matplotlib.colors as mcolors
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Centered and styled main title using inline styles
st.markdown('''
    <style>
        .main-title {
            color: #e66c37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SERVICE PROVIDER VISITS DASHBOARD</h1>', unsafe_allow_html=True)

data = pd.read_csv('cleaned_data_visit.csv')

data["visit_date"] = pd.to_datetime(data["visit_created_on"])

# Get minimum and maximum dates for the date input
startDate = data["visit_date"].min()
endDate = data["visit_date"].max()


# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create 2-column layout for date inputs
col1, col2 = st.columns(2)

# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date, key):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date, key=key)

# Display date inputs
with col1:
    date1 = display_date_input(col1, "Start Date", startDate, startDate, endDate, key="start_date")

with col2:
    date2 = display_date_input(col2, "End Date", endDate, startDate, endDate, key="end_date")

date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)
data = data[(data["visit_date"] >= date1) & (data["visit_date"] <= date2)].copy()

# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h2 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)



# Sidebar for filters
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=sorted(data['year'].unique()))
month = st.sidebar.multiselect("Select Month", options=sorted(data['MonthName'].unique()))
quarter = st.sidebar.multiselect("Select Quarter", options=sorted(data['quarter'].unique()))
visit_type = st.sidebar.multiselect("Select visit type", options=data['visit_type'].unique())


# Copy the data
filtered_data = data

    
# Filter by year
if year:
    filtered_data = filtered_data[filtered_data['year'].isin(year)]

# Filter by quarter
if quarter:
    filtered_data = filtered_data[filtered_data['quarter'].isin(quarter)]

# Filter by month
if month:
    filtered_data = filtered_data[filtered_data['MonthName'].isin(month)]

# Filter by visit type
if visit_type:
    filtered_data = filtered_data[filtered_data['visit_type'].isin(visit_type)]

# Convert visit_created_on from string to datetime
data['visit_created_on'] = pd.to_datetime(data['visit_created_on'])

# Calculate average visits
if not filtered_data.empty:
    try:
        visits_per_period = filtered_data.groupby(['year', 'quarter'])['visit_id'].count()
        average_visits = visits_per_period.mean() if not visits_per_period.empty else 0
    except Exception as e:
        st.error(f"Error calculating average visits: {e}")
        average_visits = 0
else:
    average_visits = 0

# Determine the filter description
filter_description = ""
if year:
    filter_description += f"{', '.join(map(str, year))} "
if quarter:
    filter_description += f"{', '.join(map(str, quarter))} "
if month:
    filter_description += f"{', '.join(month)} "
if visit_type:
    filter_description += f"{', '.join(visit_type)} "
if not filter_description:
    filter_description = "All Data"

if not filtered_data.empty:

    # Calculate metrics
    total_visits = len(filtered_data)
    day_visits = filtered_data[filtered_data['DayOrNight'] == 'Day'].shape[0]
    night_visits = filtered_data[filtered_data['DayOrNight'] == 'Night'].shape[0]

    # Create 4-column layout for metric cards
    col1, col2, col3, col4 = st.columns(4)

    # Define CSS for the styled boxes
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
        }
        .metric-title {
            color: #e66c37; /* Change this color to your preferred title color */
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #008040;
            font-size: 2em;
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)


    # Display metrics
    display_metric(col1, "Total Visits", f"{total_visits:.0f}")
    display_metric(col2, "Total Day Visits", f"{day_visits:.0f} ")
    display_metric(col3, "Total Night Visits", f"{night_visits:.0f}")
    display_metric(col4, f"Average Visits ({filter_description.strip()})", value=f"{average_visits:.2f}")

    fig_seasonal_visits = go.Figure(data=[go.Pie(
            labels=["Day", "Night"],
            values=[day_visits, night_visits],
            textinfo='label+percent',  # Show labels, values, and percentages
            hoverinfo='label+percent',  
            marker=dict(colors=['#1d340d', '#FF4500']),
    )])
    # Assuming filtered_data is your DataFrame
    filtered_data['visit_created_on'] = pd.to_datetime(filtered_data['visit_created_on'])

    # Extract the month and year from the 'visit_created_on' column
    filtered_data['visit_month'] = filtered_data['visit_created_on'].dt.to_period('M')

    # Get the month name for each visit
    filtered_data['MonthName'] = filtered_data['visit_created_on'].dt.strftime('%b %Y')

    # Count the number of visits per month
    visits_by_month = filtered_data['MonthName'].value_counts().sort_index()

    # Get the month with the maximum visits
    max_month = visits_by_month.idxmax()

    # Convert the max_month string to a datetime object
    max_month_datetime = pd.to_datetime(max_month)

    # Format the datetime object to the desired string format
    max_month_str = max_month_datetime.strftime('%b %Y')


    col1, col2 = st.columns(2)

    with col1:
            st.markdown('<h2 class="custom-subheader">Monthly Visits and Rate of Change</h2>', unsafe_allow_html=True)

            # Calculate the rate of change
            monthly_change = visits_by_month.pct_change() * 100  

            # Create the bar chart for visits
            bar_trace = go.Bar(
                x=visits_by_month.index.astype(str),
                y=visits_by_month.values,
                name='Number of Visits',
                marker_color='#008040',
                opacity=0.7
            )

            # Create the line chart for rate of change
            line_trace = go.Scatter(
                x=visits_by_month.index.astype(str),
                y=monthly_change,
                name='Rate of Change (%)',
                mode='lines+markers',
                marker=dict(color='#FF4500'),
                line=dict(color='#FF4500', width=2),
                yaxis='y2'  # Link the line trace to the secondary y-axis
            )

            # Create the figure and add both traces
            fig = go.Figure()
            fig.add_trace(bar_trace)
            fig.add_trace(line_trace)

            # Update layout
            fig.update_layout(
                xaxis=dict(title='Month'),
                yaxis=dict(
                    title='Number of Visits',
                    titlefont=dict(color='#008040'),
                    tickfont=dict(color='#008040')
                ),
                yaxis2=dict(
                    title='Rate of Change (%)',
                    titlefont=dict(color='#FF4500'),
                    tickfont=dict(color='#FF4500'),
                    overlaying='y',
                    side='right'
                ),
                legend=dict(
                    x=0.01,  # Position the legend inside the chart, close to the left
                    y=0.99,  # Position the legend at the top
                    xanchor='left',
                    yanchor='top',
                ),
                height=600,
                margin=dict(l=0, r=0, t=30, b=0)
            )

            # Display the plot
            st.plotly_chart(fig, use_container_width=True)

    with col2:
            st.markdown('<h2 class="custom-subheader">Seasonal Visits</h2>', unsafe_allow_html=True)
            st.plotly_chart(fig_seasonal_visits, use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
            with st.expander("Rate Of Change ViewData"):
                # Convert Series to DataFrame for styling
                monthly_change_df = monthly_change.to_frame(name='Rate of Change')
                st.write(monthly_change_df.style.background_gradient(cmap="YlOrBr"))

    with cl2:
            with st.expander("Day and Night Visits"):
                day_night_visits = pd.DataFrame({
                    "Type": ["Day", "Night"],
                    "Count": [day_visits, night_visits]
                })
                st.write(day_night_visits.style.background_gradient(cmap="YlOrBr"))

        
        # Create pie chart for visit types
    visits_by_type = filtered_data['visit_type'].value_counts()
    labels = visits_by_type.index.tolist()
    values = visits_by_type.values.tolist()
    colors = ["#1d340d", "#e66c37", "#3b9442", "#f8a785", "#CC3636"]  # Example color palette

    fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors[:len(labels)]),  # Ensure colors match number of labels
            textinfo='label+percent',  # Show label and percentage
            hoverinfo='label+percent'
        )])

    fig.update_layout(
            font=dict(color='black'),
            width=800,  
            height=600
        )

        # Top 10 Attending Doctor Specializations
    top_specializations = filtered_data['attending_doctor_specialisation'].value_counts().head(10)
    fig_specializations = go.Figure()

    fig_specializations.add_trace(go.Bar(
            y=top_specializations.index,
            x=top_specializations.values,
            orientation='h',
            marker=dict(color='#008040'),
            text=top_specializations.values,
            textposition='none',  
            hoverinfo='x+text'
        ))

    fig_specializations.update_layout(
            xaxis_title="Number of Visits",
            yaxis_title="Doctor Specialization",
            font=dict(color='white'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50)
        )

        # Displaying charts side by side
    col1, col2 = st.columns((2))

    with col1:
            st.markdown('<h2 class="custom-subheader">Visits by Visit Type</h2>', unsafe_allow_html=True) 
            st.plotly_chart(fig, use_container_width=True)

    with col2:
            st.markdown('<h2 class="custom-subheader">Top 10 Attending Doctor Specializations</h2>', unsafe_allow_html=True) 
            st.plotly_chart(fig_specializations, use_container_width=True)
        
    cols1, cols2 = st.columns((2))

    with cols1:
        with st.expander("Visit Type ViewData"):
                visit_count = filtered_data["visit_type"].value_counts().reset_index()
                visit_count.columns = ["Visit_type", "Count"]    
                st.write(visit_count.style.background_gradient(cmap="YlOrBr"))    

    with cols2:
            with st.expander("Specializations ViewData"):
                # Convert Series to DataFrame for styling
                spec_count = filtered_data["attending_doctor_specialisation"].value_counts().reset_index()
                spec_count.columns = ["attending_doctor_specialisation", "Count"]  
                st.write(spec_count.style.background_gradient(cmap="YlOrBr"))

    filtered_data['visit_created_on'] = pd.to_datetime(filtered_data['visit_created_on'])

    
    st.markdown('<h2 class="custom-subheader">Number of Visits By Day</h2>', unsafe_allow_html=True)

    custom_colors = ["#008040"]  # Replace with your desired colors

    # Group data by day and count visits
    daily_visits = filtered_data.groupby(filtered_data['visit_created_on'].dt.to_period('D')).size()
    daily_visits.index = daily_visits.index.to_timestamp()

    # Create a DataFrame for the daily visits
    daily_visits_df = daily_visits.reset_index()
    daily_visits_df.columns = ['Day', 'Number of Visits']

    # Create area chart for visits per day
    fig_area = go.Figure()

    fig_area.add_trace(go.Scatter(
        x=daily_visits_df['Day'],
        y=daily_visits_df['Number of Visits'],
        fill='tozeroy',
        mode='lines',
        marker=dict(color='#008040'),
        line=dict(color='#008040'),
        name='Number of Visits'
    ))

    fig_area.update_layout(
        xaxis_title="Days of the Month",
        yaxis_title="Number of Visits",
        font=dict(color='black'),
        width=1200,  # Adjust width as needed
        height=600   # Adjust height as needed
    )

    # Display the plot
    st.plotly_chart(fig_area, use_container_width=True)

    # Expander for Combined Data Table
    with st.expander("Visit Data Table", expanded=False):
        st.dataframe(daily_visits_df.style.background_gradient(cmap='YlOrBr'))
            
        # Data
    st.markdown("""
            <style>
            .chart-container {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .chart-container:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            </style>
            """, unsafe_allow_html=True)

    st.markdown('<h2 class="custom-subheader">Month-Wise Visit Type Summary</h2>', unsafe_allow_html=True)

    with st.expander("Summary Table"):
            colors = ["#527853", "#F9E8D9", "#F7B787", "#EE7214", "#B99470"]
            custom_cmap = mcolors.LinearSegmentedColormap.from_list("EarthyPalette", colors)
            
            st.markdown("Month-Wise Preauthorization By Amount Table")
            filtered_data["month"] = filtered_data["visit_created_on"].dt.month_name()
            
            # Create the pivot table
            sub_specialisation_Year = pd.pivot_table(
                data=filtered_data,
                values="visit_id",  # Assuming "PreAuth Amount" is the correct column name
                index=["visit_type"],
                columns="month",
                aggfunc='count'
            )
            
            st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr"))
            
else:
    st.error("No data available for this selection")
