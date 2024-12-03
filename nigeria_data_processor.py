import pandas as pd
import numpy as np
import os


def load_and_process_data():
    """
    Load and process the Nigeria indicators dataset.

    Steps:
    1. Load the CSV file dynamically.
    2. Rename columns to more concise and user-friendly names.
    3. Ensure the 'Year' column is properly formatted as integers.
    4. Convert columns to appropriate data types.
    5. Handle scientific notation for GDP values.
    6. Replace zero values for 2023 with NaN for better clarity.

    Returns:
        pd.DataFrame: Processed DataFrame with cleaned and standardized data.
    """
    # Construct the file path dynamically
    file_path = os.path.join(os.path.dirname(__file__), 'nigeria_indicators_data.csv')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Rename columns for better readability and usability
    rename_columns = {
        "Year": "Year",
        "Fertility Rate": "Fertility Rate",
        "GDP (current US$)": "GDP (US$)",
        "GDP Growth (annual %)": "GDP Growth (%)",
        "Life Expectancy (Years)": "Life Expectancy",
        "Female Population (% Total)": "Female Population (%)",
        "Male Population (% Total)": "Male Population (%)",
        "Population Growth (annual %)": "Population Growth (%)",
        "Urban Population Growth (annual %)": "Urban Growth (%)",
        "Rural Population Growth (annual %)": "Rural Growth (%)",
        "Employment to population ratio, 15+, total (%) ": "Employment Ratio (%)",
        "Employment to population ratio, 15+, male (%) ": "Male Employment (%)",
        "Employment to population ratio, 15+, female (%)": "Female Employment (%)",
        "Unemployment, female (% of female labor force) ": "Female Unemployment (%)",
        "Unemployment, male (% of male labor force)": "Male Unemployment (%)",
        "Unemployment, total (% of total labor force) ": "Unemployment (%)",
    }

    # Apply column renaming
    df.rename(columns=rename_columns, inplace=True)

    # Ensure the "Year" column is treated as integer type
    # Keep only the last 4 digits of the year if there's an unexpected formatting
    df["Year"] = df["Year"].apply(lambda x: int(str(x)[-4:]))

    # Define the desired data type conversions for each column
    convert_dtype = {
        "Year": np.int64,
        "Fertility Rate": np.float64,
        "GDP (US$)": np.float64,
        "GDP Growth (%)": np.float64,
        "Life Expectancy": np.float64,
        "Female Population (%)": np.float64,
        "Male Population (%)": np.float64,
        "Population Growth": np.float64,
        "Urban Growth (%)": np.float64,
        "Rural Growth (%)": np.float64,
        "Employment Ratio (%)": np.float64,
        "Male Employment (%)": np.float64,
        "Female Employment (%)": np.float64,
        "Female Unemployment (%)": np.float64,
        "Male Unemployment (%)": np.float64,
        "Unemployment (%)": np.float64,
    }

    # Apply the type conversion to the DataFrame
    df = df.astype(convert_dtype)

    # Convert GDP values to float without scientific notation, rounded to integers
    df['GDP (US$)'] = df['GDP (US$)'].apply(lambda x: float(f"{x:.0f}"))

    # Replace zero values in 2023 with NaN for all columns except "Year"
    for column in df.columns:
        if column != "Year":
            df.loc[(df["Year"] == 2023) & (df[column] == 0), column] = np.nan

    # Return the cleaned and processed DataFrame
    return df
