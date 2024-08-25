from typing import Callable
from datetime import datetime
from pandas import read_sql
from sqlite3 import connect
from os.path import join
from os import getcwd
from io import BytesIO
from styleframe import ExcelWriter, StyleFrame, Styler
from styleframe.utils import horizontal_alignments, colors


def main():
    as_hyperlink: Callable[[str], str] = lambda url: f'=HYPERLINK("{url}","{url}")'
    # valid_iso_format = lambda date
    as_excel_date: Callable[[str], int | str] = \
        lambda date: (datetime.fromisoformat(date) - datetime(1899, 12, 30)).days if '-' in date else date
    default_font = '游ゴシック'

    connector = connect(join(getcwd(), 'save.sqlite'))
    cursor = connector.cursor()
    table_names = cursor.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()
    excel_file: BytesIO = BytesIO()
    main_styler = Styler(horizontal_alignment=horizontal_alignments.left, date_format='YYYY-MM-DD',
                         font_color=colors.black, underline=None, font=default_font)
    header_styler = Styler(number_format='YYYY年MM月DD日', date_format='YYYY年MM月DD日')

    with ExcelWriter(path=excel_file, mode='w') as writer:
        for table_name in table_names:
            print(*table_name, flush=True)
            dataframe = read_sql(f'SELECT * FROM "{table_name.__getitem__(0)}"', connector, index_col='index')
            dataframe.reset_index(inplace=True)
            dataframe.rename(columns={'index': 'URL'}, inplace=True)
            dataframe['URL'] = dataframe['URL'].map(as_hyperlink)
            dataframe.columns = dataframe.columns.map(as_excel_date)
            styleframe = StyleFrame(dataframe, styler_obj=Styler(font=default_font))
            styleframe.set_column_width(columns=dataframe.columns[2:], width=20)
            styleframe.set_column_width(columns='URL', width=37)
            styleframe.set_column_width(columns='タイトル', width=70)
            styleframe.apply_column_style(cols_to_style=dataframe.columns[1:], styler_obj=main_styler)
            styleframe.apply_column_style(cols_to_style='URL',
                                          styler_obj=Styler(horizontal_alignment=horizontal_alignments.left))
            styleframe.apply_headers_style(styler_obj=header_styler)
            styleframe.to_excel(excel_writer=writer, sheet_name=table_name.__getitem__(0),
                                columns_and_rows_to_freeze='C2')

    with open(file=join(getcwd(), 'export.xlsx'), mode='wb') as f:
        f.write(excel_file.getvalue())


if __name__ == '__main__':
    main()
