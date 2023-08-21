import json
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

from core.api.ai import UniMajorDetail


class Attrs:

    # Years
    YEAR_1401: int = 101

    # School Major
    MATH: int = 1

    # UNI Majors
    COMPUTER_ENGINEERING: int = 250


class University(BaseModel):
    id: int
    title: str = None
    provinces: list = None
    cities: list = None


class AcceptanceHistoryItem(BaseModel):
    rank: int
    acceptance: str = None


class Kanoon:
    uni_api: str = 'https://www.kanoon.ir/EstimateKonkor/UpdateUni'
    report_api: str = 'https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors'


class Universities(Kanoon):
    year: int = None
    major: int = None
    uni_major: int = None

    def __init__(
            self,
            year: int,
            major: int,
            uni_major: int
    ) -> None:
        self.year = year
        self.major = major
        self.uni_major = uni_major

    def _req(self):
        return requests.get(
            url=self.uni_api,
            params={
                'year': str(self.year),
                'dept': str(self.major),
                'ReshteId': str(self.uni_major)

            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
        )

    def get(self) -> list[University]:
        req = self._req()
        if req.status_code == 200:
            return [
                University(
                    id=uni['UnivercityCode'],
                    title=uni['UnivercityName']
                    # **UniMajorDetail(uni['UnivercityName']).get()
                ) for uni in req.json()
            ]

        return []


class AcceptancesHistory(Kanoon):

    year: int = None
    major: int = None
    uni_major: int = None
    university: int = None
    area: int = 1

    def __init__(
            self,
            year: int,
            major: int,
            uni_major: int,
            university: int,
            area: int = 1,
    ) -> None:
        self.year = year
        self.major = major
        self.uni_major = uni_major
        self.university = university
        self.area = area

    def _req(self):
        return requests.post(
            url=self.report_api,
            json={
                'dept': str(self.major),
                'sahmieh': '0',
                'rank': '0',
                'reshte': str(self.uni_major),
                'year': str(self.year),
                'univercity': str(self.university),
                'type': '2'
            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
        )

    def get(self) -> list[AcceptanceHistoryItem]:
        req = self._req()
        if req.status_code == 200:
            data = []
            soup = BeautifulSoup(req.text, features='html.parser')
            table = soup.find('table')
            table_body = table.find('tbody')

            for r in table_body.find_all('tr', attrs={'class': f'Sahmieh-{self.area}'}):
                tds = r.find_all('td')
                data.append(
                    AcceptanceHistoryItem(
                        rank=int(tds[3].text),
                        acceptance=tds[7].text
                    )
                )

            return data

        return []
