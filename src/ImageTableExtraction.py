from typing import List

class ImageTableExtraction():
    def get_rows_columns_map(self, table_result, blocks_map):
        rows = {}
        for relationship in table_result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}
                            
                        # get the text value
                        rows[row_index][col_index] = self.get_text(cell, blocks_map)
        return rows

    def get_text(self, result, blocks_map):
        text = ''
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
        return text

    def extract_tables(self, image_analysis):
        blocks = image_analysis['Blocks']
        blocks_map = {}
        table_blocks = []
        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)
        if len(table_blocks) <= 0:
            return (False, "No tables found with AWS Textract.")
        tables = []
        for _, table in enumerate(table_blocks):
            tables.append(self.create_table(table, blocks_map))
        return (True, tables)

    def __clean_table(self, table: List[List[str]]):
        for row_index in range(len(table)):
            for col_index in range(len(table[row_index])):
                table[row_index][col_index] = table[row_index][col_index].strip()

    def create_table(self, table_result, blocks_map):
        rows = self.get_rows_columns_map(table_result, blocks_map)
        table = []
        for _, cols in rows.items():
            row = []
            table.append(row)
            for _, text in cols.items():
                row.append(text)
        self.__clean_table(table)
        return table