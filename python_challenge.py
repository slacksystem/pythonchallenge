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


def challenge1() -> str:
    return str(2**38)


def challenge2(encodedMessage: str):
    transTable = encodedMessage.maketrans(
        "abcdefghijklmnopqrstuvwxyz", "cdefghijklmnopqrstuvwxyzab"
    )
    result = encodedMessage.translate(transTable)
    pagename = "map".translate(transTable)
    return pagename


def challenge3():
    response = urllib.request.urlopen(geturl(challenge2("")))
    siteBytes = response.read()
    siteStr: str = str(siteBytes.decode("utf8"))
    commentPre: Pregex = "<!--\n" + Capture(OneOrMore(Either(AnyButFrom(">", "-"), NotFollowedBy("-", "->"))), "comment") + "\n-->"  # type: ignore
    blockOfMostlyNonsense = commentPre.get_captures(siteStr)[-1][0]
    decipheredStr = "".join(AnyLetter().get_matches(blockOfMostlyNonsense))
    return decipheredStr


def challenge4() -> str:
    response = urllib.request.urlopen(geturl(challenge3()))
    siteBytes = response.read()
    siteStr: str = str(siteBytes.decode("utf8"))
    commentPre: Pregex = "<!--" + Capture(OneOrMore(Either(AnyButFrom(">", "-"), NotFollowedBy("-", "->"))), "comment") + "-->"  # type: ignore
    blockOfMostlyNonsense = commentPre.get_captures(siteStr)[-1][0]
    cluePre: Pregex = AnyButUppercaseLetter() + AnyUppercaseLetter() * 3 + Capture(AnyLowercaseLetter()) + AnyUppercaseLetter() * 3 + AnyButUppercaseLetter()  # type: ignore
    captures = [x[0] for x in cluePre.get_captures(blockOfMostlyNonsense)]
    decipheredStr = "".join(captures)
    return decipheredStr


if __name__ == "__main__":
    print(geturl(challenge1()))
    print(
        geturl(
            challenge2(
                "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
            )
        )
    )
    print(geturl(challenge3()))
    print(f"{geturl(challenge4())}?nothing=12345")
