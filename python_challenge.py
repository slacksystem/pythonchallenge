import urllib.request
from pcutils import geturl
from pregex.core.pre import Pregex
from pregex.core.classes import AnyLetter, AnyWhitespace, AnyButLetter, AnyButFrom
from pregex.core.groups import Capture, Group
from pregex.core.quantifiers import OneOrMore, Optional, Indefinite
from pregex.core.assertions import MatchAtEnd, NotFollowedBy
from pregex.core.operators import Either


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
    comments = commentPre.get_matches(siteStr)
    print(commentPre.get_captures(siteStr)[0])
    blockOfMostlyNonsense = commentPre.get_captures(siteStr)[-1][0]
    print(blockOfMostlyNonsense)
    decipheredStr = "".join(AnyLetter().get_matches(blockOfMostlyNonsense))
    # decipheredStr = "".join(pre.get_captures(siteStr))
    # decipheredStr = siteStr
    # return decipheredStr
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
