#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import MeCab

MECAB = MeCab.Tagger("-Owakati")

JA_SYMBOLS = u'!?！？。☆★♡♥❤♪♬♫✿'
JA_TOKENIZER = nltk.tokenize.RegexpTokenizer(u'[^{0}]*([{0}]+|$)'.format(JA_SYMBOLS))
EN_SYMBOLS = u'☆★♡♥❤♪♬♫✿'
EN_TOKENIZER = nltk.tokenize.RegexpTokenizer(u'[^{0}]*([{0}]+|$)'.format(EN_SYMBOLS))

def sent_tokenize_ja(s):
    return JA_TOKENIZER.tokenize(s)[:-1]

def sent_tokenize_en(s):
    sentences = EN_TOKENIZER.tokenize(s)[:-1]
    sentencess = map(lambda sent: nltk.sent_tokenize(sent.strip()), sentences)
    return [sentence for sentences in sentencess for sentence in sentences]

def sent_tokenize(s, lang=None):
    if lang == 'en':
        return sent_tokenize_en(s)
    elif lang == 'ja':
        return sent_tokenize_ja(s)
    else:
        raise NotImplementedError

def word_tokenize_ja(s):
    string = s.encode("utf-8")
    output = MECAB.parse(string)
    tokens = output.decode('utf8')
    return tokens.strip()

def word_tokenize_en(s):
    return ' '.join(nltk.wordpunct_tokenize(s.strip()))

def word_tokenize(s, lang=None):
    if lang == 'en':
        return word_tokenize_en(s)
    elif lang == 'ja':
        return word_tokenize_ja(s)
    else:
        raise NotImplementedError

def dump(words):
    print '-' * 30
    for word in words:
        print word

if __name__ == '__main__':
    # dump(sent_tokenize_ja(u'白だしを使うから上品な味に仕上がります。夏はこれがなきゃ始まらないくらい大好きな冷やしうどんです。'))
    # dump(sent_tokenize_ja(u'キャベツたっぷり！油揚げに詰めて焼いた簡単＆ヘルシーなメンチカツ風のおかず (^0^*　) 動画アリ♪'))
    # dump(sent_tokenize_ja(u'中に詰める具材はしっかり練り混ぜてください。動画レシピ：http://www.youtube.com/watch?v=kWcPNQYviNY'))
    # dump(sent_tokenize_ja(u'ベジーテがモニター当選したので考えました。キャベツを１個買ったのでキャベツ料理♪ヘルシー素材すぎて彼にはどうかな～と思ったけど食べ応えあったらしく喜んでもらえた☆'))
    # dump(sent_tokenize_ja(u'調味料３つでスピード調理♬生姜とお酢効果でさっぱり＆ふっくら仕上がり❤とことん無駄を省いたずぼら美味しい料理★'))
    # dump(sent_tokenize_ja(u'すき焼き風の豆腐とひき肉でご飯のお供にぴったりです(*◔‿◔)❤'))
    # dump(sent_tokenize_ja(u'シンプルな塩炒めです．シンプルなのにとってもおいしいですよ！お酒にも合う！！！'))
    # dump(sent_tokenize_ja(u'肉じゃがをマッシャーで潰す。(汁気が多い場合は少し汁気を切ったほうがいいです。)'))
    # dump(sent_tokenize_ja(u'耐熱器に入れて、チーズをたっぷり乗せて、トースターでチン♪パセリをパラパラ〜♪'))

    # dump(sent_tokenize_en(u'Tofu, leek and egg are the only ingredients ♪ You can make this in just a few minutes. '))
    # dump(sent_tokenize_en(u'A favorite recipe ♪ The mushroom soaks up the butter soy sauce flavor. '))
    # dump(sent_tokenize_en(u'Sukiyaki-style tofu and ground meat is the perfect match for rice (*◔‿◔)❤'))
    # dump(sent_tokenize_en(u'After trying a sukiyaki-style stew with ground meat and other leftovers I had in the refrigerator, it turned out good! So I\'ve decided to upload this recipe!'))

    dump(word_tokenize_en(u'Sukiyaki-style tofu and ground meat is the perfect match for rice (*◔‿◔)❤'))

