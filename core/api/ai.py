import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ.get('CHATGPT_APIKEY')


class ChatGPT:
    engine: str = 'text-davinci-003'

    def prompt(self, text: str) -> str:
        return openai.Completion.create(
            max_tokens=300,
            engine=self.engine,
            prompt=text
        ).choices[0].text


class UniMajorDetail(ChatGPT):

    university_text: str = None

    def __init__(
            self,
            university_text: str
    ) -> None:
        self.university_text = university_text

    def get(self) -> dict:
        return json.loads(self.prompt(
            f'The following string is Iranian university data! please Convert "{self.university_text} to JSON in this format (if the province or city is not written, find the match province according to city or reverse). only write the json list without any text:' + json.dumps(
                {
                    'title': 'university name (persian)',
                    'provinces': ['university province 1 (persian)'],
                    'cities': ['university city 1 (persian)']
                }
            )
        ).strip())
