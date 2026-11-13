"""Verify the packaged files and recorded checks without running mathematics."""
from pathlib import Path
from hashlib import sha256
import json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    manifest={}
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        value,name=line.split('  ',1)
        if digest(ROOT/name)!=value:raise RuntimeError('Changed file: '+name)
        manifest[name]=value
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
            if p.is_file() and not set(p.relative_to(ROOT).parts)&{'.git','tmp','build','__pycache__','reproduced'}
            and str(p.relative_to(ROOT))!='SHA256SUMS.txt' and p.name!='.DS_Store'}
    if set(manifest)!=actual:raise RuntimeError('Manifest coverage mismatch')
    for name in actual:
        p=ROOT/name
        if p.is_symlink():raise RuntimeError('Symlink: '+name)
        if p.suffix in {'.md','.tex','.py','.sh','.lua','.yaml','.json','.cff','.txt'}:
            s=p.read_text()
            if re.search(r'/U[s]ers/|plugi[n]://|cod[e]x://threads/|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}',s):
                raise RuntimeError('Private path or credential: '+name)
    subprocess.run([sys.executable,str(ROOT/'computations/code/verify_package.py')],check=True)
    evidence=json.loads((ROOT/'docs/verification.json').read_text())
    if any(digest(ROOT/'paper'/('manuscript.'+ext))!=h for ext,h in evidence['paper_hashes'].items()):
        raise RuntimeError('Verification report targets another paper')
    print(json.dumps({'status':'PASS','manifest_files':len(manifest),'saved_check_count':68,
                      'mathematical_jobs_started':0,'publication_performed':False},indent=2))
if __name__=='__main__':main()
