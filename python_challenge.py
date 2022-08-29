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


if __name__ == "__main__":
    print(geturl(challenge1()))
    print(
        geturl(
            challenge2(
                "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
            )
        )
    )
