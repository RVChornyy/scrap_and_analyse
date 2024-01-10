import csv
import datetime
from dataclasses import dataclass, astuple, fields

from technologies import POSSIBLE_TECHNOLOGIES

BASE_URL = "https://work.ua/"


@dataclass
class Vacancy:
    date: datetime.date | None
    title: str
    site_id: str
    company: str
    technology_stack: list
    salary_margin: list | None
    salary: int | None
    required_experience: int


class PreCleanData:
    @staticmethod
    def clean_salary_margin(salary: str | list) -> list | str:
        salary_data = (salary[:-4].
                       replace(" ", "").
                       replace(" – ", "-").
                       split("-"))
        try:
            clean_salary_margin = [int(item) for item in salary_data]
        except ValueError:
            return "As interview result"

        return clean_salary_margin

    @staticmethod
    def clean_technology_stack(data: str) -> list[str]:

        return [tech for tech in POSSIBLE_TECHNOLOGIES if tech.lower() in data.lower()]

    @staticmethod
    def clean_experience(data: str) -> int:
        for item in data.strip().split():
            try:
                years = int(item)
            except ValueError:
                pass
            else:
                return years

    @staticmethod
    def clean_date(date_data) -> datetime:
        try:
            data_to_transform = date_data[date_data.index("від") + 4:].split()
        except ValueError:
            return None
        months = ("січня", "лютого", "березня", "квітня", "травня",
                  "червня", "липня", "серпня", "вересня", "жовтня",
                  "листопада", "грудня")
        data_to_transform[1] = months.index(data_to_transform[1]) + 1

        date = datetime.date(*[int(i) for i in data_to_transform][::-1])

        return date


class FileWriter:
    @staticmethod
    def write_to_csv(filename: str, data: list[Vacancy]) -> None:
        file_path = f"..\\data_analysis\\{filename}.csv"
        with open(file_path, "w", newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            writer.writerow([field.name for field in fields(Vacancy)])
            writer.writerows([astuple(vacancy) for vacancy in data])
        with open("../data_analysis/filename.txt", "w") as text_file:
            text_file.write(file_path)
