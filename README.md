# AWS Cloud Club Data Processing Tool

[![GitHub](https://img.shields.io/badge/GitHub-JpCurada-blue?logo=github)](https://github.com/JpCurada)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-jpcurada-blue?logo=linkedin)](https://www.linkedin.com/in/jpcurada/)

Welcome to the **AWS Cloud Club Data Tool**, a Streamlit-based application designed to streamline membership application processing for the AWS Cloud Club at PUP. This project was entrusted to me by our club captain, Kuya Aki, as part of our ongoing efforts to enhance our club's data management processes. The tool provides an intuitive interface for uploading, analyzing, and editing member data, ensuring data quality and accuracy.

The app is live and accessible at: [https://awsccpup-data-tool.streamlit.app/](https://awsccpup-data-tool.streamlit.app/)

---

## 📖 Project Overview

The AWS Cloud Club Data Tool is built to assist the club's leadership in managing membership applications efficiently. It offers features for data quality checks, filtering, editing, and visualization, with a focus on ensuring clean and reliable data. Key functionalities include:

- **Data Upload and Editing**: Upload CSV files containing member data and edit them interactively using a data editor.
- **Data Quality Checks**:
  - Display key metrics (total rows, unique webmails, duplicate webmails, non-webmail members).
  - Visualize missing values per column and text case analysis (uppercase, lowercase, title case) for name fields.
- **Filtering and Analysis**:
  - Filter data by duplicates, missing values, or specific values.
  - Perform string similarity analysis to identify similar entries.
- **Change Tracking and Download**:
  - Track edit history with timestamps and before/after values.
  - Download edited data as a CSV file.

This project is a collaborative effort, and I'm grateful to Kuya Aki for entrusting me with this task. It's been a rewarding experience to contribute to our club's mission of fostering a vibrant AWS community.

---

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.9
- **Streamlit**: 1.43.0
- Install dependencies from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### Running the App Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/JpCurada/jpcurada-awscc-data-tool.git
   cd jpcurada-awscc-data-tool
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Access the app at `http://localhost:8501`.

Alternatively, you can use the live deployment at [https://awsccpup-data-tool.streamlit.app/](https://awsccpup-data-tool.streamlit.app/).

---

## 📂 Directory Structure

```
jpcurada-awscc-data-tool/
├── README.md                 # Project documentation
├── helpers.py                # Utility functions for data processing
├── requirements.txt          # Project dependencies
├── streamlit_app.py          # Main Streamlit application
├── visualizations.py         # Plotly visualization functions
├── static/                   # Static assets
│   ├── styles.css            # Custom CSS for styling
│   └── images/               # Image assets (e.g., header)
└── .streamlit/               # Streamlit configuration
    └── config.toml           # Theme and app settings
```

---

## 🛠️ Features and Implementation

### Core Features
- **Data Upload and Editing**:
  - Upload CSV files for member data and Certificates of Registration (COR).
  - Interactive data editor with change tracking and download functionality.
- **Data Quality Checks**:
  - Display metrics using Streamlit's `st.metric` for total rows, unique webmails, duplicate webmails, and non-webmail members.
  - Visualize missing values and text case analysis using Plotly charts (horizontal bar charts and subplots).
- **Filtering and Analysis**:
  - Filter data by duplicates, missing values, or specific search terms.
  - Perform string similarity analysis using `difflib.SequenceMatcher` to identify similar strings above a threshold.
- **Customization**:
  - Custom CSS in `static/styles.css` for a polished UI, including Poppins font and AWS Cloud Club branding (primary color: `#7B169E`).
  - Theme configuration in `.streamlit/config.toml` for a dark theme.

### Key Files
- **`helpers.py`**:
  - Functions for cleaning column names, adjusting names for download, calculating metrics, analyzing text case, and finding similar strings.
- **`visualizations.py`**:
  - Plotly visualization functions for missing values and text case analysis, with custom styling (e.g., bar color `#7B169E`).
- **`streamlit_app.py`**:
  - Main application logic, including page setup, session state management, filter controls, data editor, and tabs for members and COR data.

---

## 🌟 Usage Notes

- **Members Data Overview Tab**:
  - Upload member data and view data quality metrics and visualizations.
  - Use filters to inspect duplicates, missing values, or specific values in the data editor.
  - Edit data interactively and track changes in the edit history.
  - Download edited data as a CSV file.
- **Extract COR Tab**:
  - Upload Certificate of Registration data (functionality under development).

The app is designed to be user-friendly, with tooltips and clear layouts to guide users. Filters apply only to the data editor, while metrics and visualizations remain static, reflecting the original data.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the tool or add new features, feel free to:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your changes align with the project's goals and follow best practices for code quality and documentation.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- **Kuya Aki**: For entrusting me with this project and providing guidance.
- **AWS Cloud Club PUP**: For fostering a supportive community and inspiring this tool.
- **Streamlit and Plotly Communities**: For their amazing tools and documentation.

---

## 📬 Contact

Feel free to reach out for questions, feedback, or collaboration:

- **GitHub**: [JpCurada](https://github.com/JpCurada)
- **LinkedIn**: [jpcurada](https://www.linkedin.com/in/jpcurada/)

Let's continue building tools that empower our AWS Cloud Club community! 🚀

