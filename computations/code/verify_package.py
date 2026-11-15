"""Host-only validation of files, recorded runs and scope mappings; no math imports."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def load(p):return json.loads(p.read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()
def records(folder):
    found=[]
    for line in (folder/'log.jsonl').read_text().splitlines():
        try:found.append(json.loads(line))
        except json.JSONDecodeError:pass
    return found

def validate_run(entry):
    runtime=ROOT/entry['runtime_root'];folder=ROOT/entry['result_dir']
    d=load(folder/'result.json');e=load(folder/'environment.json');w=d['worker_summary']
    label=entry['job'];cfg=load(runtime/'environment.lock.json');job=load(runtime/'jobs.json')[label]
    require(d['status']=='PASS' and d['client_exit_code']==0,label+' failed')
    require(d['stopped'] and d['removed'] and d['lock_released'],label+' cleanup')
    require(e['container_state']['ExitCode']==0 and not e['container_state']['OOMKilled'],label+' container state')
    require(not e['error'] and not e['mathematics_on_host'],label+' controller error')
    require(d['log_sha256']==digest(folder/'log.jsonl'),label+' log digest')
    ids=[r['id'] for r in d['checks']]
    require(len(ids)==len(set(ids)) and set(ids)==set(entry['check_ids'])==set(job['check_ids']),label+' check IDs')
    require(all(r['status']=='PASS' for r in d['checks']) and not w['failed'] and not w['missing'] and not w['error'],label+' false success')
    for key in ('python','sage','sympy'):require(w['versions'][key]==cfg[key],label+' version')
    require(int(w['metrics']['memory.peak'])<=cfg['memory_bytes'],label+' peak')
    hc=e['host_config']
    require(hc['Memory']==hc['MemorySwap']==1999998976 and hc['NanoCpus']==1_000_000_000 and hc['PidsLimit']==32,label+' resource enforcement')
    require(hc['NetworkMode']=='none' and hc['ReadonlyRootfs'] and not hc['OomKillDisable'] and hc['RestartPolicy']['Name']=='no',label+' isolation')
    for filename,value in e['input_hashes'].items():
        require(not Path(filename).is_absolute(),label+' input path')
        require(digest(runtime/filename)==value,label+' changed actual input '+filename)
    logs=records(folder);pre=[r for r in logs if r.get('record')=='preflight']
    require(len(pre)==1,label+' missing preflight')
    cg=pre[0]['cgroup'];q,p=map(int,cg['cpu.max'].split())
    require(int(cg['memory.max'])<=1999998976 and cg['memory.swap.max']=='0' and 0<q<=p and int(cg['pids.max'])<=32,label+' cgroup')
    require(pre[0]['ipv4_route_rows']==0 and pre[0]['ipv6_only_loopback'],label+' network')
    if entry['runtime_root']=='jets/':
        pinned=load(runtime/'dependency-hashes.json')
        deps=[r['verified'] for r in logs if r.get('record')=='dependencies']
        require(len(deps)==1 and set(deps[0])==set(job['dependencies']),label+' incomplete imported dependency evidence')
        for filename in job['dependencies']:
            require(digest(runtime/filename)==pinned[filename]==deps[0][filename]==e['input_hashes'][filename],label+' unbound helper '+filename)
        domain=[r for r in logs if r.get('record')=='jet-domain']
        require(len(domain)==1 and domain[0]['first']==24 and domain[0]['second']==60 and domain[0]['ricci_symmetry']=='PASS',label+' input domain')
        if job['jet_order']==3:require(domain[0]['third']==120,label+' third domain')
    return d

def main():
    rows=load(ROOT/'checks.json');execution=load(ROOT/'execution-index.json')
    require(len(rows)==68 and len({r['id'] for r in rows})==68,'68 unique check IDs required')
    allids={cid for e in execution['jobs'] for cid in e['check_ids']}
    require(allids=={r['id'] for r in rows},'Correspondence/job mismatch')
    binding=load(ROOT/'MANUSCRIPT-LOCATORS.json')
    require(binding['target_version']==load(ROOT.parent/'docs/release-status.json')['paper_version'],'Wrong target version')
    require(digest(ROOT/binding['target_path'])==binding['target_sha256'],'Paper source digest')
    reference=binding['rendered_reference']
    require(digest(ROOT/reference['pdf_path'])==reference['pdf_sha256'],'Paper PDF digest')
    locators=binding['locators']
    for row in rows:
        catalog=load(ROOT/row.get('input_catalog','inputs.json'))
        require(row['input'] in (catalog['profiles'] if 'profiles' in catalog else catalog),'Missing input profile')
        tree=ast.parse((ROOT/row['implementation']).read_text())
        funcs={n.name:n.lineno for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
        require(funcs.get(row['function'])==row['function_line'],'Function/line mismatch')
        require(not any(isinstance(n,ast.Constant) and isinstance(n.value,float) for n in ast.walk(tree)),'Float literal in calculation source')
        require(set(row['anchors'])<=set(locators),'Missing manuscript locator')
        rendered=row['rendered_reference']
        require(row['manuscript_version']==binding['target_version'] and row['manuscript_sha256']==binding['target_sha256'],'Index source binding')
        require(rendered['version']==binding['target_version'] and rendered['pdf_sha256']==reference['pdf_sha256'],'Wrong paper version/hash')
        for v in rendered['equations']:
            require(locators[v['anchor']]['rendered_equation_number']==v['number'] and locators[v['anchor']]['rendered_page']==v['page'],'Printed locator mismatch')
        require(row['id'] in (ROOT/'CHECKS.md').read_text(),'Missing Markdown row')
    actual={}
    for entry in execution['jobs']:
        d=validate_run(entry)
        actual.update({r['id']:r for r in d['checks']})
    for row in rows:
        require(actual[row['id']]['status']==row['actual_result']['status']=='PASS','Index differs from actual output')
        require(digest(ROOT/row['actual_result']['log'])==row['actual_result']['log_sha256'],'Index/log digest')
    for probe in execution['probes']:
        runtime=ROOT/probe['runtime_root'];folder=ROOT/probe['result_dir'];d=load(folder/'result.json');e=load(folder/'environment.json')
        require(d['status']=='FAIL' and d['client_exit_code']==probe['expected_exit']==1,'False-check probe did not fail')
        require(d['stopped'] and d['removed'] and d['lock_released'],'Probe cleanup')
        require(d['worker_summary']['failed']==['RUNNER-FAILURE-PROBE'] and not d['worker_summary']['missing'] and not d['worker_summary']['error'],'Unexpected probe failure')
        require(digest(folder/'log.jsonl')==d['log_sha256'],'Probe log')
        for filename,value in e['input_hashes'].items():require(digest(runtime/filename)==value,'Probe input drift')
    retained=load(ROOT/'rc1-retained-hashes.json')
    require(retained['source_zip_sha256']==execution['rc1_zip_sha256'],'rc.1 source identity')
    for filename,value in retained['files'].items():require(digest(ROOT/filename)==value,'Changed retained rc.1 file '+filename)
    rc2=load(ROOT/'rc2-retained-hashes.json')
    for filename,value in rc2['files'].items():require(digest(ROOT/filename)==value,'Changed retained rc.2 file '+filename)
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink in payload')
        if not p.is_file():continue
        require(p.name!='.DS_Store' and '__pycache__' not in p.parts,'Unintended file')
        text=p.read_text()
        require(not re.search(r'[\u3040-\u30ff\u3400-\u9fff]',text),'Unintended Japanese/CJK')
        require(not re.search(r'/U[s]ers/|[A-Za-z]:\\U[s]ers\\|\.code[x]/|plugi[n]://|source[_]thread[_]id|cha[t]log/',text),'Private path/chat')
        require(not re.search(r'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----',text),'Possible credential')
        if p.suffix=='.md':
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in target or target.startswith('#'):continue
                require((p.parent/target.split('#')[0]).exists(),'Broken local link '+target)
    manifest={}
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        value,name=line.split('  ',1);manifest[name]=value
        require(digest(ROOT/name)==value,'Manifest hash '+name)
    require(set(manifest)=={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'},'Manifest coverage')
    print(json.dumps({'status':'PASS','mathematical_checks':len(actual),'retained_rc1_checks':57,'fresh_jet_checks':11,'mathematical_jobs':len(execution['jobs']),'false_check_probes':len(execution['probes']),'retained_files':len(retained['files']),'manifest_files':len(manifest),'helper_hashes_and_import_evidence':'PASS','privacy_and_local_links':'PASS','math_reexecuted_by_validation':False},indent=2))

if __name__=='__main__':main()
