vitae
=====

A python module for building curriculum vitae and other documents from
a bibtex file.

I hate formatting citations. It's tedious, and error-prone. Further, when I build my CV, I tend to muck it up and leave something out, mis-sort it, duplicate it accidentally, etc. So, I need a tool to do a better job. 

The first function here, `makemycv`, will take a few arguments and put sorted `\bibentry` commands into `.tex` files with names corresponding to bibtex entry types. In doing so, you can then simply use an `\input` command to embed all of these citations right in your document in an enumerated environment. 

Right now, it only works for a `bib` file containing only papers of the cv-writer. I'll fix that eventually. 

Eventually I'll put this on pypi, but you can pip install it right now from github. 

If you try this, please understand:
a. No warrantee. This is still a work in progress. 
b. Please provide your feedback.
c. Please help! I can use help with additional portions. 
