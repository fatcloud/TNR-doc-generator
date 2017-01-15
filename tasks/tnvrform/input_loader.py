#! /usr/bin/env python

from openpyxl import load_workbook


class TNVRDataLoader(object):

    data = []

    def __init__(self, filename=None):
        if filename:
            self.load_xlsx(filename)


    def load_xlsx(self, filename):
        '''
        讀取輸入的 xlsx 檔，擷取出看起來像是資料的列，存入 self.data 這個變數中
        '''
        wb = load_workbook(filename=filename)
        sht = wb.worksheets[0]

        data = self.data
        data[:] = []

        for row in sht.rows:    
            if TNVRDataLoader.__looks_good(row):
                content = [cell.value for cell in row]
                data.append(content)
        

    @staticmethod
    def __looks_good(row):
        items = [cell.value for cell in row]
        
        # 跳過空行
        if items == [None] * len(items):
            return False
        
        # A 欄有字，整列無視
        return items[0] is None 



if __name__ == '__main__':
    loader = TNVRDataLoader(filename='example.xlsx')
    for row in loader.data:
        print(row, '\n')
    
