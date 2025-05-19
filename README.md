
# Player Comparison Radar

## Description
This is an interactive web application to compare football players who play as Right Wingback Defenders using pizza plots.
The app allows users to select two players from the dropdown menus and generates a visual comparison using radar charts (pizza plots) to analyze their performance metrics.

## Features
- Interactive player selection using dropdowns.
- Generates pizza plots for visual comparison.
- Uses percentile ranks to normalize player statistics.
- Compares two players side by side.

## Technologies Used
- Python
- Streamlit (for the web interface)
- pandas (for data manipulation)
- matplotlib and mplsoccer (for radar chart visualization)
- highlight_text (for annotated text in plots)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hashim125/player-profiling-app.git
   ```

2. Navigate to the project directory:
   ```bash
   cd player-profiling-app
   ```

3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Execute the following command to start the Streamlit server:
```bash
streamlit run app.py
```
Then, open the URL provided by Streamlit (usually `http://localhost:8501`) in your browser.

## How to Use
1. Select two players from the dropdown menus.
2. The app will display a comparison pizza plot with the selected players' statistics.
3. View the percentile rankings to compare player performance.

