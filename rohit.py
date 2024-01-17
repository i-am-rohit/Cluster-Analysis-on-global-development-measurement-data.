from json import load
from pdb import run
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO



def main():
    st.markdown("# Interactive dashboard for clustering")
    st.markdown('<style>description{color:blue;}</style>', unsafe_allow_html=True)
    st.markdown("<description>This web-app shows some interactive plots that "+
                "helps analysing clustering results. It runs SQL queries on a "+
                "BigQuery public dataset: the London bicycles (EU region).</description>", unsafe_allow_html=True
    )
    
    st.sidebar.markdown("## Select the analysis step")
    step = st.sidebar.radio("", ["Load Data", "EDA"])
    if step == "Load Data":
        load_data()
    
    elif step == "EDA":
        explorate()



def load_data():
    multiple_files = st.file_uploader('CSV',type="csv", accept_multiple_files=True)
    for file in multiple_files:
        dataframe = pd.read_csv(file)
        file.seek(0)
        st.write(dataframe)



def explorate():
    tab1, tab2, tab3 = st.tabs(["Data Info", "Numeric Features", "Categorical Features"])
    multiple_files = st.file_uploader('CSV',type="csv", accept_multiple_files=True)
    for file in multiple_files:
        df = pd.read_csv(file)
    with tab1:
        if multiple_files is not None:
            # extract meta-data from the uploaded dataset

            st.header("Columns")

            st.markdown(list(df.columns))


            st.header("Meta-data")

            row_count = df.shape[0]

            column_count = df.shape[1]
            
            # Use the duplicated() function to identify duplicate rows
            duplicates = df[df.duplicated()]
            duplicate_row_count =  duplicates.shape[0]

            missing_value_row_count = df[df.isna().any(axis=1)].shape[0]

            table_markdown = f"""
            | Description | Value | 
            |---|---|
            | Number of Rows | {row_count} |
            | Number of Columns | {column_count} |
            | Number of Duplicated Rows | {duplicate_row_count} |
            | Number of Rows with Missing Values | {missing_value_row_count} |
            """

            st.markdown(table_markdown)

            st.header("Columns Type")

            # get feature names
            df = df.dropna()

            columns = list(df.columns)
             


            # create dataframe
            column_info_table = pd.DataFrame({
                "column": columns,
                "data_type": df.dtypes.tolist()
            })
            
            # display pandas dataframe as a table
            st.dataframe(column_info_table, hide_index=True)

            

    with tab2:
        if multiple_files is not None:
            # find numeric features  in the dataframe
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            
            st.header("Numerical Columns")
            st.markdown(numeric_cols)


            # birth = df["Birth Rate"].tolist()
            # birth = df["Birth Rate"].fillna(0)

            # st.markdown(birth)


            # numeric_cols = numeric_cols.fillna().mean()

            # numeric_cols = df[numeric_cols].dropna().unique()

            # add selection-box widget
            selected_num_col = st.selectbox("Which numeric column do you want to explore?", numeric_cols)

            

            st.header(f"{selected_num_col} - Statistics")

            # uni_value = df[selected_num_col].nunique
            # miss_value = df[selected_num_col].isnull().sum()
            # mean_value = df[selected_num_col].mean()

            table_markdown = f"""
            | Description | Value | 
            |---|---|
            | Number of Unique Values | {df[selected_num_col].nunique()} |
            | Number of Rows with Missing Values | {df[selected_num_col].isnull().sum()} |
            | Average Value | {df[selected_num_col].mean()} |
            | Minimum Value | {df[selected_num_col].min()} |
            | Maximum Value | {df[selected_num_col].max()} |
            | Median Value | {df[selected_num_col].median()} |
            """
            st.markdown(table_markdown)

            # col_info["Number of Rows with Missing Values"] = df[selected_num_col].isnull().sum()
            # col_info["Number of Rows with 0"] = df[selected_num_col].eq(0).sum()
            # col_info["Number of Rows with Negative Values"] = df[selected_num_col].lt(0).sum()
            # col_info["Average Value"] = df[selected_num_col].mean()
            # col_info["Standard Deviation Value"] = df[selected_num_col].std()
            # col_info["Minimum Value"] = df[selected_num_col].min()
            # col_info["Maximum Value"] = df[selected_num_col].max()
            # col_info["Median Value"] = df[selected_num_col].median()

            # info_df = pd.DataFrame({"Description" : })

            # info_df = pd.DataFrame(list(col_info.items()), columns=['Description', 'Value'])
            # # display dataframe as a markdown table
            # st.dataframe(info_df)

            st.header("Histogram")
  

    with tab3:
        if multiple_files is not None:
            # find categorical columns in the dataframe
            cat_cols = df.select_dtypes(include='object')
            cat_cols_names = cat_cols.columns.tolist()

            st.header("Categorical Columns")
            st.markdown(cat_cols_names)

            # add select widget
            selected = st.selectbox("Which text column do you want to explore?", cat_cols_names)

            st.header(f"{selected}")

            
            
            # add categorical column stats
            cat_col_info = {}
            cat_col_info["Number of Unique Values"] = (df[selected].nunique())
            cat_col_info["Number of Rows with Missing Values"] = df[selected].isnull().sum()
            cat_col_info["Number of Empty Rows"] = df[selected].eq("").sum()
            cat_col_info["Number of Rows with Only Whitespace"] = len(df[selected][df[selected].str.isspace()])
            cat_col_info["Number of Rows with Only Lowercases"] = len(df[selected][df[selected].str.islower()])
            cat_col_info["Number of Rows with Only Uppercases"] = len(df[selected][df[selected].str.isupper()])
            cat_col_info["Number of Rows with Only Alphabet"] = len(df[selected][df[selected].str.isalpha()])
            cat_col_info["Number of Rows with Only Digits"] = len(df[selected][df[selected].str.isdigit()])
            # cat_col_info["Mode Value"] = df[selected].mode()[0]

            cat_info_df = pd.DataFrame(list(cat_col_info.items()), columns=['Description', 'Value'])
            st.dataframe(cat_info_df)





main()