import xlsxwriter
from core.api.kanoon import Universities, AcceptancesHistory, Attrs
from core.models import PackData
from core.writer import Table
from core.analyzer import AnalyzeRank

from rich.pretty import pprint

workbook = xlsxwriter.Workbook('mohammadreza.xlsx')
worksheet = workbook.add_worksheet(
    'My Worksheet'
)

year = Attrs.YEAR_1401
major = Attrs.MATH
uni_majors = [
    {
        'id': Attrs.COMPUTER_ENGINEERING,
        'title': 'مهندسی کامپیوتر'
    },
    {
        'id': 168,
        'title': 'مهندسی حرفه ای کامپیوتر'
    }
]
my_rank = 3053
area = 3


def data_major(m: int, m_title: str):
    return [
        PackData(
            detail=uni,
            possibility=AnalyzeRank(
                history=AcceptancesHistory(
                    year=year,
                    major=major,
                    uni_major=m,
                    university=uni.id,
                    area=area
                ).get(),
                rank=my_rank
            ).check(),
            major_title=m_title

        ) for uni in Universities(
            year=year,
            major=major,
            uni_major=m
        ).get()
    ]


Table(
    worksheet=worksheet,
    all_data=data_major(
        m=Attrs.COMPUTER_ENGINEERING,
        m_title='مهندسی کامپیوتر'
    ) + data_major(
        m=168,
        m_title='مهندسی حرفه ای کامپیوتر'
    )

).render()

workbook.close()
