import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_missing_values_chart(df):
    """
    Create a horizontal bar chart for missing values per column.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze.
    
    Returns:
        go.Figure: Plotly figure for missing values.
    """
    missing_counts = df.isna().sum()
    missing_counts = missing_counts[missing_counts > 0]  # Only show columns with missing values
    
    if missing_counts.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No missing values found.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(
            title="Missing Values per Column",
            height=300
        )
        return fig
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=missing_counts.values,
            y=missing_counts.index,
            orientation='h',
            marker_color='#7B169E'
        )
    )
    fig.update_layout(
        title="Missing Values per Column",
        xaxis_title="Number of Missing Values",
        yaxis_title="Column",
        height=max(300, len(missing_counts) * 30),  # Dynamic height based on number of columns
        template="plotly_white"
    )
    return fig

def create_text_case_chart(case_analysis_df):
    """
    Create a subplot for text case analysis (uppercase, lowercase, title case).
    
    Args:
        case_analysis_df (pd.DataFrame): Dataframe with case analysis results.
    
    Returns:
        go.Figure: Plotly figure with subplots for each column.
    """
    if case_analysis_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No text columns to analyze.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(
            title="Text Case Analysis",
            height=300
        )
        return fig
    
    columns = case_analysis_df.columns
    fig = make_subplots(
        rows=1,
        cols=len(columns),
        subplot_titles=columns,
        shared_yaxes=True
    )
    
    for i, col in enumerate(columns, start=1):
        fig.add_trace(
            go.Bar(
                x=case_analysis_df[col].index,
                y=case_analysis_df[col].values,
                name=col,
                marker_color=['#7B169E', '#7B169E', '#7B169E']  # Colors for uppercase, lowercase, title case
            ),
            row=1,
            col=i
        )
    
    fig.update_layout(
        title="Text Case Analysis (Uppercase, Lowercase, Title Case)",
        height=400,
        showlegend=False,
        template="plotly_white"
    )
    fig.update_yaxes(title_text="Count", row=1, col=1)
    return fig