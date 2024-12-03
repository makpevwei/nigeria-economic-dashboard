import streamlit as st
from nigeria_data_processor import load_and_process_data
import pandas as pd
import plotly.express as px


@st.cache_data
def load_and_process_data_cached():
    """
    Load and process data using a caching mechanism.
    
    Returns:
        pd.DataFrame: Processed dataset.
    """
    return load_and_process_data()


def end_before_start(start_year, end_year):
    """
    Check if the end year is before the start year.

    Args:
        start_year (int): Selected start year.
        end_year (int): Selected end year.

    Returns:
        bool: True if the end year is before the start year, False otherwise.
    """
    return start_year > end_year


@st.cache_data
def min_max_normalize(data, indicator):
    """
    Apply min-max normalization to scale data between 0 and 1.

    Args:
        data (pd.DataFrame): Input dataset.
        indicator (str): Column to normalize.

    Returns:
        pd.Series: Normalized values for the specified column.
    """
    min_val = data[indicator].min()
    max_val = data[indicator].max()
    if max_val - min_val == 0:
        return data[indicator]  # Avoid division by zero
    return (data[indicator] - min_val) / (max_val - min_val)


def format_large_numbers(value):
    """
    Format large numbers into readable units (e.g., millions, billions).

    Args:
        value (float): Numeric value to format.

    Returns:
        str: Formatted string.
    """
    if value >= 1e9:
        return f"{value / 1e9:.2f} Billion"
    elif value >= 1e6:
        return f"{value / 1e6:.2f} Million"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} Thousand"
    else:
        return f"{value:.2f}"


def display_dashboard(data, start_year, end_year, indicator, related_indicators):
    """
    Display the dashboard with visualizations for the selected indicator.

    Args:
        data (pd.DataFrame): The dataset to visualize.
        start_year (int): Start year for analysis.
        end_year (int): End year for analysis.
        indicator (str): Selected indicator for analysis.
        related_indicators (list): List of indicators for comparison.
    """
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "📊 Compare Years", "🔗 Indicator Relationships"])

    # Tab 1: Trend Analysis
    with tab1:
        st.subheader(f"{indicator} Trend from {start_year} to {end_year}")
        filtered_data = data[(data["Year"] >= start_year) & (data["Year"] <= end_year)]

        if not filtered_data.empty:
            fig = px.line(
                filtered_data,
                x="Year",
                y=indicator,
                title=f"{indicator} Trend ({start_year}-{end_year})",
                labels={"Year": "Year", indicator: f"{indicator}"},
                markers=True,
            )
            fig.update_layout(
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True),
                template="plotly_white",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No data available for the selected range.")

    # Tab 2: Yearly Comparison
    with tab2:
        st.subheader(f"Comparison of {indicator} between {start_year} and {end_year}")

        initial_value = data.loc[data["Year"] == start_year, indicator].values
        final_value = data.loc[data["Year"] == end_year, indicator].values

        initial_value = initial_value[0] if initial_value.size > 0 else None
        final_value = final_value[0] if final_value.size > 0 else None

        comparison_df = pd.DataFrame({
            "Year": [start_year, end_year],
            "Value": [initial_value, final_value]
        })

        col1, col2 = st.columns(2)
        with col1:
            if initial_value is not None:
                st.metric(label=f"{indicator} ({start_year})", value=format_large_numbers(initial_value))
            else:
                st.write(f"No data for {start_year}")
        with col2:
            if final_value is not None:
                delta = None if initial_value is None else f"{((final_value - initial_value) / initial_value * 100):.2f}%"
                st.metric(label=f"{indicator} ({end_year})", value=format_large_numbers(final_value), delta=delta)
            else:
                st.write(f"No data for {end_year}")

        fig = px.bar(
            comparison_df,
            x="Year",
            y="Value",
            title=f"{indicator} Comparison ({start_year} vs {end_year})",
            labels={"Value": f"{indicator} Value", "Year": "Year"},
            text=comparison_df["Value"].apply(format_large_numbers),  # Ensure text matches y-axis values
        )
        fig.update_traces(
            textposition="inside"  # Place labels inside the bars
        )
        fig.update_layout(
            template="plotly_white",
            xaxis=dict(type="category", categoryorder="array", categoryarray=[start_year, end_year]),
            yaxis=dict(showgrid=True),
            bargap=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Indicator Relationships (Normalized)
    with tab3:
        st.subheader("Compare Indicators Over Time (Normalized)")
        
        # Set default values for the select boxes
        default_x = "GDP (US$)"
        default_y = "Population Growth"
        
        # X-axis and Y-axis indicator selection with default values
        x_indicator = st.selectbox(
            "Select X-axis Indicator", 
            options=related_indicators, 
            index=related_indicators.index(default_x),
            key="x_indicator_relationship"
        )
        y_indicator = st.selectbox(
            "Select Y-axis Indicator", 
            options=related_indicators, 
            index=related_indicators.index(default_y),
            key="y_indicator_relationship"
        )

        # Normalize the selected indicators
        line_data = data[(data["Year"] >= start_year) & (data["Year"] <= end_year)].copy()
        line_data[x_indicator] = min_max_normalize(line_data, x_indicator)
        line_data[y_indicator] = min_max_normalize(line_data, y_indicator)

        if not line_data.empty:
            fig = px.line(
                line_data,
                x="Year",
                y=[x_indicator, y_indicator],
                labels={"Year": "Year", "value": "Normalized Value", "variable": "Indicator"},
                markers=True,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No data available for the selected range.")



def main():
    """
    Main function to run the Streamlit application.
    """
    st.title("Nigeria Economic and Demographic Dashboard")
    data = load_and_process_data_cached()

    with st.expander("See full data table"):
        display_df = data.copy()
        display_df["Year"] = display_df["Year"].astype(str)
        st.dataframe(display_df)

    st.info("Explore more global economic and demographic data on [World Bank Open Data](https://data.worldbank.org/).")

    indicator_options = [col for col in data.columns if col != "Year"]

    col1, col2, col3 = st.columns(3)
    with col1:
        start_year = st.slider("Start Year", min_value=int(data["Year"].min()), max_value=int(data["Year"].max()), value=1999)
    with col2:
        end_year = st.slider("End Year", min_value=int(data["Year"].min()), max_value=int(data["Year"].max()), value=2023)
    with col3:
        indicator = st.selectbox("Indicator", options=indicator_options, index=0)

    if end_before_start(start_year, end_year):
        st.error("End year must be greater than or equal to start year.")
    else:
        display_dashboard(data, start_year, end_year, indicator, indicator_options)


if __name__ == "__main__":
    main()
