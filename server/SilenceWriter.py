import requests
from config import Config
from logger import logger
import json


class SilenceWriter:

    @staticmethod
    def create_silence(payload: dict, user: str, folders: str) -> dict:
        SilenceWriter.format_json(payload, user, folders)

        if Config.DEBUG:
            print(f"formatted json: \n{json.dumps(payload)}")

        response = requests.request(
            method="POST",
            url=Config.API_PATH,
            headers={
                "Authorization": f"Bearer {Config.API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        )

        data = response.json()
        status_code = response.status_code

        if Config.DEBUG:
            print(f"response: \n{response}")

        try:
            return {"status_code": status_code, "silenceID": data["silenceID"]}
        except KeyError:
            return {"status_code": status_code, "failureMsg": data["message"]}

    @staticmethod
    def format_json(payload: dict, user: str, folders: str):
        try:
            payload["matchers"].insert(0, {  # Add Folder which user should have access to
                "name": "grafana_folder",
                "value": folders,
                "operator": "=~"
            })

            matchers = payload["matchers"]
            for matcher in matchers:
                operator = matcher["operator"]

                if operator == "=":
                    matcher["isEqual"] = True
                    matcher["isRegex"] = False

                elif operator == "!=":
                    matcher["isEqual"] = False
                    matcher["isRegex"] = False

                elif operator == "=~":
                    matcher["isEqual"] = True
                    matcher["isRegex"] = True

                elif operator == "!~":
                    matcher["isEqual"] = False
                    matcher["isRegex"] = True

                matcher.pop("operator", "")
            payload.pop("timestamp", "")
            payload.pop("timestamp", "")
            payload["startsAt"] = payload.pop("start")
            payload["endsAt"] = payload.pop("end")
            payload["createdBy"] = f"API {user}"

            # Format in IST
            payload["startsAt"] = payload["startsAt"] + ":00+05:30"
            payload["endsAt"] = payload["endsAt"] + ":00+05:30"

        except KeyError:
            logger.exception("[execution occurred]", user)
