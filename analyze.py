# -*- coding: utf-8 -*-
# @Author: mypolopony
# @Date:   2019-03-08 21:29:52
# @Last Modified by:   mypolopony
# @Last Modified time: 2019-03-08 22:38:52

import nltk
import sys
import re

def load_from_gutenberg():
    '''
    Example NLTK method discouraged as per above (DISCOURAGED)
    '''
    sents = nltk.corpus.gutenberg.sents('bible-kjv.txt')

    # For each, identify if it begins with a chapter / verse, which we'll
    # truncate. This would have worked but the problem proved to be more
    # widespread / diverse
    for sent in sents:
        try:
            _ = int(sent[0])
            sent = sent[3:]
        except:
            pass

        # After having 'pure' sentences, we print them to find the problem
        for fragment in sent:
            try:
                _ = int(fragment)
                print(sent)
                continue
            except:
                pass

def generate_sentences(fn_in=None):
    '''
    This is actually just a documentary function. The nltk package does have
    high level acccess to some texts but it's parsing is not entirely reliable.

    The example I found, i.e. to understand why, you can look at the official
    Gutenberg King James Bible and after the following procedure, which should
    isolate verses ('sentences'), it does not quite work as expected.

    It is a bug in the sentence identifier. Some phrases in this particular 
    text are usually structured like this

        12:23 AND THEN SOMETHING HAPPENED.

        12:24 AND THEN SOMETHING ELSE HAPPENED.

    But occasionally, it looks like

        12:23 AND THEN SOMETHING HAPPENED:

        12:24 AND THEN SOMETHING ELSE HAPPENED

    In which case neither the colon nor the newline is respected as a terminator
    and as such you get an improper run-on combining the two verses.

    Furthermore, if you download the text from Gutenberg [link here], can see, 
    for example the following

        24:35 And the LORD hath blessed my master greatly; and he is become
        great: and he hath given him flocks, and herds, and silver, and gold,
        and menservants, and maidservants, and camels, and asses.

        24:36 And Sarah my master's wife bare a son to my master when she was
        old: and unto him hath he given all that he hath.

    Whereas, right next door, you'll see

        24:37 And my master made me swear, saying, Thou shalt not take a wife
        to my son of the daughters of the Canaanites, in whose land I dwell:
        24:38 But thou shalt go unto my father's house, and to my kindred, and
        take a wife unto my son.

    And then, again, next door, you can find

        24:40 And he said unto me, The LORD, before whom I walk, will send his
        angel with thee, and prosper thy way; and thou shalt take a wife for
        my son of my kindred, and of my father's house: 24:41 Then shalt thou
        be clear from this my oath, when thou comest to my kindred; and if
        they give not thee one, thou shalt be clear from my oath.

    This became an issue only coincidentally, with the Biblical case, in which
    one of the desires is to identify numbers WITHIN verses, which makes parsing
    important.

    Approach: So thank you, nltk, for providing high-level access to these
    textx, but essentially it's easier to do some case-specific parsing first, 
    then presenting it to nltk if necessary.
    '''

    # TODO: This should be a generator?

    # Load the sentences
    if not fn_in:
        # Just for demonstration purposes
        sents = load_from_gutenberg('bible-kjv.txt')
        return None

    # Text file
    else:
        with open(fn_in, 'r') as fulltext:
            # Default read of all data
            data = fulltext.read()

            # --- Cleansing ---
            # This is source-specific and can be more elegantly enumerated 
            # elsewhere

            # - King James Bible -
            # From: URL URL URL
            pattern = re.compile(r'[0-9]+:[0-9]+')  # Split pattern (CHP:VRS)
            if fn_in == 'sources/kjv.txt':
                # This replace is actually because there can be '\n's within
                # the sentence as well as as bookends
                for line in pattern.split(data):
                    yield line.replace('\n', ' ').strip()
    
if __name__ in ('__console__', '__main__'):
    # Check arguments
    if len(sys.argv) == 1:
        print('Please add an argument')
        sys.exit(0)
    else:
        # Filename
        fn_in = sys.argv[1]

    # Test case looks OK
    '''
    In the beginning God created the heaven and the earth.
    And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.
    And God said, Let there be light: and there was light.
    And God saw the light, that it was good: and God divided the light from the darkness.
    And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.
    And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.
    And God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament: and it was so.
    And God called the firmament Heaven. And the evening and the morning were the second day.
    And God said, Let the waters under the heaven be gathered together unto one place, and let the dry land appear: and it was so.
    '''
    sents = generate_sentences(fn_in)
    for _ in range(10):
        print(next(sents))
