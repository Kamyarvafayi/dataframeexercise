# In[] for tranforming Jalali to Gregorian and Vice Versa
# import jdatetime
# import jalali_pandas
# # gregorian_date = jdatetime.date(1396, 2, 30).togregorian()
# # current_Year = datetime.today().year
# # current_Month = datetime.today().month
# # current_Day = datetime.today().day

# # jalili_date = jdatetime.datetime.fromgregorian(day = current_Day, month=current_Month, year=current_Year)
# # # jalili_date = datetime.strptime(str(jalili_date), '%Y-%m-%d %H:%M:%S')
# # Gregorian_Date = jdatetime.date.togregorian(jalili_date)

# Gregorian_Date = datetime.date(datetime.today())

# CurrentTime = datetime.strptime(str('07:00:00'), '%H:%M:%S')
# CurrentCombinedDateTime = datetime.combine(Gregorian_Date, CurrentTime.time())

# MachinePlannedTime = {}
# MachinePlannedTime2 = {}
# MachinePlannedTime3 = {}
# Last_Product_M = {}

# PlanStatusTable['Date'] = PlanStatusTable['Date'].astype(str)
# PlanStatusTable['Date'] = PlanStatusTable['Date'].jalali.parse_jalali("%Y%m%d")
# PlanStatusTable['Date'] = PlanStatusTable['Date'].jalali.to_gregorian()

# In[]: The Main Part
import pandas as pd

mysource = pd.read_excel(r'C:/Users/k.vafaeinejad/Desktop/Test.xlsx')

mysource2 = mysource.groupby(by = ['Drugstore_ID', 'Line'])['Invoice_Sales'].sum().reset_index()

All_DrugStores = pd.unique(mysource2['Drugstore_ID'])

Targeted_DrugStores = []
for DS in All_DrugStores:
    tempDF = mysource2[mysource2['Drugstore_ID'] == DS]
    AvailableLines = pd.unique(tempDF.Line)
    if 'انکولوژی شیمیایی' in AvailableLines and 'انکولوژی بیولوژیک' in AvailableLines and 'نفرولوژی' in AvailableLines and 'خود ایمنی و پوکی استخوان' in AvailableLines:
        if 'نورولوژی شیمیایی' in AvailableLines and 'نورولوژی بیولوژیک' in AvailableLines:
            Targeted_DrugStores.append(DS)

Active_Indices = mysource2['Drugstore_ID'].isin(Targeted_DrugStores)

mysource3 = mysource2[Active_Indices].reset_index(drop = False)

Active_Drug_Stores = pd.unique(mysource3['Drugstore_ID'])

Line_List = ['انکولوژی شیمیایی', 'انکولوژی بیولوژیک', 'نفرولوژی', 'خود ایمنی و پوکی استخوان']

Total_Sales = {}
Total_Sales_To_Line_List = {}

Key_DrugStores = []
for DS in Active_Drug_Stores:
    tempDF = mysource3[mysource3['Drugstore_ID'] == DS]
    Total_Sales[DS] = tempDF.Invoice_Sales.sum()

    Active_Indices2 = tempDF['Line'].isin(Line_List)
    tempDF2 = tempDF[Active_Indices2]

    Total_Sales_To_Line_List[DS] = tempDF2.Invoice_Sales.sum()

    if Total_Sales_To_Line_List[DS]/Total_Sales[DS] <= 0.9:
        Key_DrugStores.append(DS)

Active_Indices3 = mysource['Drugstore_ID'].isin(Key_DrugStores)

KeyDS_DF = mysource[Active_Indices3]
