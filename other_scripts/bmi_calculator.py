import numpy as np
import pandas as pd
import re


def height_conversion(height):
    """convert the various height formats into just inches"""
    num_list = re.findall(r"\d+", height)
    inches = int(num_list[0]) * 12 + int(num_list[1])
    return inches


def weight_conversion(weight):
    """convert the various height formats into just inches"""
    num_list = re.findall(r"(\d+)", weight)
    if int(num_list[0]) <= 120:
        pounds = int(num_list[0]) * 2.2
    else:
        pounds = int(num_list[0])
    return pounds


def calculate_bmi(height, weight):
    """calculate the BMI given the height in inches and the weight in pounds"""
    m_weight = 703 * weight
    m_height = height**2
    bmi = m_weight / m_height
    return bmi


def bmi_magic(data):
    """function to correct the values in the height and weight columns"""
    data['BMI'] = np.nan
    for i, row in data.iterrows():
        data.at[i, "Height"] = height_conversion(data.at[i, "Height"])
        data.at[i, "Weight"] = weight_conversion(data.at[i, "Weight"])
        data.at[i, "BMI"] = calculate_bmi(data.at[i, "Height"], data.at[i, "Weight"])
    return data


def main():
    """main part of the script"""
    draft_class = 56
    from_csv = 'smjhl-2020-09-10.csv'
    to_csv = 'S' + str(draft_class) + '-bmi.csv'


    full_data = pd.read_csv(f"../{from_csv}")
    draft_class_data = full_data.loc[full_data['Draft Class Numeric'] == draft_class].copy()
    height_weight_raw = draft_class_data[["First Name", "Last Name", "Height", "Weight"]]

    bmi_chart = bmi_magic(height_weight_raw)
    bmi_chart = bmi_chart.sort_values(by=["BMI"], axis=0, ascending=False)

    # print(full_data)
    print(bmi_chart)
    bmi_chart.to_csv(to_csv)


main()
