"""Export-only adjustments for this paper; no mathematical substitutions."""
from pathlib import Path
import json, re, sys

p=Path(sys.argv[1]);text=p.read_text();repairs=[]
def once(before,after,name):
    global text
    if text.count(before)!=1: raise RuntimeError(name+': expected one occurrence')
    text=text.replace(before,after,1);repairs.append(name)
once('\\hypersetup{','\\providecommand{\\xmpquote}[1]{#1}\n\\hypersetup{','Pandoc keyword wrapper')
m=re.search(r'\\section\{Global twistor sources for analytic Einstein\s+spacetimes\}(\\label\{global-twistor-sources-for-analytic-einstein-spacetimes\})',text)
if not m: raise RuntimeError('Expected body title')
once(m.group(0),m.group(1),'Remove duplicate body title, retain anchor')
text=text.replace('\\subsubsection{','\\RELEASEsubsection{').replace('\\subsection{','\\section{').replace('\\RELEASEsubsection{','\\subsection{')
repairs.append('Promote source heading levels')
once('\\section{Abstract}\\label{abstract}','\\pandocabstractheading\\label{abstract}','Centered Abstract heading')
for a in ['\\href{https://doi.org/10.4007/annals.2003.157.575}{doi:10.4007/annals.2003.157.575}', '\\href{https://arxiv.org/abs/2104.07031v2}{arXiv:2104.07031v2}']:
    prefix,label=a.rsplit('}{',1)
    once(a,prefix+'}{\\nolinkurl{'+label[:-1]+'}}','Allow bibliography link wrapping')
p.write_text(text)
p.with_name('release-tex-repairs.json').write_text(json.dumps({'repairs':repairs},indent=2)+'\n')
