import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Streamlit app
st.title('Total Runs Scored in Every Over by Both Teams')

# File uploader to upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read data from the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Group by Over Number and Batting Team to get total runs scored in each over
    over_runs = df.groupby(['Over Number', 'Batting Team'])['Runs'].sum().reset_index()

    # Assuming 'dismissals' is part of the uploaded CSV file
    if 'Dismissals' in df.columns:
        dismissals = df[['Over Number', 'Batting Team', 'Dismissals']]
        # Merge with dismissals to identify overs with dismissals
        over_runs = over_runs.merge(dismissals, on=['Over Number', 'Batting Team'], how='left')

        # Set opacity to 0.5 if there is a dismissal, otherwise 1.0
        over_runs['opacity'] = over_runs['Dismissals'].apply(lambda x: 0.5 if x > 0 else 1.0)
    else:
        over_runs['opacity'] = 1.0

    # Create the Manhattan chart with different opacities for different phases
    fig = px.bar(over_runs, x='Over Number', y='Runs', color='Batting Team', barmode='group',
                 title='Total Runs Scored in Every Over by Both Teams',
                 labels={'Runs': 'Total Runs', 'Over Number': 'Over Number'},
                 opacity=over_runs['opacity'])

    # Update the layout to set the background color
    fig.update_layout(
        plot_bgcolor='#1D3040',
        paper_bgcolor='#1D3040',
        font_color='white'
    )

    # Add dotted white lines to differentiate phases
    fig.add_shape(type="line", x0=6.5, y0=0, x1=6.5, y1=max(over_runs['Runs']) + 5,
                  line=dict(color="white", width=2, dash="dot"))
    fig.add_shape(type="line", x0=15.5, y0=0, x1=15.5, y1=max(over_runs['Runs']) + 5,
                  line=dict(color="white", width=2, dash="dot"))

    # Add annotations for the phases with highlighted text
    fig.add_annotation(x=3.5, y=max(over_runs['Runs']) + 5, text="Powerplay", showarrow=False, font=dict(color="black", weight="bold"), bgcolor="rgba(255, 255, 255, 1)")
    fig.add_annotation(x=11, y=max(over_runs['Runs']) + 5, text="Middle overs", showarrow=False, font=dict(color="black", weight="bold"), bgcolor="rgba(255, 255, 255, 1)")
    fig.add_annotation(x=17.5, y=max(over_runs['Runs']) + 5, text="Death overs", showarrow=False, font=dict(color="black", weight="bold"), bgcolor="rgba(255, 255, 255, 1)")

    # Display the chart in the Streamlit app
    st.plotly_chart(fig)
