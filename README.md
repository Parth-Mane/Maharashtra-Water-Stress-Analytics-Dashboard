Maharashtra Water Stress Analytics Dashboard

#Overview

This project analyzes water stress patterns across Maharashtra’s districts using government datasets. 
It combines Evapotranspiration (ET) and Soil Moisture data to compute a custom Water Stress Index (ET − Soil Moisture), 
highlighting regions facing potential agricultural and water resource challenges.
The insights are visualized through an interactive Power BI dashboard, enabling data-driven monitoring, planning, and p
olicy support for sustainable water management.


#Objectives

1.Identify districts with high water stress using the ET−SoilMoisture metric.

2.Track temporal changes in evapotranspiration and soil moisture levels.

3.Provide data freshness KPIs to ensure updated monitoring.

4.Enable visual decision support for government and research use cases.


#Key Features

1.Calculated Metric: Water Stress Index (ET − Soil Moisture)

2.Interactive Power BI Dashboard with filters by State, District, and Date

3.Visuals: Heatmaps, KPIs, and Trend Graphs

4.Data Refresh Indicator to track the latest update date

5.District-Level Insights showing the most affected regions


#Data Pipeline

1.Extract: Data pulled from Government Open Data portals (Evapotranspiration & Soil Moisture datasets).

2.Transform:

  *Cleaned and merged data using Python (Pandas)
      
  *Derived calculated fields like Water Stress = ET − Soil Moisture
      
  *Stored processed data in MySQL database
      
3.Load & Visualize: Imported clean dataset into Power BI for dashboard creation and analysis.


#Tech Stack

1.Languages: Python, SQL

2.Libraries: Pandas, NumPy, MySQL Connector

3.Visualization: Power BI

4.Data Source: Government Open Data Portal


#Dashboard Highlights

1.Max Water Stress Districts: Identifies the top stressed regions dynamically.

2.Temporal Analysis: Tracks ET & Soil Moisture trends over time.

3.KPIs: Shows data freshness and overall water stress metrics.

4.Geospatial Heatmaps: Visual representation of stress intensity across Maharashtra.

#Folder Structure

    📁 Maharashtra-Water-Stress-Dashboard
    ├── 📂 data
    │   ├── evapotranspiration.csv
    │   ├── soil_moisture.csv
    ├── 📂 py_code
    │   ├── ETL_pipeline.py
    ├── 📂 dashboard
    │   ├── Maharashtra_Water_Stress.pbix
    └── README.md


#Results

1.Identified top 5 most water-stressed districts in Maharashtra.

2.Built a visual analytics tool for real-time monitoring.

3.Supported evidence-based insights for water management and agriculture planning.

#Future Scope

1.Integrate live API data for real-time updates.

2.Expand analysis to pan-India level.

3.Add machine learning models for stress prediction.

#Acknowledgment

Data sourced from Government of India Open Data Portal and Maharashtra State Water Resource Department.
