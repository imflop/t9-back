import dataclasses as dc
import math


BASE = 62
UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48


@dc.dataclass(frozen=True)
class ShorterService:
    def make_short_link(self, link_id: int) -> str:
        return f"https://t9.pm/{self.encode(link_id)}"

    def get_real_link_id(self, encoded_url: str) -> int:
        return self.decode(encoded_url)

    def _true_chr(self, integer: int):
        """
        Turns an integer [integer] into digit in base [BASE]
        as a character representation.
        """
        if integer < 10:
            return chr(integer + DIGIT_OFFSET)
        elif 10 <= integer <= 35:
            return chr(integer + UPPERCASE_OFFSET)
        elif 36 <= integer < 62:
            return chr(integer + LOWERCASE_OFFSET)
        else:
            raise ValueError(f"{integer} is not a valid integer in the range of base {BASE}")

    def encode(self, link_id: int) -> str:
        """
        Turn an integer [integer] into a base [BASE] number
        in string representation
        """
        # we won't step into the while if integer is 0
        # so we just solve for that case here
        if link_id == 0:
            return "0"

        string = ""
        while link_id > 0:
            remainder = link_id % BASE
            string = self._true_chr(remainder) + string
            link_id = int(link_id / BASE)

        return string

    def _true_ord(self, char: str) -> int:
        """
        Turns a digit [char] in character representation
        from the number system with base [BASE] into an integer.
        """

        if char.isdigit():
            return ord(char) - DIGIT_OFFSET
        elif "A" <= char <= "Z":
            return ord(char) - UPPERCASE_OFFSET
        elif "a" <= char <= "z":
            return ord(char) - LOWERCASE_OFFSET
        else:
            raise ValueError(f"{char} is not a valid character")

    def decode(self, encoded_url: str) -> int:
        """
        Turn the base [BASE] number [key] into an integer
        """
        reversed_key = encoded_url[::-1]
        return sum(self._true_ord(char) * int(math.pow(BASE, idx)) for idx, char in enumerate(reversed_key))
