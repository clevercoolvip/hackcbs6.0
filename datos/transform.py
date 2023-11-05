import pandas as pd
from stats import *
import matplotlib.pyplot as plt
import plotly.express as px
import plotly as plt



path = "data.csv"
data = pd.read_csv(path)
removenan(data)

def run_transform(data):
    int_col = []
    object_col = []


    for col in data.columns:
        if (check_dtype(data[col])):
            int_col.append(col)
        else:
            object_col.append(col)




    #<-------------------------- Int Col ------------------------------>
    def getinfo_int_col(col):
        ans = {}
        SKEWNESS = skewness(col)
        KURTOSIS = kurtosis(col)
        MEAN = mean(col)
        MEDIAN = median(col)
        STD = std(col)
        COLUMN_DESCRIPTION = column_description(col) #json
        DOMAINS = domains(col) #json
        DIVERSITY = diversity_in_percentage(col) #json
        name = None
        ans["colname"] = None
        try:
            name = col.name
        except:
            pass
        

        #correlation between two columns
        corr_strings = []
        for i in int_col:
            val = correlation_between(col, data[i])
            if (val<0.99 and val>0.5):
                corr_strings.append(f"-> column {col.name} and {data[i].name} are directly proportional. If {col.name} increases then {data[i].name} increases!\n")
            if(val>-0.99 and val<-0.5):
                corr_strings.append(f"-> column {col.name} and {data[i].name} are inversely proportional. If {col.name} increase then {data[i].name} decreases! and vice-versa\n")

        ans["corr"] = f"{' and '.join(corr_strings)}"



    #name of the column
        if name:
            ans["colname"] = name

    # finding outliers and suggesting outliers
        if SKEWNESS > -0.5 and SKEWNESS < 0.5:
            ans["skewness"] = "-> The data might not have any outlier but unsure (kurtosis test)\n"
        else:
            ans["skewness"] = "-> The data has outliers as indicated by skewness\n"
        

        if KURTOSIS > 2.8 and KURTOSIS<3.2:
            ans["kurtosis"] = "-> The data has limited vulnerable outliers (can be ignored)\n"
        elif KURTOSIS<2.8:
            ans["kurtosis"] = "-> The data has outliers and vulnerable values as indicated by kurtosis\n"

    #domains
        string = "-> "
        for key in DOMAINS.keys():
            string += f"{key} value in the column is {DOMAINS[key]}\n" 
        ans["domains"] = string

    #diversity
        ans["diversity_low"] = f"-> {DIVERSITY['diverse']}% of the values are greater then {DIVERSITY['val_range'][0]} and are less then {DIVERSITY['val_range'][1]}\n"

    #average
        ans["average"] = f"-> {MEAN} is the average value of this column\n"
        ans["columns_description"] = f"-> {COLUMN_DESCRIPTION['Description']}\n"

        return ans



    for column in int_col:
        result = getinfo_int_col(data[column])
        with open("results.txt", "a+") as f:
            if result["colname"]:
                f.write(f" For column {result['colname']} : \n")
            else:
                f.write(f" For column {column} : \n")

            for key in result:
                if key!="colname":
                    f.write(result[key])

            f.write("\n")

            f.write("----------------- Changing column -------------------\n")

            f.write("\n")

            f.close()


    #<----------------------------- object_col ---------------------->

    def getinfo_object_col(col):
        UNIQUE_COUNT = len(pd.unique(col))
        if UNIQUE_COUNT<10:
            ax = px.bar(data_frame=data, x=col,)
            ax.write_html(f"plots/barplots/res{col.name}.html")


    for i in data.columns:
        getinfo_object_col(data[i])

    #< ----------------------Test Graphs --------------->
    #line chart
    # for i in range(len(int_col)):
    #     for j in range(i+1, len(int_col)):
    #         if len(pd.unique(data[int_col[i]]))>20 and len(pd.unique(data[int_col[j]]))>20:
    #             ax = px.line(data_frame=data, x=data[int_col[i]], y=data[int_col[j]])
    #             ax.write_html(f"plots/line/fig{int_col[i]}-{int_col[j]}.html")


    #< ---------------------- Graphs --------------->

    if int_col:
        for i in int_col:
            if len(pd.unique(data[i]))>20:
                ax = px.line(data_frame=data, x=data[i], y=range(len(data[i])))
                ax.write_image(f"plots/line/fig{i}.png")

            else:
                ax = px.histogram(data, x=data[i], color=data[i])
                ax.write_image(f"plots/barplots/fig{i}.png")


    if object_col:
        for j in object_col:
            if len(pd.unique(data[j]))<10:
                ax = px.histogram(data, x=data[j], color=data[j])
                ax.write_image(f"plots/barplots/fig{j}.png")



if __name__=="__main__":
    run_transform(data)