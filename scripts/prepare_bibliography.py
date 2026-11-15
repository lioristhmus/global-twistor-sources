"""Mark the unchanged manual reference entries as standard TeX bibitems."""
from pathlib import Path
import argparse, json, re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('tex', type=Path)
args = parser.parse_args()
text = args.tex.read_text()
heading = r'\section{References}\label{references}'
assert text.count(heading) == 1, 'Expected one manual References heading'
head, bibliography = text.split(heading, 1)
assert '\\bibitem' not in text and '\\begin{thebibliography}' not in text
anchor = re.compile(r'\\protect\\phantomsection\\label\{ref:([^}]+)\}')
keys = anchor.findall(bibliography)
assert len(keys) == len(set(keys)) == 25
wrapper = r'''

\begingroup
\makeatletter
\let\@bibtitlestyle\relax
\def\bibliofont{\normalsize}
\renewcommand{\@biblabel}[1]{}
\makeatother
\setlength{\labelsep}{0pt}
\begin{thebibliography}{}
\setlength{\emergencystretch}{5em}
\raggedright
'''
marked = anchor.sub(lambda m: '\\bibitem[]{ref-' + m.group(1) + '}\n' + m.group(0), bibliography)
assert marked.count(r'\end{document}') == 1
marked = marked.replace(r'\end{document}', '\\end{thebibliography}\n\\endgroup\n\n\\end{document}', 1)
result = head + heading + wrapper + marked
# Reverse the transformation before accepting it: no entry text or body edits.
reversed_text = re.sub(r'\\bibitem\[\]\{ref-[^}]+\}\n', '', result)
reversed_text = reversed_text.replace(wrapper, '', 1).replace('\\end{thebibliography}\n\\endgroup\n\n', '', 1)
assert reversed_text == text
args.tex.write_text(result)
args.tex.with_name('bibliography-markup.json').write_text(json.dumps({
    'entry_count': len(keys), 'citation_keys': ['ref-' + k for k in keys],
    'body_and_entry_payloads_exact_after_removing_markup': True,
    'bibliography_environment': 'thebibliography',
    'printed_entry_labels': 'empty; existing author-year text preserved',
    'scope': 'Local source-structure check; Hexagon server extraction not run.'
}, indent=2) + '\n')
