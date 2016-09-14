#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###
# Maps integer keys to a set of arbitrary values.
class Multidict:
    def __init__(self, pairs=[]):
        self.d = dict()
        for k,v in pairs:
            self.put(k,v)
    def put(self, k, v):
        if k in self.d: self.d[k].append(v)
        else: self.d[k]=[v]
    def get(self, k):
        try:
            return self.d[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        assert k>0
        subseq = ''
        for i in xrange(k): subseq += seq.next()
        rh = RollingHash(subseq)
        pos = 0
        while True:
            yield (rh.current_hash(),(pos, subseq))
            pre = subseq[0]
            subseq = subseq[1:]+seq.next()
            rh.slide(pre, subseq[-1:])
            pos += 1
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    assert m >= k
    try:
        pos = 0
        while True:
            subseq = ''
            for i in xrange(k): subseq += seq.next()
            rh = RollingHash(subseq)
            yield (rh.current_hash(),(pos, subseq))
            for i in xrange(m-k):
                seq.next()
            pos += m
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    print "Building table from sequence A..."
    seqtable = Multidict(intervalSubsequenceHashes(a, k, m))
    print "...done building table."
    for hb, (posb, subseqb) in subsequenceHashes(b, k):
        for posa, subseqa in seqtable.get(hb):
            if subseqa == subseqb: yield (posa, posb)
    return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)
    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
