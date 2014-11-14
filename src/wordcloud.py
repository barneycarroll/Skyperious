# -*- coding: utf-8 -*-
"""
A very simple word cloud analyzer, provides only word size calculation and no
layout.

------------------------------------------------------------------------------
This file is part of Skyperious - a Skype database viewer and merger.
Released under the MIT License.

@author      Erki Suurjaak
@created     17.01.2012
@modified    10.04.2014
------------------------------------------------------------------------------
"""
import collections
import re

import conf

"""Default language for common words."""
DEFAULT_LANGUAGE = "en"

"""Maximum amount of words to include."""
WORDS_MAX = 100

"""Minimum count for words to be included."""
COUNT_MIN = 2

"""Minimum length for words to be included."""
LENGTH_MIN = 2

"""Minimum font size for words (for wx.html.HtmlWindow)."""
FONTSIZE_MIN = 0

"""Maximum font size for words (for wx.html.HtmlWindow)."""
FONTSIZE_MAX = 7

"""A map of languages and common words."""
COMMON_WORDS = {
    "en": u"""
        i me my myself we us our ours ourselves you your yours yourself
        yourselves he him his himself she her hers herself it its itself they
        them their theirs themselves what which who whom whose this that these
        those am is are was were be been being have has had having do does did
        doing will would should can could ought i'm you're he's she's it's
        we're they're i've  you've we've they've i'd you'd he'd she'd we'd
        they'd i'll you'll he'll she'll we'll they'll isn't aren't wasn't
        weren't hasn't  haven't hadn't doesn't don't didn't won't wouldn't
        werent hasnt havent hadnt doesnt dont didnt wont wouldnt
        shan't shouldn't can't cannot couldn't mustn't let's that's who's
        shant shouldnt cant cannot couldnt mustnt lets thats whos
        what's here's there's when's where's why's how's a an the and but if or
        because as until while of at by for with about against between into
        through during before after above below to from up upon down in out on
        off over under again further then once here there when where why how
        all any both each few more most other some such no nor not only own
        same so than too very say says said shall just ok now much like also
        well really probably still hey hi around quite one two yeah many see
        get go
        """,
    "et": u"""
        a aga aha ahaa ainult alates all alla alles alt asemel ciao edasi ees 
        eest ega ehk ehkki ei eile elik enam end endale ennast enne ennem 
        ennist ent eriti et ette hea hei heip hetkel hiljuti hm hmm hmmm hmmmm 
        hoi homme hoopis hästi iga ikka ilma ilmselt ise isegi ja jah jahh 
        jaoks jap japp jees jep jepp jmt jne ju juba just juurde juures jälle 
        järel järele järelt järgi ka kaasa kas keegi kes keskel keski 
        kindlasti kinni kle kohe kohta kokku koos kuhu kuhugi kui kuid kuidas 
        kuigi kuna kunagi kuni kus kuskil kuskile kusagil kusagile kust kuule 
        kõik kõrval kõrvale kõrvalt kätte küll ligi lihtsalt liiga läbi 
        lähemal lähemale lähemalt ma maha me meid meie meil meile mh mhh mhmh 
        mida midagi miks millal mina mind mingeid mingi mingit minna minu minus
        mis miski mitte mitu mm mmm mu muidu muidugi mujal mujale mujalt mul 
        mulle mus naa nad nagu nagunii natuke need neid neil neis nemad nii 
        niisama ning no noh nojah näiteks nüüd og ogi ok oki okei ole oled 
        oleks olema oleme olen olevat olgu olid olime olin olla oli olid oligi 
        olin  on ongi oma omad omal omale omas ometi paiku pakaa palju peab 
        peaks peal peale pealt pigem pihta pole pool poole praegu põhjal pärast
        päris rohkem sa saa saab saaks samas sageli sau sauh seal sealt see 
        sees seda sellal selle sellega selleks sellel sellelt selles sellest 
        selline sellist sest siin siis siiski siit sina sind sinna sinu sinul 
        sisse su suht suhtes sul sulle sult sääl säält ta taga tagant tagasi 
        talle te tea tead teda tegelikult tegelt teha teie teid teil tema 
        temale tere terv tervist tol tollal too tsau tshau tšau tuleb tulla 
        tundub täna täpselt yo umbes vahel vaid vaja vara varem vast vastu vbl 
        veel veidi vist või võib võib-olla võibolla võid võiks väga vähe vähem 
        vähemalt välja väljas väljast õite äkki ära üks üldse üle üles ümber 
        ümbert üsna yle yo and in is of the to you
    """,
    "ru": u"""
        Й Ч ЧП ОЕ ЮФП ПО ОБ С У УП ЛБЛ Б ФП ЧУЕ ПОБ ФБЛ ЕЗП ОП ДБ ФЩ Л Х ЦЕ 
        ЧЩ ЪБ ВЩ РП ФПМШЛП ЕЕ НОЕ ВЩМП ЧПФ ПФ НЕОС ЕЭЕ ОЕФ П ЙЪ ЕНХ ФЕРЕТШ 
        ЛПЗДБ ДБЦЕ ОХ ЧДТХЗ МЙ ЕУМЙ ХЦЕ ЙМЙ ОЙ ВЩФШ ВЩМ ОЕЗП ДП ЧБУ ОЙВХДШ 
        ПРСФШ ХЦ ЧБН УЛБЪБМ ЧЕДШ ФБН РПФПН УЕВС ОЙЮЕЗП ЕК НПЦЕФ ПОЙ ФХФ ЗДЕ 
        ЕУФШ ОБДП ОЕК ДМС НЩ ФЕВС ЙИ ЮЕН ВЩМБ УБН ЮФПВ ВЕЪ ВХДФП ЮЕМПЧЕЛ 
        ЮЕЗП ТБЪ ФПЦЕ УЕВЕ РПД ЦЙЪОШ ВХДЕФ Ц ФПЗДБ ЛФП ЬФПФ ЗПЧПТЙМ ФПЗП 
        РПФПНХ ЬФПЗП ЛБЛПК УПЧУЕН ОЙН ЪДЕУШ ЬФПН ПДЙО РПЮФЙ НПК ФЕН ЮФПВЩ 
        ОЕЕ ЛБЦЕФУС УЕКЮБУ ВЩМЙ ЛХДБ ЪБЮЕН УЛБЪБФШ ЧУЕИ ОЙЛПЗДБ УЕЗПДОС 
        НПЦОП РТЙ ОБЛПОЕГ ДЧБ ПВ ДТХЗПК ИПФШ РПУМЕ ОБД ВПМШЫЕ ФПФ ЮЕТЕЪ ЬФЙ 
        ОБУ РТП ЧУЕЗП ОЙИ ЛБЛБС НОПЗП ТБЪЧЕ УЛБЪБМБ ФТЙ ЬФХ НПС ЧРТПЮЕН 
        ИПТПЫП УЧПА ЬФПК РЕТЕД ЙОПЗДБ МХЮЫЕ ЮХФШ ФПН ОЕМШЪС ФБЛПК ЙН ВПМЕЕ 
        ЧУЕЗДБ ЛПОЕЮОП ЧУА НЕЦДХ без безо бишь благодаря близ более больше 
        будем будет будете будешь будто буду будут бы бывало был была были 
        было быть вам вами вас ваш ваша ваше вашего вашей вашем вашему вашею 
        ваши вашим вашими ваших вашу вблизи вверх вверху ввиду вдоволь вдоль 
        вдруг ведь вероятно весь весьма включая влево вместо вне вниз внизу 
        внутри внутрь во вокруг вон вообще вообщем вопреки вот вполне вправо 
        впрочем вроде все всегда всего всей всем всеми всему всех всею вслед 
        вследствие всю всюду вся всё всём вы где да дабы давай даже дескать 
        для до докуда другая другие другим другими других другого другое 
        другой другом другому другою другую его едва ее ей емнип ему если 
        есть еще ещё её же за запросто затем зато зачем здесь из извне 
        изрядно или иль им именно иметь ими имхо иначе исключая итак их ихая 
        ихие ихий ихим ихими ихих ихнего ихнее ихней ихнем ихнему ихнею 
        ихние ихний ихним ихними ихних ихнюю ихняя как какая каких какую кем 
        ко когда коли конечно которая которого которое которой котором 
        которому которою которую которые который которым которыми которых 
        кроме кстати кто куда ли либо лишь ль между менее меньше меня мне 
        мной мною мну мог могла могли могло могу могут мое моего моей моем 
        моему моею можем может можете можешь можно мои моим моими моих мой 
        мол мою моя моё моём мы на навсегда навстречу над надо наконец нам 
        нами наподобие наружу нас насколько насчет насчёт начиная наш наша 
        наше нашего нашей нашем нашему нашею наши нашим нашими наших нашу не 
        негде него незачем ней некем некогда некому некоторый некто некуда 
        неоткуда несколько несмотря несомненно нет неужели нечего нечем 
        нечто неё ни нибудь нигде никак никем никогда никого никому никто 
        никуда ним ними ниоткуда нисколько них ничего ничем ничему ничто 
        ничуть но ну об оба обе обеим обеими обеих обо обоим обоих однако 
        около он она они оно опять от откуда отнюдь ото отовсюду отсюда 
        оттого оттуда отчего очень перед по под подо подобно пока после 
        потому походу почему почти поэтому при привет притом причем причём 
        про прочая прочего прочее прочей прочем прочему прочею прочие прочий 
        прочим прочими прочих прочую пускай пусть разве сам сама самая сами 
        самим самими самих само самого самое самой самом самому саму самые 
        самый сверх сколько слева следовательно слишком словно снова со 
        собой собою справа спустя суть та так такая также такие таким такими 
        таких такого такое такой таком такому такою такую там твое твоего 
        твоей твоем твоему твоею твои твоим твоих твой твою твоя твоё твоём 
        те тебе тебя тем теми тех то тобой тобою тогда того тоже тоими той 
        только том тому тот тотчас тою ту тут ты уж уже хоть хотя чего чей 
        чем через что чтобы чье чьего чьей чьем чьему чьею чьи чьим чьими 
        чьих чью чья чьё чьём чём эта эти этим этими этих это этого этой 
        этом этому этот этою эту в-пятых в-третьих в-четвертых в-четвёртых 
        во-вторых во-первых едва-едва еле-еле из-за из-под как-никак 
        по-моему по-над по-под то-есть точь-в-точь чуть-чуть т.д. т.е. т.к. 
        т.н. т.п. aga budem budet budu byl byla byli bylo byt chto da davai 
        davaj dykk ee emu esli est est' eta eto gde ili kak ne net nu ok on 
        ona oni my mne menya mozhet mozhno privet ya tak tam togda tolko 
        tol'ko tebe uzhe ty vy vam 
    """
}



def get_cloud(text, additions=None):
    """
    Returns the word cloud for the specified text. Language of the text is
    autodetected from among English (default), Estonian and Russian, and
    pre-defined common words (like 'at') are removed.

    @param   text       text to analyze
    @param   additions  a pre-parsed list of additional words to add
    @return             in descending order of relevance, as
                        [('word', count, font size), ]
    """
    result = []
    words = re.findall("\w{%s,}" % LENGTH_MIN, text.lower(), re.UNICODE) \
            + (additions or [])
    commons = set(get_common_words(words))
    cloud = collections.defaultdict(lambda: 0)
    # Add and count all non-common and not wholly numeric words
    for i in filter(lambda x: x not in commons and re.search("\D", x), words):
        cloud[i] += 1
    # Drop rare words and limit the number of words
    count_last = COUNT_MIN
    if len(cloud) > WORDS_MAX:
        count_last = max(count_last, sorted(cloud.values())[WORDS_MAX - 1])
    cloud = dict((i, cloud[i]) for i in cloud if cloud[i] >= count_last)
    count_min = min(cloud.values()) if cloud else -1
    count_max = max(cloud.values()) if cloud else -1
    for word, count in cloud.items():
        size = get_word_size(count, count_min, count_max)
        result.append((word, count, size))
    result.sort(key=lambda x: x[1], reverse=True) # Sort by count
    result = result[:WORDS_MAX]
    return result


def get_word_size(count, count_min, count_max):
    """
    Returns the font size for a word.

    @param   count      count of the word in the text
    @param   count_min  minimum word count in the text
    @param   count_max  maximum word count in the text
    @return             FONTSIZE_MIN..FONTSIZE_MAX
    """
    result = FONTSIZE_MAX
    if count_min != count_max:
        lo, hi = FONTSIZE_MIN, FONTSIZE_MAX
        ratio = count / float(count_max - count_min)
        result = int(lo + (hi - lo) * min(1, ratio ** 0.2))
    return result


def get_common_words(words):
    """
    Returns the defined common words for the specified words, in the language
    that matches best the given words.

    @param   words  a list of words
    @return         a list of common words
    """
    best_matches = []
    max_matches = 0

    for language, text in COMMON_WORDS.items():
        commons = set(re.findall("\w+", text, re.UNICODE))
        match_count = len(commons.intersection(words))

        if match_count > max_matches:
            best_matches = commons
            max_matches = match_count

    return best_matches
