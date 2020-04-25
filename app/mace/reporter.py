# TODO: implement reporting
# This class is in charge of taking attributes
# from the Mace fitted object and turn it into
# an Excel file to be written on disk
from pandas import DataFrame, ExcelWriter
from pathlib import Path
from app.mace.mace import Mace
from app.config import UPLOAD_FOLDER


class MaceReporter(object):
    """
    Create excel file report to send to user.
    """

    def __init__(self, data: Mace, filename: str):

        self.data = {

            "first_sheet": DataFrame({}),

            "second_sheet": DataFrame({})

        }

        self.destination = Path(__file__).parent / \
            UPLOAD_FOLDER / f"attachment_{filename}.xslx"

    def save(self) -> None:
        """
        Method to save the algorithm results to an Excel file.
        It expects sheet names and pandas DataFrames.
        """
        with ExcelWriter(self.destination) as file_writer:
            for sheet_name, dataframe in self.data.items():
                dataframe.to_excel(file_writer, sheet_name, index=False)
