from typing import Iterable, Any

from pdfminer.high_level import extract_pages


def show_ltitem_hierarchy(o: Any, elementsList:list, depth=0):
    """Show location and text of LTItem and all its descendants"""

    elementsList.append([f'{get_indented_name(o, depth):<30.30s}', f'{get_optional_fontinfo(o):<20.20s}', f'{get_optional_text(o)}'])     

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, elementsList, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of class"""
    if hasattr(o, '__class__'):
        return f'{o.__class__.__name__} class name'
    return 'No Class Name Data'


def get_optional_fontinfo(o: Any) -> str:
    """Font info of LTChar if available, otherwise empty string"""
    if hasattr(o, 'fontname') and hasattr(o, 'size'):
        return f'{o.fontname}, {round(o.size)}pt'
    return 'No font Data'


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return 'No Text Data'


path = "impossible.pdf"
pages = extract_pages(path, page_numbers=[313])
impossibleElemList = []
show_ltitem_hierarchy(pages, impossibleElemList)
print(impossibleElemList)