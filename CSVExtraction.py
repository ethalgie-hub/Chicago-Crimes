import plotly.express as px
import pandas as pd 

# py -m pip install plotly (terminal) to install plotly if not already installed

# Data Sources:
# Src_1, Crime_Reports.csv  : https://catalog.data.gov/dataset/crime-reports-bf2b7
# Src_2, Crimes_20251129.csv: https://data.cityofchicago.org/Public-Safety/Crimes-Map/dfnk-7re6
# Src_2, CrimeDate.csv      : https://www.kaggle.com/datasets/elijahtoumoua/chicago-analysis-of-crime-data-dashboard


### DATA EXTRACTION FROM CSV FILE 1: Crime_Reports.csv 
with open('Crime_Reports.csv') as file1:
    data = file1.readlines() #list each indice is a line with the commas included
    file1_list_csv = []
    for line in data:
        file1_list_csv.append(line.strip().split(','))
        
    id1_column0  = [] #Incident Number
    id1_column1  = [] #Highest Offense Description
    id1_column2  = [] #Highest Offense Code
    id1_column3  = [] #Family Violence
    id1_column5  = [] #Occurred Date
    id1_column6  = [] #Occurred Time
    id1_column10 = [] #Location Type
    id1_column11 = [] #Council District
    
    Location_Type_Crude  = set()

    for r in range(1,len(file1_list_csv)):
        id1_column0.append(file1_list_csv[r][0])
        id1_column1.append(file1_list_csv[r][1])
        id1_column2.append(file1_list_csv[r][2])
        id1_column3.append(file1_list_csv[r][3])
        id1_column5.append(file1_list_csv[r][5])
        id1_column6.append(file1_list_csv[r][6])
        id1_column10.append(file1_list_csv[r][10])
        id1_column11.append(file1_list_csv[r][11])
        Location_Type_Crude.add(file1_list_csv[r][10])

    zipped_lists1 = list(zip(id1_column0, id1_column1,  id1_column2, id1_column3,
                             id1_column5, id1_column6, id1_column10, id1_column11))
    DataFrameScr1 = pd.DataFrame(zipped_lists1, columns=['Incident Number', 'Highest Offense Description',
                                                         'Highest Offense Code', 'Family Violence', 'Occurred Date',
                                                        'Occurred Time', 'Location Type', 'Council District'])

### DATA EXTRACTION FROM CSV FILE 2: Crimes_20251129.csv
with open('Crimes_20251129.csv') as file2:
    pass

### DATA EXTRACTION FROM CSV FILE 3: CrimeDate.csv
with open('CrimeDate.csv') as file3:
    data = file3.readlines() #list each indice is a line with the commas included
    file3_list_csv = []
    for line in data:
        file3_list_csv.append(line.strip().split(','))
    id3_column0 = [] # Date
    id3_column1 = [] # Type of Crime
    id3_column2 = [] # Number of Crimes
    id3_column3 = [] # Number of arrests
    id3_column4 = [] # Non arrested
    id3_date = []

    for r in range(1,len(file3_list_csv)):
        id3_column0.append(file3_list_csv[r][0])
        id3_column1.append(file3_list_csv[r][1])
        id3_column2.append(file3_list_csv[r][2])
        id3_column3.append(file3_list_csv[r][3])
        id3_column4.append(file3_list_csv[r][4])
        id3_date.append(list(file3_list_csv[r][0])[0:4]) 


DataFrameScr3 = pd.read_csv('CrimeDate.csv')



def find_min_max(values, mode):
    if mode == 'max':
        max = int(values[0])

        for v in values:
            v = int(v)
            if v > max:
                max = v
        return max

    elif mode == 'min':
        min = int(values[0])

        for v in values:
            v = int(v)
            if v < min:
                min = v
        return min
    
    else:
        return None



#________________________________________________________________________________________________#



### VISUALIZATION 1 DENSITY OF CRIMES PER TYPE on bar chart ### Q1

vis_1 = px.pie(DataFrameScr3,
                values='arrest_count',
                names='primary_type',
                title='Percentage Distribution of Crime Types (2001-2022)',
                hover_data=['crime_count']
                )
vis_1.update_traces(textposition='inside',
                     textinfo='percent+label')
vis_1.show()

### VISUALIZATION 2: DENSITY OF CRIMES PER TYPE per year on bubble chart ### Q1

step = 7
df_small = DataFrameScr3.iloc[::step]

vis_2 = px.scatter(
    df_small,
    x="arrest_count",
    y="crime_count",
    size="arrest_count",
    color="primary_type",
    hover_name="primary_type",
    log_x=True,
    size_max=120,
    animation_frame="date",
    title="Crime by Type Over Time (Sampled)"
)

vis_2.show()

### VISUALIZATION 3: What proportion of offenders are actually arrested? ### Q2

import plotly.express as px


arrested_per_year = {}
not_arrested_per_year = {}

for i in range(len(id3_date)):
    year_str = "" # id3_date[i] = ['2','0','1','5']
    for j in range(4):
        year_str += str(id3_date[i][j])
    year = int(year_str)

    if year >= 2010:
        a = int(id3_column3[i])
        n = int(id3_column4[i])

        if year not in arrested_per_year:
            arrested_per_year[year] = 0
        if year not in not_arrested_per_year:
            not_arrested_per_year[year] = 0

        arrested_per_year[year] += a
        not_arrested_per_year[year] += n



years = sorted(arrested_per_year.keys())

arrested_vals = []
not_arrested_vals = []
for y in years:
    arrested_vals.append(arrested_per_year[y])
    not_arrested_vals.append(not_arrested_per_year[y])



fused_years = years + years
fused_counts = arrested_vals + not_arrested_vals
typed_arrests = (['ARRESTED'] * len(years)) + (['NOT ARRESTED'] * len(years))



vis_3 = px.line(
    x=fused_years,
    y=fused_counts,
    color=typed_arrests,
    markers=True,
    title="Arrested vs Not Arrested Over Time",
    labels={'x': 'Year', 'y': 'Number of Incidents'}
)

vis_3.update_layout(xaxis=dict(type='category')) 
vis_3.show()


### VISUALIZATION 4: How have crime levels changed over the past several years? ### Q3

crimes_per_year_month = {}

for i in range(0, len(DataFrameScr1)):
    year = DataFrameScr1['Occurred Date'][i][-4:]
    mon  = DataFrameScr1['Occurred Date'][i][0:2]

    
    if year not in crimes_per_year_month:
        crimes_per_year_month[year] = {}

    
    if mon not in crimes_per_year_month[year]:
        crimes_per_year_month[year][mon] = 1
    else:
        crimes_per_year_month[year][mon] += 1
    
month_order = ['01','02','03','04','05','06','07','08','09','10','11','12']
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


years_list = []
months_list = []
values_list = []

for year in sorted(crimes_per_year_month.keys()):
    months = month_order[:] 
    values = [crimes_per_year_month[year].get(m, 0) for m in months]

    years_list.append(year)
    months_list.append(months)
    values_list.append(values)

Year_col  = []
Month_col = []
Count_col = []

for i in range(len(years_list)):
    for j in range(12):
        Year_col.append(str(years_list[i]))
        Month_col.append(month_names[j]) 
        Count_col.append(values_list[i][j])

df_vis4 = pd.DataFrame({
    "Year": Year_col,
    "Month": Month_col,
    "Crimes": Count_col
})


vis_4 = px.scatter(
    df_vis4,
    x="Month",
    y="Crimes",
    animation_frame="Year",
    category_orders={"Month": month_names},
    title="Monthly Crimes",
    size_max=50,
    range_y=[0, find_min_max(Count_col, 'max')],
)

vis_4.update_layout(xaxis_title="Month", yaxis_title="Number of Crimes")
vis_4.show()

    




### VISUALIZATION 5: Crime Counts by Council District ### Q4

Council_District_dict = {}

for district in id1_column11:
    if district == '':
        district = 'N/A'
    if str(district) not in Council_District_dict:
        Council_District_dict[str(district)] = 1
    else:
        Council_District_dict[str(district)] += 1

if 'N/A' in Council_District_dict:
    del Council_District_dict['N/A']


Council_District_dict = dict(
    sorted(Council_District_dict.items(), key=lambda x: int(x[0]))
)

vis_5 = px.bar(
    x=list(Council_District_dict.keys()),
    y=list(Council_District_dict.values()),
    title='Crime Counts by Council District',
    labels={'x': 'Council District', 'y': 'Number of Crimes'}
)

vis_5.update_layout(bargap=0.2)
vis_5.show()



### VISUALIZATION 1: Location Types Distribution ### Q n/a

Location_Types_dict = {}
for type in id1_column10:
    if type == '':
        type = 'UNCATEGORIZED'
    if type not in Location_Types_dict:
        Location_Types_dict[type] = 1
    else:
        Location_Types_dict[type] += 1


vis_6 = px.bar(x=list(Location_Types_dict.values()),
                         y=list(Location_Types_dict.keys()),
                        title="Crime Distribution by Location Type",
                        labels={'x': 'Number of Crimes', 'y': 'Location Type'},
                        log_x=True, 
                        )

vis_6.show()


### Export
vis_1.write_html("vis_1.html")
vis_2.write_html("vis_2.html")
vis_3.write_html("vis_3.html")
vis_4.write_html("vis_4.html")
vis_5.write_html("vis_5.html")
vis_6.write_html("vis_6.html")