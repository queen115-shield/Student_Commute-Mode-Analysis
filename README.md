# Student Commute Mode Analysis

**Author:** Rishta Bharti  
**Program:** B.Tech CSE (AI & ML), 1st Semester  
**Institution:** CGC University  
**Project:** Data Science Mini-Project

> The bundled 120-row dataset is **synthetic demonstration data**. It is not an actual university survey. Replace it with consented real survey responses before reporting campus-specific results.

## Features
- CSV dataset and cleaning pipeline
- Jupyter Notebook for introductory analysis
- Eight saved static visualizations
- Summary statistics and mode comparisons
- Illustrative carbon emissions calculation
- Commute burden score (illustrative index)
- Streamlit interactive dashboard with filters
- What-if emissions scenario and rule-based commute suggestions
- Project report, presentation, survey questionnaire, survey report template and viva guide

## Quick start
1. Install Python 3.10+.
2. Open terminal in this project folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the analysis:
   `python analysis.py`
5. Launch dashboard:
   `streamlit run dashboard/app.py`
6. Open notebook:
   `jupyter notebook notebooks/commute_analysis.ipynb`

## Data fields
Student_ID, Year, Section, Hostel_DayScholar, Commute_Mode, Distance_km, Travel_Time_min, Daily_Cost_INR, Days_Per_Week.

## Visualizations
The `images/` folder contains mode count, mode share, distance histogram, travel-time box plot, distance-time scatter, year-mode heatmap, average-cost chart, and stacked year-wise mode chart.

## Sustainability assumptions
Emission factors are illustrative teaching assumptions in kg CO2 per passenger-km. They should be verified against authoritative current sources and documented for any formal study. Calculations currently use one-way distance.

## Survey
Copy questions from `survey/survey_questionnaire.docx` into Google Forms. Keep the survey anonymous; do not collect names, phone numbers or exact addresses. Replace the synthetic CSV with downloaded survey data after cleaning columns to match.

## GitHub upload
Create a repository named `student-commute-mode-analysis`, upload this project folder, and include the README. Avoid uploading private respondent information.

## Student
Rishta Bharti | B.Tech CSE (AI & ML) | 1st Semester | CGC University
