"""
Python Console Library
Copyright (C) 2022  鱼翔浅底,吴宇航
Distributed under GPL 3.0 License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Distributed under GPL license
See copy at https://opensource.org/licenses/GPL-3.0

感谢吴宇航原创的代码着色功能！！！ 原作链接：
‘https://code.xueersi.com/home/project/detail?lang=code&pid=39312324&version=offline&form=python&langType=python’
CodeRender控件90%的代码都来自此作品！！！

以后将会补充一些常用控件，例如选择框，进度条。
尽可能保证跨平台。
"""

__auther__ = "鱼翔浅底"
__website__ = None

import datetime
import enum
import keyword
import platform
import sys
from typing import Any, Iterable, Optional

NUMBER, BUILTIN, KEYWORD, STRING, OTHER = "NUMBER", "BUILTIN", "KEYWORD", "STRING", "OTHER"  # 用于Python词法分析的常量

builtins_list = dir(__builtins__)  # 内置函数
keywords = keyword.kwlist  # 关键字


class Platform(enum.Enum):
    """
    枚举，表示当前平台
    """
    Windows = 0
    Other = 1


platform = Platform.Windows if platform.platform().lower().startswith("windows") else Platform.Other  # 当前平台

# 常用的键码对照表
ConsoleKeys: dict = {
    'Tab': 9,
    'Enter': 10 if platform == Platform.Other else 13,
    'A': 65,
    'B': 66,
    'C': 67,
    'D': 68,
    'E': 69,
    'F': 70,
    'G': 71,
    'H': 72,
    'I': 73,
    'J': 74,
    'K': 75,
    'L': 76,
    'M': 77,
    'N': 78,
    'O': 79,
    'P': 80,
    'Q': 81,
    'R': 82,
    'S': 83,
    'T': 84,
    'U': 85,
    'V': 86,
    'W': 87,
    'X': 88,
    'Y': 89,
    'Z': 90,
    '[': 91,
    '\\': 92,
    ']': 93,
    '^': 94,
    '_': 95,
    '`': 96,
    'a': 97,
    'b': 98,
    'c': 99,
    'd': 100,
    'e': 101,
    'f': 102,
    'g': 103,
    'h': 104,
    'i': 105,
    'j': 106,
    'k': 107,
    'l': 108,
    'm': 109,
    'n': 110,
    'o': 111,
    'p': 112,
    'q': 113,
    'r': 114,
    's': 115,
    't': 116,
    'u': 117,
    'v': 118,
    'w': 119,
    'x': 120,
    'y': 121,
    'z': 122
}


class ConsoleColor(enum.Enum):
    """
    枚举，表示终端颜色
    """
    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Purple = 5
    Cyan = 6
    White = 7
    Default = 8


class ConsoleKeyInfo(object):
    """
    键盘事件类
    """

    def __init__(self, _key_down: int, _datetime: datetime.datetime) -> None:
        """
        初始化键盘事件，开发者不应当使用
        :param _key_down: 按下的键码
        :param _datetime: 按键时间
        """
        self.__key_down = _key_down
        self.__key_down_time = _datetime

    def get_key(self) -> int:
        """
        获取此键盘事件的键码
        :return: 此键盘事件的键码
        """
        return self.__key_down

    def get_time(self) -> datetime.datetime:
        """
        获取此键盘事件发生的时间
        :return: 此键盘事件发生的时间
        """
        return self.__key_down_time

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        else:
            return other.__key_down == self.__key_down


class Console(object):
    class __ColorType(enum.Enum):
        """
        枚举，用于辅助表示ConsoleColor的用途。开发者不应使用
        """
        ForegroundColor = 0
        BackgroundColor = 1

    __fg_color_map = {
        ConsoleColor.Black: "\033[30m",
        ConsoleColor.Red: "\033[31m",
        ConsoleColor.Green: "\033[32m",
        ConsoleColor.Yellow: "\033[33m",
        ConsoleColor.Blue: "\033[34m",
        ConsoleColor.Purple: "\033[35m",
        ConsoleColor.Cyan: "\033[36m",
        ConsoleColor.White: "\033[37m"
    }
    __bg_color_map = {
        ConsoleColor.Black: "\033[40m",
        ConsoleColor.Red: "\033[41m",
        ConsoleColor.Green: "\033[42m",
        ConsoleColor.Yellow: "\033[43m",
        ConsoleColor.Blue: "\033[44m",
        ConsoleColor.Purple: "\033[45m",
        ConsoleColor.Cyan: "\033[46m",
        ConsoleColor.White: "\033[47m"
    }

    def __init__(self, _out=sys.stdout, _in=sys.stdin) -> None:
        """
        初始化控制台，并开放两个输出重定向接口。不建议重定向输出。
        :param _out: 默认输出
        :param _in: 默认输入
        """
        self._out = _out
        self._in = _in

    def write(self, _t: Any) -> None:
        """
        向_out写入内容，并刷新缓冲区
        :param _t: 内容
        :return: 无返回值
        """
        self._out.write(_t)
        self._out.flush()

    def write_line(self, _t: Any) -> None:
        """
        向_out写入内容，并换行，刷新缓冲区
        :param _t: 内容
        :return: 无返回值
        """
        self._out.write(_t + "\n")
        self._out.flush()

    def writes(self, _iter: Iterable, _sep: str = " ", newline: bool = True) -> None:
        """
        拼接可迭代对象，然后写入_out
        :param _iter: 可迭代对象
        :param _sep: 分隔符
        :param newline: 是否换行
        :return: 无返回值
        """
        self._out.write(_sep.join(_iter) + "\n" if newline else "")
        self._out.flush()

    def read(self) -> str:
        """
        从_in中读入一个字节并返回
        :return: 读入的字节
        """
        return self._in.read(1)

    def read_key(self) -> ConsoleKeyInfo:
        """
        从标准输入流读入键盘事件。重定向输入流对此函数无效。
        :return: 键盘事件
        """
        if platform == Platform.Windows:
            import msvcrt
            return ConsoleKeyInfo(ord(msvcrt.getch()), datetime.datetime.now())
        else:
            import termios
            fd = sys.stdin.fileno()  # 获取标准输入的描述符
            old_tty_info = termios.tcgetattr(fd)  # 获取标准输入(终端)的设置
            new_tty_info = old_tty_info[:]  # 配置终端
            new_tty_info[3] &= ~termios.ICANON  # 使用非规范模式
            new_tty_info[3] &= ~termios.ECHO  # 关闭回显

            termios.tcsetattr(fd, termios.TCSANOW, new_tty_info)  # 使设置生效

            res = sys.stdin.read(1)

            termios.tcsetattr(fd, termios.TCSANOW, old_tty_info)  # 恢复设置

            return ConsoleKeyInfo(ord(res), datetime.datetime.now())

    def read_line(self) -> str:
        """
        从_in读入一行
        :return: 读入的内容
        """
        _input = self._in.readline()
        return _input[:-1] if _input.endswith("\n") else _input

    def clear(self) -> None:
        """
        清屏
        :return: 无返回值
        """
        self._out.write("\033c")

    def reset_style(self) -> None:
        """
        重置终端样式
        :return: 无返回值
        """
        self._out.write("\033[0m")

    def set_bg_color(self, color: ConsoleColor) -> None:
        """
        设置背景颜色
        :param color: 颜色
        :return: 无返回值
        """
        if color == ConsoleColor.Default:
            self.reset_style()
        self._out.write(Console.__render(color, Console.__ColorType.BackgroundColor))

    def set_fg_color(self, color: ConsoleColor) -> None:
        """
        设置前景颜色
        :param color:颜色
        :return: 无返回值
        """
        if color == ConsoleColor.Default:
            self.reset_style()
        self._out.write(Console.__render(color, Console.__ColorType.ForegroundColor))

    def __del__(self):
        """
        退出时自动重置终端颜色
        :return: 无返回值
        """
        self.reset_style()

    @classmethod
    def __render(cls, color: ConsoleColor, _type: __ColorType) -> str:
        """
        渲染ANSI转义序列。开发者不应当使用
        :param color: 颜色
        :param _type: 颜色类型/用途
        :return: 渲染后的字符串
        """
        if _type == cls.__ColorType.BackgroundColor:
            return cls.__bg_color_map.get(color, "")
        else:
            return cls.__fg_color_map.get(color, "")


class CodeRender(object):
    """
    感谢吴宇航！！！
    """

    class Token:
        def __init__(self, tp, value):
            self.tp = tp
            self.value = value
            self.color = None

        def __str__(self):
            return f"({self.tp} , {self.value})"

        __repr__ = __str__

    class Scanner:
        def __init__(self, code):
            self.code = code
            self.pos = 0
            self.char = code[0]

        def advance(self):
            self.pos += 1
            if self.pos < len(self.code):
                self.char = self.code[self.pos]
            else:
                self.char = None

        def get_token(self):
            while self.char:
                if self.char.isdigit():
                    res = ""
                    while self.char.isdigit() or self.char == ".":
                        res += self.char
                        self.advance()
                    return CodeRender.Token(NUMBER, res)
                elif self.char == '"' or self.char == "'":
                    quot = self.char
                    self.advance()
                    res = quot
                    while self.char != quot and self.char:
                        res += self.char
                        self.advance()
                    self.advance()
                    res += quot
                    return CodeRender.Token(STRING, res)
                elif self.char.isalpha():
                    res = ""
                    while self.char.isalnum():
                        res += self.char
                        self.advance()
                    if res in builtins_list:
                        return CodeRender.Token(BUILTIN, res)
                    elif res in keywords:
                        return CodeRender.Token(KEYWORD, res)
                    else:
                        return CodeRender.Token(OTHER, res)
                else:
                    char = self.char
                    self.advance()
                    return CodeRender.Token(OTHER, char)

        def tokens(self):
            ret = []
            while self.char:
                ret.append(self.get_token())
            return ret

    colortable = {
        NUMBER: ConsoleColor.Blue,
        STRING: ConsoleColor.Green,
        BUILTIN: ConsoleColor.White,
        KEYWORD: ConsoleColor.Purple,
        OTHER: ConsoleColor.White
    }

    def __init__(self, code: str, _console: Console) -> None:
        self.console = _console
        self.code = code
        self.__tokens = CodeRender.Scanner(self.code).tokens()
        self.__color()

    def __color(self):
        for token in self.__tokens:
            token.color = CodeRender.colortable[token.tp]

    def output(self):
        console.reset_style()
        for token in self.__tokens:
            if token.value:
                self.console.set_fg_color(token.color)
                self.console.write(token.value)
                self.console.reset_style()

    @classmethod
    def Output(cls, code: str, _console: Console) -> None:
        CodeRender(code, _console).output()


class ChoiceScreen(object):
    def __init__(
            self,
            title: str,
            choices: list,
            _console: Console,
            info: Optional,
            _current_option_color=ConsoleColor.Green,
            _enter_key=ConsoleKeys["Enter"]
    ) -> None:
        """

        :param title:
        :param choices:
        :param _console:
        :param info:
        :param _current_option_color:
        :param _enter_key:
        """
        self.title = title
        self.choices = choices
        self._console = _console
        self.info = info
        self.__has_info = False if self.info is None else True
        self._enter_key = _enter_key
        self._current_option_color = _current_option_color
        self.current_choice = 0

    def __output(self) -> None:
        self._console.clear()
        self._console.reset_style()

        self._console.write_line(self.title)
        if self.__has_info:
            for key in self.info.keys():
                value = self.info[key]
                self._console.write_line(f"{key}:{value}\n")

        for choice_index in range(len(self.choices)):
            if self.current_choice == choice_index:
                self._console.set_fg_color(self._current_option_color)
                self._console.write(f">>{self.choices[choice_index]}\n")
                self._console.reset_style()
            else:
                self._console.write(f"  {self.choices[choice_index]}\n")
                self._console.reset_style()

        self._console.write("请选择(w/s选择,Enter确认)>>>")

    def show(self) -> int:
        while True:
            self.__output()
            key = self._console.read_key()
            if key.get_key() == self._enter_key:
                return self.current_choice
            elif key.get_key() == ConsoleKeys["w"]:
                self.current_choice = (
                    len(self.choices) - 1
                    if (self.current_choice - 1) < 0
                    else self.current_choice - 1
                )
            elif key.get_key() == ConsoleKeys["s"]:
                self.current_choice = (
                    0
                    if (self.current_choice + 1) >= len(self.choices)
                    else self.current_choice + 1
                )
            self._console.clear()
            self._console.reset_style()


def pause(_console: Console, tip: str = "按任意键继续>>>") -> None:
    _console.write(tip)
    _console.read_key()


if __name__ == "__main__":
    console = Console()
    index = ChoiceScreen(
        "hello",
        [
            "显示代码",
            "退出"
        ],
        console,
        None
    ).show()
    if index == 0:
        console.clear()
        CodeRender.Output(
            """
import os,sys
print("hello world")
            """,
            console
        )
    else:
        console.write_line("")
        pause(console)
