# Copyright 2013-2014 The rust-url developers.
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

# Run as: python make_uts46_mapping_table.py IdnaMappingTable.txt > uts46_mapping_table.rs
# You can get the latest idna table from
# http://www.unicode.org/Public/idna/latest/IdnaMappingTable.txt

import collections
import itertools

print('''\
// Copyright 2013-2014 The rust-url developers.
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. This file may not be copied, modified, or distributed
// except according to those terms.

// Generated by make_idna_table.py

static TABLE: &'static [Range] = &[
''')

txt = open("IdnaMappingTable.txt")

def escape_char(c):
    return "\\u{%x}" % ord(c[0])

def char(s):
    return unichr(int(s, 16))

strtab = collections.OrderedDict()
strtab_offset = 0

def strtab_slice(s):
    global strtab, strtab_offset

    if s in strtab:
        return strtab[s]
    else:
        utf8_len = len(s.encode('utf8'))
        c = (strtab_offset, utf8_len)
        strtab[s] = c
        strtab_offset += utf8_len
        return c

def rust_slice(s):
    return "(StringTableSlice { byte_start: %d, byte_len: %d })" % s

for line in txt:
    # remove comments
    line, _, _ = line.partition('#')
    # skip empty lines
    if len(line.strip()) == 0:
        continue
    fields = line.split(';')
    if fields[0].strip() == 'D800..DFFF':
        continue  # Surrogates don't occur in Rust strings.
    first, _, last = fields[0].strip().partition('..')
    if not last:
        last = first
    mapping = fields[1].strip().replace('_', ' ').title().replace(' ', '')
    if len(fields) > 2:
        if fields[2].strip():
            unicode_str = u''.join(char(c) for c in fields[2].strip().split(' '))
            mapping += rust_slice(strtab_slice(unicode_str))
        elif mapping == "Deviation":
            mapping += rust_slice(strtab_slice(''))
    print("    Range { from: '%s', to: '%s', mapping: %s }," % (escape_char(char(first)),
                                                                escape_char(char(last)),
                                                                mapping))

print("];\n")

def escape_str(s):
    return [escape_char(c) for c in s]

print("static STRING_TABLE: &'static str = \"%s\";"
      % '\\\n  '.join(itertools.chain(*[escape_str(s) for s in strtab.iterkeys()])))