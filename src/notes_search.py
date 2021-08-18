#!/usr/bin/python3
# -*- coding: utf-8 -*-
from unicodedata import normalize

from Alfred3 import Items as Items
from Alfred3 import Tools as Tools
from MyNotes import Search

Tools.logPyVersion()

md_search = Search()

query = normalize('NFC', Tools.getArgv(1))

search_terms, search_type = md_search.get_search_config(query)

wf = Items()

if len(search_terms) > 0:
    sorted_file_list = md_search.notes_search(search_terms, search_type)
else:
    sorted_file_list = md_search.getFilesListSorted()
for f in sorted_file_list:
    c_date = Tools.getDateStr(f['ctime'])
    m_date = Tools.getDateStr(f['mtime'])
    file_tags = md_search.getFileTags(f['path'])
    tags = ' '.join(['#' + tag for tag in file_tags]) if file_tags else ' '
    wf.setItem(
        title=f['title'],
        subtitle=f"{tags}",
        type='file',
        arg=f['path']
    )
    wf.addMod(
        key="cmd",
        arg=f"{f['path']}>{query}",
        subtitle="Enter Actions Menu for the Note...",
        icon_path="icons/action.png",
        icon_type="image"
    )
    wf.addItem()

if len(wf.getItems(response_type="dict")['items']) == 0:
    wf.setItem(
        title="Nothing found...",
        subtitle=f'Do you want to create a new note with title "{query}"?',
        arg=query
    )
    wf.addItem()
wf.write()
