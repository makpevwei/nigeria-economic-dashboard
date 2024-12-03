### Nigeria Economic and Demographic Dashboard
This repository contains a Streamlit application for visualizing and analyzing key economic and demographic indicators of Nigeria. The app allows users to explore trends, compare data across years, and analyze relationships between various indicators in an interactive and user-friendly interface.

### Project Structure
The repository is organized as follows:
- ```nigeria_dashboard_app.py```: The main Streamlit application file. It serves as the front end of the dashboard, where users can select indicators, time ranges, and compare trends.
- ```data_processor.py```: A utility module responsible for loading, cleaning, and processing the dataset. It ensures the data is well-formatted and ready for visualization.
- ```nigeria_indicators_data.csv```: The dataset containing Nigeria's economic and demographic indicators, which is loaded and processed by the app.

### Features
1. **Trend Analysis**:
- Visualize the trend of a selected indicator over a user-defined time range using line charts.
- Compare multiple normalized indicators to understand their patterns over time.
2. **Yearly Comparison**:
- Compare the values of a selected indicator between two years using bar charts and metrics.
- Analyze changes with percentage differences displayed dynamically.
3. **Indicator Relationships**:
- Explore relationships between indicators using normalized comparisons.
- Compare multiple indicators over the years to identify       correlations or divergences.

### Prerequisites
Before running the application, ensure you have the following:
1. Python 3.7+
2. Necessary Python libraries:
- ```streamlit```
- ```pandas```
- ```numpy```
- ```plotly```

### Dataset Processing
The dataset is cleaned and preprocessed in data_processor.py to ensure consistency and usability. Below are some key steps in the processing:
1. **Column Renaming**: Columns are renamed to concise and user-friendly names.
2. **Year Formatting**: The Year column is formatted as integers.
    Data Type Conversion: Columns are converted to appropriate data types (float64 for numeric data).
3. **Handling Missing Values**: Zero values in the year 2023 are replaced with NaN to improve data clarity.
4. **GDP Formatting**: GDP values are converted from scientific notation to readable integers.

### Example Dataset (Columns)
The dataset includes the following indicators:
- Year
- Fertility Rate
- GDP (US$)
- GDP Growth (%)
- Life Expectancy
- Female Population (%)
- Male Population (%)
- Population Growth
- Urban Growth (%)
- Rural Growth (%)
- Employment Ratio (%)
- Male Employment (%)
- Female Employment (%)
- Female Unemployment (%)
- Male Unemployment (%)
- Total Unemployment (%)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Streamlit application:
```bash
streamlit run nigeria_dashboard_app.py
```

### Usage
### Default Dashboard
1. Select a **start year** and **end year** for analysis.
2. Choose an indicator from the dropdown menu to analyze its trends or compare its values between years.
3. Switch between tabs to explore:
- Trend Analysis: View time-series data.
- Yearly Comparison: Compare indicator values for two years.
- Indicator Relationships: Analyze normalized relationships between indicators.

### Normalized Comparisons
In the **Indicator Relationships** section:
- The default indicators for X-axis and Y-axis are **GDP (US$)** and **Population Growth**, respectively.
- Users can select alternative indicators from the dropdown menus to explore relationships.

### Acknowledgments
 **Data Source**: [World Bank Open Data](https://data.worldbank.org/)
- **Visualization Frameworks**:
  - [Streamlit](https://streamlit.io/)
  - [Plotly](https://plotly.com/)