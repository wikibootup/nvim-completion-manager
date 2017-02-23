# -*- coding: utf-8 -*-


class Matcher(object):

    def __init__(self,nvim,chcmp,*args):
        self._chcmp = chcmp

    def process(self,name,ctx,startcol,matches):

        # fix for chinese characters
        # `你好 abcd|` 
        # has  col('.')==11 on vim
        # the evaluated startcol is: startcol[8] typed[你好 abcd]
        # but in python, "你好 abcd"[8] is not a valid index
        begin = -(ctx['col'] - startcol)
        base = ''
        if begin:
            base = ctx['typed'][begin:]


        tmp = []
        for item in matches:
            score = self._match(base,item)
            if not score:
                continue
            tmp.append((item,score))

        # sort by score, the smaller the better
        tmp.sort(key=lambda e: e[1])

        return [e[0] for e in tmp]

    # return the score, the smaller the better
    def _match(self, base, item):

        word = item['word']
        if len(base)>len(word):
            return None
        p = -1
        pend = len(word)
        begin = pend
        for c in base:
            p += 1
            if p>=pend:
                return None
            while not self._chcmp(c,word[p]):
                p += 1
                if p>=pend:
                    return None
            if p < begin:
                begin = p

        # return the score, the smaller the better
        # prefer shorter match
        # prefer fronter match
        return (p-begin, begin, word.swapcase())

