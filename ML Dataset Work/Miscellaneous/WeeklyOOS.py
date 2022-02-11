import pandas as pd

oos = pd.read_excel(r"C:\Users\rmalekzai\Downloads\Venture OOS Order Report.xlsx", sheet_name="Out of Stock items")
back = pd.read_excel(r"C:\Users\rmalekzai\Downloads\Venture OOS Order Report.xlsx",
                     sheet_name="Items W Severe BO Status")

# oos_trim = oos[["OOS Items", "Description", "Vendor", "ETA this week"]]

df = pd.DataFrame(columns=["Issue", "Item Number", "Description", "Vendor", "ETA this week", "Comments"])
columns = ["Issue", "Item Number", "Description", "Vendor", "ETA this week", "Comments"]

#Add OOS Items
temp = pd.DataFrame(columns=["OOS ITEMS", "Description", "Vendor", "ETA this week", "Comments"])
for x in range(len(oos.index)):
    if oos.iloc[x]["USPD Use"] == "Yes":
        temp = temp.append(oos.iloc[x][["OOS ITEMS", "Description", "Vendor", "ETA this week"]])
temp.columns = ["Item Number", "Description", "Vendor", "ETA this week", "Comments"]
temp["Issue"] = "Out of Stock"
temp = temp.reindex(columns=columns)
df = df.append(temp)

#Add Projected to run out
temp = pd.DataFrame(columns=["Item Number", "Description", "Vendor", "This week ETA", "Comments"])
for x in range(len(back.index)):
    if back.iloc[x]["USPD Use"] == "Yes" and back.iloc[x]["Projected to run out (Y/N)"] == "Y":
        temp = temp.append(back.iloc[x][["Item Number", "Description", "Vendor", "This week ETA"]])
temp.columns = ["Item Number", "Description", "Vendor", "ETA this week", "Comments"]
temp["Issue"] = "Projected to run out"
temp = temp.reindex(columns=columns)
df = df.append(temp)

#Add Backordered
temp = pd.DataFrame(columns=["Item Number", "Description", "Vendor", "This week ETA", "Comments"])
for x in range(len(back.index)):
    if back.iloc[x]["USPD Use"] == "Yes" and back.iloc[x]["Projected to run out (Y/N)"] == "N":
        temp = temp.append(back.iloc[x][["Item Number", "Description", "Vendor", "This week ETA"]])
temp.columns = ["Item Number", "Description", "Vendor", "ETA this week", "Comments"]
temp["Issue"] = "Backordered"
temp = temp.reindex(columns=columns)
df = df.append(temp)

df.to_excel(r"C:\Users\rmalekzai\Downloads\WeeklyReport.xlsx")