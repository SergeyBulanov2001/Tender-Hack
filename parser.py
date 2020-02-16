import openpyxl
from openpyxl_image_loader import SheetImageLoader
import random
import string


class Parser:
    def __init__(self, xlsx_file, xlsx_info):
        self.file = xlsx_file
        self.info = xlsx_info

    def parse(self):

        wb = openpyxl.load_workbook(self.file)
        ws = wb.active

        column_counter = 1
        row_counter = 2

        finished = False

        last_cell = ws.cell(column=len(self.info), row=1)

        if last_cell.value is None:
            raise Exception("Inconsistency of the fields in the table and specified on the site")

        while not finished:
            final_array = []
            cell_content = ws.cell(column=column_counter, row=row_counter)
            cell_type = self.info[column_counter - 1]["type"]

            if cell_content.value is None and cell_type != "image":
                finished = True
            else:
                while cell_content.value is not None or cell_type == "image":
                    if column_counter > len(self.info):
                        break
                    cell_content = ws.cell(column=column_counter, row=row_counter)
                    cell_type = self.info[column_counter - 1]["type"]
                    cell_unit = self.info[column_counter - 1]["unit"]

                    if cell_type == "image":
                        image_loader = SheetImageLoader(ws)
                        image = image_loader.get(cell_content.coordinate)
                        image_token = self.generate_token(8)
                        image.save("data/images/{}.png".format(image_token))
                        cur_cell = {"content": "data/images/{}.png".format(image_token), "type": cell_type, "unit": cell_unit}
                        final_array.append(cur_cell)
                    else:
                        cur_cell = {"content": cell_content.value, "type": cell_type, "unit": cell_unit}
                        final_array.append(cur_cell)
                    column_counter += 1

            column_counter = 1
            row_counter += 1
            yield final_array

    def get_categories(self):

        category_column = None
        row_counter = 2

        for item in self.info:
            if item["type"] == "category":
                category_column = self.info.index(item) + 1

        if category_column is None:
            raise Exception('Category column not marked!')

        wb = openpyxl.load_workbook(self.file)
        ws = wb.active

        cell_content = ws.cell(column=category_column, row=row_counter)

        final_array = []

        while cell_content.value is not None:
            cell_content = ws.cell(column=category_column, row=row_counter)
            final_array.append(cell_content.value)
            row_counter += 1

        return set(final_array)

    def generate_token(self, length):
        alphabet = string.ascii_letters + string.digits
        token = ''
        for i in range(length):
            token += alphabet[random.randint(0, len(alphabet) - 1)]
        return token


if __name__ == '__main__':
    # TODO проверка одинаковых типов

    name = "name"
    company = "company"
    parser = Parser("data/esus.xlsx",
                    [{"type": "1", "unit": "1", "required": True}, {"type": "2", "unit": "1", "required": True}, {"type": "3", "unit": "1", "required": True},
                     {"type": "4", "unit": "1", "required": True}, {"type": "5", "unit": "1", "required": True}, {"type": "6", "unit": "1", "required": True},
                     {"type": "7", "unit": "1", "required": True}, {"type": "8", "unit": "1", "required": True}, {"type": "image", "unit": "1", "required": True},
                     {"type": "10", "unit": "1", "required": True}, {"type": "11", "unit": "1", "required": True}, {"type": "12", "unit": "1", "required": True},
                     {"type": "13", "unit": "1", "required": True}, {"type": "14", "unit": "1", "required": True}, {"type": "15", "unit": "1", "required": True},
                     {"type": "16", "unit": "1", "required": True}, {"type": "category", "unit": "1", "required": True}])
    get_iter = parser.parse()

    print(next(get_iter))
    print(next(get_iter))
    print(next(get_iter))

    print(parser.get_categories())
