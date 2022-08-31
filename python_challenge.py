import re
import urllib.request
from typing import List

from pregex.core.assertions import NotFollowedBy
from pregex.core.classes import (
    AnyButFrom,
    AnyButUppercaseLetter,
    AnyLetter,
    AnyLowercaseLetter,
    AnyUppercaseLetter,
)
from pregex.core.groups import Backreference, Capture
from pregex.core.operators import Either
from pregex.core.pre import Pregex
from pregex.core.quantifiers import OneOrMore

from pcutils import geturl

prefix = "http://www.pythonchallenge.com/pc/def/"


def challenge1() -> str:
    return geturl(str(2**38))


def challenge2():
    encodedMessage = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    transTable = encodedMessage.maketrans(
        "abcdefghijklmnopqrstuvwxyz", "cdefghijklmnopqrstuvwxyzab"
    )
    result = encodedMessage.translate(transTable)
    pagename = "map".translate(transTable)
    return geturl(pagename)


def challenge3():
    response = urllib.request.urlopen(challenge2())
    siteBytes = response.read()
    siteStr: str = str(siteBytes.decode("utf8"))
    commentPre: Pregex = "<!--\n" + Capture(OneOrMore(Either(AnyButFrom(">", "-"), NotFollowedBy("-", "->"))), "comment") + "\n-->"  # type: ignore
    blockOfMostlyNonsense = commentPre.get_captures(siteStr)[-1][0]
    decipheredStr = "".join(AnyLetter().get_matches(blockOfMostlyNonsense))
    return geturl(decipheredStr)


def challenge4() -> str:
    response = urllib.request.urlopen(challenge3())
    siteBytes = response.read()
    siteStr: str = str(siteBytes.decode("utf8"))
    commentPre: Pregex = "<!--" + Capture(OneOrMore(Either(AnyButFrom(">", "-"), NotFollowedBy("-", "->"))), "comment") + "-->"  # type: ignore
    blockOfMostlyNonsense = commentPre.get_captures(siteStr)[-1][0]
    cluePre: Pregex = AnyButUppercaseLetter() + AnyUppercaseLetter() * 3 + Capture(AnyLowercaseLetter()) + AnyUppercaseLetter() * 3 + AnyButUppercaseLetter()  # type: ignore
    captures = [x[0] for x in cluePre.get_captures(blockOfMostlyNonsense)]
    decipheredStr = "".join(captures)
    return f"{prefix}{decipheredStr}.php?nothing=12345"


def getNothing(nothing: str):
    url = f"{prefix}linkedlist.php?nothing={nothing}"
    response = urllib.request.urlopen(url)
    source: str = response.read().decode("utf8")
    regex: re.Pattern = re.compile(r"\d+")
    resMatch: re.Match | None = regex.search(source)
    if resMatch is None:
        if re.search("Divide by two", source):
            getNothing(str(int(nothing) / 2))
        elif re.search(r"\.html", source):
            return f"{prefix}{source}"
    else:
        newUrl = f"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={resMatch.group()}"
        return getNothing(resMatch.group())


def challenge5():
    firstUrl = challenge4()
    return getNothing(firstUrl)


if __name__ == "__main__":
    print(challenge1())
    print(challenge2())
    print(challenge3())
    print(challenge4())
    print(challenge5())
