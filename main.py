import xlsxwriter
from core.api.kanoon import Universities, AcceptancesHistory, Attrs
from core.models import PackData
from core.writer import Table
from core.analyzer import AnalyzeRank

from rich.pretty import pprint

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet(
    'My Worksheet'
)

year = Attrs.YEAR_1401
major = Attrs.MATH
uni_major = Attrs.COMPUTER_ENGINEERING
my_rank = 3053
area = 3

Table(
    worksheet=worksheet,
    all_data=[
        PackData(
            detail=uni,
            possibility=AnalyzeRank(
                history=AcceptancesHistory(
                    year=year,
                    major=major,
                    uni_major=uni_major,
                    university=uni.id,
                    area=area
                ).get(),
                rank=my_rank
            ).check()
        ) for uni in Universities(
            year=year,
            major=major,
            uni_major=uni_major
        ).get()
    ]
).render()

workbook.close()
