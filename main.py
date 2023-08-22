import itertools
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

Table(
    worksheet=worksheet,
    all_data=list(
        itertools.chain(
            *[

                [
                    PackData(
                        detail=uni,
                        possibility=AnalyzeRank(
                            history=AcceptancesHistory(
                                year=year,
                                major=major,
                                uni_major=_major['id'],
                                university=uni.id,
                                area=area
                            ).get(),
                            rank=my_rank
                        ).check(),
                        major_title=_major['title']

                    ) for uni in Universities(
                        year=year,
                        major=major,
                        uni_major=_major['id']

                    ).get()
                ] for _major in uni_majors
            ]
        )
    )

).render()

workbook.close()
