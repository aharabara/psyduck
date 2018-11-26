import curses

import npyscreen


class MessagesHistory(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class Contacts(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class MessageBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit

class QLTheme(npyscreen.ThemeManager):
    _colors_to_define = (
        ('WHITE_BLACK', curses.COLOR_WHITE, curses.COLOR_BLACK),
        ('BLACK_WHITE', curses.COLOR_BLACK, curses.COLOR_WHITE),
        ('BLUE_BLACK', curses.COLOR_BLUE,curses.COLOR_BLACK),
        ('CYAN_BLACK', curses.COLOR_CYAN, curses.COLOR_BLACK),
        ('GREEN_BLACK', curses.COLOR_GREEN, curses.COLOR_BLACK),
        ('MAGENTA_BLACK', curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        ('RED_BLACK', curses.COLOR_RED, curses.COLOR_BLACK),
        ('YELLOW_BLACK', curses.COLOR_YELLOW, curses.COLOR_BLACK),
        ('BLACK_RED', curses.COLOR_BLACK, curses.COLOR_RED),
        ('BLACK_GREEN', curses.COLOR_BLACK, curses.COLOR_GREEN),
        ('BLACK_YELLOW', curses.COLOR_BLACK, curses.COLOR_YELLOW),
        ('BLUE_WHITE', curses.COLOR_BLUE, curses.COLOR_WHITE),
        ('GREEN_WHITE', curses.COLOR_GREEN, curses.COLOR_WHITE),
        ('YELLOW_WHITE', curses.COLOR_YELLOW, curses.COLOR_WHITE),
        ('RED_WHITE', curses.COLOR_RED, curses.COLOR_WHITE),
    )

    default_colors = {
        'DEFAULT': 'WHITE_BLACK',
        'FORMDEFAULT': 'WHITE_BLACK',
        'NO_EDIT': 'BLACK_WHITE',
        'STANDOUT': 'BLUE_WHITE',
        'LABEL': 'YELLOW_BLACK',
        'LABELBOLD': 'YELLOW_BLACK',
        'CONTROL': 'WHITE_BLACK',
        'IMPORTANT': 'GREEN_WHITE',
        'SAFE': 'GREEN_WHITE',
        'WARNING': 'YELLOW_WHITE',
        'DANGER': 'RED_WHITE',
        'CRITICAL': 'RED_WHITE',
        'GOOD': 'GREEN_WHITE',
        'GOODHL': 'GREEN_WHITE',
        'VERYGOOD': 'BLACK_WHITE',
        'CAUTION': 'YELLOW_WHITE',
        'CAUTIONHL': 'BLACK_WHITE',
        }