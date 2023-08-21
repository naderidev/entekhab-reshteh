import xlsxwriter
from core.models import PackData
from rich.pretty import pprint

class Table:
    headers: list = [
        {'header': ' کد رشته '},
        {'header': ' نام دانشگاه '},
        {'header': ' استان '},
        {'header': ' شهر '},
        {'header': ' اولویت '},
        {'header': ' احتمال قبولی '},
        {'header': ' روزانه / نوبت دوم '},
    ]

    def __init__(
            self,
            worksheet: xlsxwriter.workbook.Worksheet,
            all_data: list[PackData] = []
    ) -> None:
        self.all_data = all_data
        self.worksheet = worksheet
    
    def render(self):
        data = self.get_data()
        self.worksheet.add_table(
            'B2:H' + str(len(data)),
            {
                'data': self.get_data(),
                'columns': self.headers,
                'name': 'Entekhab_Reshteh'
            },
        )

    def get_data(self) -> list:
        return [
            [
                None,
                data.detail.title,
                data.detail.province,
                data.detail.city,
                None,
                data.possibility,
                None

            ] for data in self.all_data
        ]
