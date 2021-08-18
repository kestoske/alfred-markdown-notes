#!/usr/bin/python3
# -*- coding: utf-8 -*-

import MyNotes
from Alfred3 import Items, Tools

SUFFIX = " (DEFAULT)"

query = Tools.getArgv(1)

my_notes = MyNotes.Search()
all_files = my_notes.getFilesListSorted()
template_files = sorted(all_files, key=lambda x: x['path'] != my_notes.getDefaultTemplate())

wf = Items()
for md_file in template_files:
    if my_notes.isNoteTagged(md_file['path'], my_notes.getTemplateTag()) \
            and query.lower() in md_file['filename'].lower():
        suffix = str()
        if md_file['path'] == my_notes.getDefaultTemplate():
            suffix = SUFFIX
        wf.setItem(
            title=md_file['filename'] + suffix,
            subtitle=f"Create new file based on \"{md_file['filename']}\"",
            arg=Tools.strJoin(md_file['path']),
            type='file'
        )
        wf.addItem()
wf.write()
