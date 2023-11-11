from typing import List
from ImageAnalysis import ImageAnalysis
from ImageTableExtraction import ImageTableExtraction

class SudokuDetection():
    def __init__(self, image_analysis: ImageAnalysis, table_extraction: ImageTableExtraction) -> None:
        self.image_analysis = image_analysis
        self.table_extraction = table_extraction

    def __trim_table(self, table):
        new_table = []
        for row_index in range(len(table)):
            if row_index >= 9:
                break
            new_row = []
            new_table.append(new_row)
            for col_index in range(len(table[row_index])):
                if col_index >= 9:
                    break
                new_row.append(table[row_index][col_index])
        return new_table

    def __trim__tables(self, tables):
        new_tables = []
        for table in tables:
            new_tables.append(self.__trim_table(table))
        return new_tables

    def __is_valid_sudoku_table(self, table):
        if len(table) != 9:
            return False
        for row in table:
            if len(row) != 9:
                return False
        for row in table:
            for col in row:
                if len(col) > 0 and not col.isdigit():
                    return False
        return True

    def __get_first_valid_sudoku(self, tables):
        trimmed = self.__trim__tables(tables)
        for table in trimmed:
            if self.__is_valid_sudoku_table(table):
                return (True, table)
        return (False, trimmed)

    def detect(self, image_bytes) -> List[List[str]]:
        success, analyzed = self.image_analysis.analyze(image_bytes)
        if not success:
            return (False, analyzed)
        success, tables = self.table_extraction.extract_tables(analyzed)
        if not success:
            return (False, tables)
        return self.__get_first_valid_sudoku(tables)
