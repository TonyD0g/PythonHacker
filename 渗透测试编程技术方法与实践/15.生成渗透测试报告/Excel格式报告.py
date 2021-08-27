"""
    Python数据处理 处理Excel: https://www.jianshu.com/p/7546f4bd2b8a

"""
import xlsxwriter
workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet()
#创建一个图表对象.
chart = workbook.add_chart({'type': 'column'})
# 向工作表中添加一些数据
data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
]
worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])
worksheet.write_column('C1', data[2])
# 添加数据序列
chart.add_series({'values': '=Sheet1!$A$1:$A$5'})
chart.add_series({'values': '=Sheet1!$B$1:$B$5'})
chart.add_series({'values': '=Sheet1!$C$1:$C$5'})
# 将图表插入到工作表中
worksheet.insert_chart('A7', chart)
workbook.close()