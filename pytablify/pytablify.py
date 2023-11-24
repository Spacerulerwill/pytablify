from typing import Any, Optional


def grid_to_string(
    arr: list[list[Any]],
    hPadding: Optional[int] = 1,
    cChar: Optional[str] = "+",
    hChar: Optional[str] = "-",
    vChar: Optional[str] = "|",
) -> str:
    """
    Convert a 2d array 'grid' to a string and return the string\n
    arr - 2d array to convert\n
    hPadding - the horizontal padding between data and the column lines\n
    cChar - the character used for corners in the grid - str\n
    hChar - the character used for horizontal - str\n
    vChar - the character used for vertical seperations - str\n
    """

    # if empty 2d array - return a box shape
    if len(arr) == 1 and len(arr[0]) == 0:
        return "Empty Table"

    # find grid cols and rows
    gridCols = len(max(arr, key=lambda x: len(x)))  # <- as wide as longest sublist

    # iterate through data, find widest element for each column
    # this + hPadding*2 will be the width of the entire column
    columnWidths = []
    for i in range(gridCols):
        column = [el[i] for el in arr if i < len(el)]  # get column

        # get max width of element in each column
        maxWidthElem = ""
        for elem in column:
            sep = str(elem).split("\n")
            for s in sep:
                if len(s) > len(maxWidthElem):
                    maxWidthElem = s

        columnWidths.append(len(maxWidthElem))  # append to list by column index

    # max row heights for each row
    rowHeights = []
    for row in arr:
        maxRowElemHeight = (
            str(max(row, key=lambda x: str(x).count("\n") + 1)).count("\n") + 1
        )  # height of each row in amount of \n + 1
        rowHeights.append(maxRowElemHeight)

    # construct grid seperator with grid widths found
    gridSeperator = "\n"
    for width in columnWidths:
        gridSeperator += cChar + hChar * (width + hPadding * 2)
    gridSeperator += cChar

    constructedString = ""

    # print grid with new column widths
    for row, i in enumerate(arr):
        rowHeight = rowHeights[row]
        constructedString += gridSeperator
        for h in range(rowHeight):
            constructedString += "\n"
            for col in range(gridCols):
                colWidth = columnWidths[col] + hPadding * 2
                try:
                    raw_elem = arr[row][col]
                    if raw_elem == None:
                        constructedString += vChar + " " * colWidth
                    else:
                        split = str(raw_elem).split("\n")
                        centered_elem = str(split[h]).center(colWidth, " ")
                        constructedString += "|" + centered_elem
                except IndexError:
                    constructedString += vChar + " " * colWidth

                # if last column, add last vChar
                if col == gridCols - 1:
                    constructedString += vChar
    constructedString += gridSeperator

    return constructedString


class Table:
    def __init__(
        self,
        columnTitles: list[str],
        rowTitles: list[str],
        hPadding: Optional[int] = 1,
        cChar: Optional[str] = "+",
        hChar: Optional[str] = "-",
        vChar: Optional[str] = "|",
    ):
        if len(columnTitles) == 0:
            raise ValueError("Must have atleast 1 column title")

        if len(rowTitles) == 0:
            raise ValueError("Must have atleast 1 row title")

        self._data = {
            rowTitle: {columnTitle: "" for columnTitle in columnTitles}
            for rowTitle in rowTitles
        }
        self._columnTitles = columnTitles
        self._rowTitles = rowTitles
        self._hPadding = hPadding
        self._cChar = cChar
        self._hChar = hChar
        self._vChar = vChar

    def __str__(self):
        return grid_to_string(
            # first row (header columns)
            [[""] + [columnTitle for columnTitle in self._columnTitles]] +
            # all other rows
            [
                ([rowTitle] + list(rowData.values()))
                for rowTitle, rowData in self._data.items()
            ],
            hPadding=self._hPadding,
            cChar=self._cChar,
            hChar=self._hChar,
            vChar=self._vChar,
        )
    
    def __getitem__(self, key: str) -> dict:
        return self._data[key] 
    
    def aggregate_as_list(self, key: str) -> list:
        return [row[key] for row in self._data.values()]
    
    def aggregate_as_dict(self, key: str) -> dict:
        return {dataKey: row[key] for dataKey, row in self._data.items()}

if __name__ == "__main__":
    table = Table(
        ["Score"],
        ["Player 1", "Player 2", "Player 3", "Player 4"],
    )
    table["Player 1"]["Score"] = 5
    table["Player 2"]["Score"] = 5
    table["Player 3"]["Score"] = 5
    table["Player 4"]["Score"] = 5
    print(table.aggregate_as_list("Score"))
    print(table.aggregate_as_dict("Score"))
    print(table)


