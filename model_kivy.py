import json
from datetime import datetime


class DictionaryItem:
    def __init__(self, word_id, word, translation):
        self.id = word_id
        self.word = word
        self.translation = translation


class LeitnerItem:
    def __init__(self, dictionary_item):
        self.id = dictionary_item.id
        self.word = dictionary_item.word
        self.translation = dictionary_item.translation
        self.level = 1
        self.day = 0  # 0 means never reviewed


class Project:
    def __init__(self, user_name="Sanaz"):
        self.user_name = user_name
        self.create_date = datetime.now().date()
        self.dictionary = {}  # key: word_id, value: DictionaryItem
        self.box = {}         # key: word_id, value: LeitnerItem

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "create_date": self.create_date.isoformat(),
            "dictionary": {
                k: {
                    "word": v.word,
                    "translation": v.translation
                } for k, v in self.dictionary.items()
            },
            "box": {
                k: {
                    "word": v.word,
                    "translation": v.translation,
                    "level": v.level,
                    "day": v.day
                } for k, v in self.box.items()
            }
        }

    @staticmethod
    def from_dict(data):
        project = Project(data["user_name"])
        project.create_date = datetime.fromisoformat(
            data["create_date"]
        ).date()

        project.dictionary = {
            k: DictionaryItem(k, v["word"], v["translation"])
            for k, v in data["dictionary"].items()
        }

        project.box = {}
        for k, v in data["box"].items():
            item = LeitnerItem(project.dictionary[k])
            item.level = v["level"]
            item.day = v["day"]
            project.box[k] = item

        return project

    def save_to_file(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                self.to_dict(),
                f,
                ensure_ascii=False,
                indent=4
            )

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Project.from_dict(data)
