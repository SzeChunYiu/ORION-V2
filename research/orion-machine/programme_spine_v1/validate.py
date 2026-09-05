"""Read-only prefreeze programme-spine validation: 0 valid, 1 defect, 2 unavailable.

The trust root is this reviewed code at its Git identity, not a hash kept beside
mutable data. V1 is an immutable checkpoint; later events require a successor
checkpoint and review. No event grants research, proof, adoption or issue authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[2]
SNAPSHOT_SHA256 = '23e2d2047bc436f23d71b9a397b2c2cf646badf3689e9675c2295d0aab294ffc'
SCHEMA_KEYS = {'$schema', '$id', 'type', 'const', 'enum', 'properties', 'required',
               'additionalProperties', 'items', 'minItems', 'maxItems',
               'uniqueItems', 'minLength', 'pattern', 'minimum'}

class Defect(Exception):
    pass

class CannotCheck(Exception):
    pass

def require(condition, code, detail=''):
    if not condition:
        raise Defect(f'{code}: {detail}')

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pairs(values):
    out = {}
    for key, value in values:
        require(key not in out, 'DUPLICATE_JSON_KEY', key)
        out[key] = value
    return out

def parse(raw):
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(Defect('NONFINITE_JSON: '+x)))
    except (ValueError, UnicodeError) as exc:
        raise Defect('INVALID_JSON: '+str(exc)) from exc

def safe_file(root, relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == relative,
            'UNSAFE_PATH', relative)
    root = root.resolve()
    target = root
    for component in p.parts:
        target = target / component
        require(not target.is_symlink(), 'SYMLINK_INPUT', relative)
    if not target.is_file():
        raise CannotCheck('MISSING_INPUT: '+relative)
    return target

def read(root, relative):
    return safe_file(root, relative).read_bytes()

def load(root, relative):
    return parse(read(root, relative))

def schema_check(value, schema, path='$'):
    """Evaluate all keywords used by the shipped schema; refuse unknown keywords.

    This is a deliberately restricted JSON Schema evaluator, not a general
    Draft-2020-12 implementation. External full-engine verification is separate.
    """
    unknown = set(schema)-SCHEMA_KEYS
    if unknown:
        raise CannotCheck('UNSUPPORTED_SCHEMA_KEYWORD: '+','.join(sorted(unknown)))
    if 'type' in schema:
        types = {'object':dict, 'array':list, 'string':str, 'integer':int,
                 'boolean':bool, 'null':type(None)}
        if schema['type'] not in types:
            raise CannotCheck('UNSUPPORTED_SCHEMA_TYPE: '+str(schema['type']))
        require(type(value) is types[schema['type']], 'SCHEMA_TYPE', path)
    if 'const' in schema:
        require(type(value) is type(schema['const']) and value == schema['const'], 'SCHEMA_CONST', path)
    if 'enum' in schema:
        require(any(type(value) is type(x) and value == x for x in schema['enum']), 'SCHEMA_ENUM', path)
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= set(value), 'SCHEMA_REQUIRED', path)
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            require(set(value) <= set(props), 'SCHEMA_ADDITIONAL_PROPERTY', path)
        for key, item in value.items():
            if key in props:
                schema_check(item, props[key], path+'.'+key)
    if isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), 'SCHEMA_MIN_ITEMS', path)
        require(len(value) <= schema.get('maxItems', len(value)), 'SCHEMA_MAX_ITEMS', path)
        if schema.get('uniqueItems'):
            require(len({canonical(x) for x in value}) == len(value), 'SCHEMA_UNIQUE_ITEMS', path)
        for i, item in enumerate(value):
            if 'items' in schema:
                schema_check(item, schema['items'], f'{path}[{i}]')
    if isinstance(value, str):
        require(len(value) >= schema.get('minLength', 0), 'SCHEMA_MIN_LENGTH', path)
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None, 'SCHEMA_PATTERN', path)
    if type(value) is int and 'minimum' in schema:
        require(value >= schema['minimum'], 'SCHEMA_MINIMUM', path)

def source_tasks(body):
    """Recover all231 source checkbox identities independently of backlog data."""
    lines = body.splitlines()
    result = {}
    package = None
    counts = {}
    for i, line in enumerate(lines):
        if line.startswith('## Positive package'):
            package = 'POSITIVE'
        elif line.startswith('## Negative/equivalence package'):
            package = 'NEGATIVE'
        elif line.startswith('## CANNOT_CHECK package'):
            package = 'CANNOT_CHECK'
        if not re.match(r'^- \[[ x]\] ', line):
            continue
        match = re.match(r'^- \[[ x]\] `([^`]+)`\s*(.*)', line)
        if match:
            ident, description = match.groups()
        else:
            require(package is not None, 'UNIDENTIFIED_CHECKBOX', str(i+1))
            counts[package] = counts.get(package, 0)+1
            ident = f'OM-CLOSE-{package}-{counts[package]:02d}'
            description = line[6:]
        follow = []
        for next_line in lines[i+1:]:
            if not next_line.startswith('  '):
                break
            follow.append(next_line)
        require(ident not in result, 'DUPLICATE_SOURCE_TASK', ident)
        result[ident] = {'task_id':ident,
                        'task_kind':'PROTOCOL' if ident.startswith('OPS') else 'COMPLETION_GATE' if ident.startswith('OM-CLOSE') else 'WORK',
                        'source_line':i+1, 'source_checkbox':line,
                        'description':description, 'acceptance_text':'\n'.join(follow)}
    return result

def task_identity(task):
    return sha(canonical({k:task[k] for k in ('task_id','task_kind','source_line',
                                             'source_checkbox','description','acceptance_text')}))

def validate_backlog(backlog, schema, source):
    schema_check(backlog, schema)
    body = source['197']['body']
    require(backlog['source_body_sha256'] == sha(body.encode()), 'SOURCE_BODY_DRIFT')
    expected = source_tasks(body)
    tasks = backlog['tasks']
    ids = [t['task_id'] for t in tasks]
    require(len(ids) == len(set(ids)), 'DUPLICATE_TASK')
    require(set(ids) == set(expected), 'SOURCE_TASK_COVERAGE')
    by_id = {t['task_id']:t for t in tasks}
    for task in tasks:
        ident = task['task_id']
        require(all(task[k] == v for k,v in expected[ident].items()), 'TASK_STATEMENT_MUTATION', ident)
        for dep in task['dependencies']:
            require(dep in by_id, 'DANGLING_DEPENDENCY', dep)
        if task['status'] == 'COMPLETE':
            require(bool(task['evidence']), 'CHECKED_WITHOUT_EVIDENCE', ident)
            require(ident in {f'OM-WP0-{n:03d}' for n in range(1,10)} and task['terminal']=='PASS' and any(e['kind']=='ENGINEERING_VERIFICATION' for e in task['evidence']), 'UNAUTHORIZED_COMPLETION', 'Scientific acceptance is separate; engineering completion needs its source-bound verification receipt.')
        else:
            require(task['terminal'] is None, 'UNAUTHORIZED_TERMINAL', ident)
    visited, visiting = set(), set()
    def visit(ident):
        require(ident not in visiting, 'CYCLIC_DEPENDENCY', ident)
        if ident in visited:
            return
        visiting.add(ident)
        for dep in by_id[ident]['dependencies']:
            visit(dep)
        visiting.remove(ident)
        visited.add(ident)
    for ident in ids:
        visit(ident)
    for task in tasks:
        if task['status']=='COMPLETE':
            require(all(by_id[d]['status']=='COMPLETE' for d in task['dependencies']), 'INCOMPLETE_DEPENDENCY',task['task_id'])
    return by_id

def git_bytes(root, expression):
    try:
        proc = subprocess.run(['git','cat-file','blob',expression], cwd=root,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CannotCheck('GIT_UNAVAILABLE: '+str(exc)) from exc
    if proc.returncode:
        raise CannotCheck('GIT_OBJECT_UNAVAILABLE: '+expression)
    return proc.stdout

def validate_binding(binding, root):
    path = binding['path']
    require(re.fullmatch(r'[0-9a-f]{40}',binding['commit']) is not None, 'BAD_COMMIT_IDENTITY')
    require(re.fullmatch(r'[0-9a-f]{40}',binding['git_blob']) is not None, 'BAD_BLOB_IDENTITY')
    current = read(root,path)
    require(len(current) == binding['bytes'] and sha(current) == binding['sha256'], 'PROOF_HASH_DRIFT', path)
    original = git_bytes(root,binding['commit']+':'+path)
    require(original == current, 'STALE_EVIDENCE_POINTER', path)
    actual_blob = hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
    require(actual_blob == binding['git_blob'], 'GIT_BLOB_MISMATCH', path)

def validate_events(events, by_id, genesis, *, root=None, source_bindings=None):
    require(bool(events), 'EMPTY_EVENT_HISTORY')
    require(events[0]['kind'] == 'GENESIS', 'MISSING_GENESIS')
    require(events[0]['event_hash'] == genesis, 'RESET_EVENT_HISTORY')
    identity = {k:task_identity(v) for k,v in by_id.items()}
    require(events[0]['task_identity_sha256'] == sha(canonical(identity)), 'EVENT_TASK_IDENTITY_DRIFT')
    states = {k:'OPEN' for k in by_id}
    previous = '0'*64
    claims = set()
    seen_revisions = set()
    for i,event in enumerate(events):
        require(type(event.get('sequence')) is int and event['sequence'] == i, 'EVENT_SEQUENCE')
        require(event.get('previous_hash') == previous, 'EVENT_CHAIN_BREAK')
        unsigned = {k:v for k,v in event.items() if k != 'event_hash'}
        require(event.get('event_hash') == sha(canonical(unsigned)), 'EVENT_HASH_DRIFT')
        require(event.get('authority_delta') == 'NONE', 'EVENT_AUTHORITY_ESCALATION')
        previous = event['event_hash']
        if i==0:
            continue
        require(event.get('kind') != 'GENESIS', 'RESET_EVENT_HISTORY')
        task = event.get('task_id')
        require(task in by_id, 'EVENT_UNKNOWN_TASK')
        require(event.get('task_identity_sha256') == identity[task], 'EVENT_TASK_IDENTITY_DRIFT')
        if event['kind'] in ('CLAIM','STATUS_TRANSITION'):
            require(event['from_status'] == states[task], 'EVENT_STATE_MISMATCH')
            transition = (event['from_status'],event['to_status'])
            allowed = {('OPEN','IN_PROGRESS'),('IN_PROGRESS','READY_FOR_REVIEW'),('OPEN','BLOCKED'),('IN_PROGRESS','BLOCKED'),('READY_FOR_REVIEW','IN_PROGRESS'),('BLOCKED','IN_PROGRESS'),('READY_FOR_REVIEW','COMPLETE')}
            require(transition in allowed, 'EVENT_UNAUTHORIZED_TRANSITION')
            if event['kind']=='CLAIM':
                require(transition==('OPEN','IN_PROGRESS') and task not in claims, 'DUPLICATE_CLAIM')
                claims.add(task)
            if event['to_status']=='COMPLETE':
                require(task in {f'OM-WP0-{n:03d}' for n in range(1,10)} and by_id[task]['terminal']=='PASS' and any(e['kind']=='ENGINEERING_VERIFICATION' for e in by_id[task]['evidence']), 'EVENT_UNAUTHORIZED_TRANSITION')
                require(all(states[d]=='COMPLETE' for d in by_id[task]['dependencies']), 'INCOMPLETE_EVENT_DEPENDENCY',task)
                verification=next(e for e in by_id[task]['evidence'] if e['kind']=='ENGINEERING_VERIFICATION')
                require(event.get('verification_receipt_sha256')==verification['sha256'] and event.get('verified_checkpoint_sha256')==verification.get('verified_checkpoint_sha256'), 'EVENT_ACCEPTANCE_SUBJECT_DRIFT')
            states[task] = event['to_status']
        elif event['kind'] in ('THEOREM_REVISION','REFUTATION','SUPERSESSION'):
            # Informational proposed successor only. Original theorem/checkpoint survives;
            # status promotion and scientific acceptance are deliberately unavailable.
            require(root is not None and source_bindings is not None, 'REVISION_CUSTODY_REQUIRED')
            old = event.get('predecessor_path'); new = event.get('successor_path')
            require(old in source_bindings and old != new, 'REVISION_PREDECESSOR_MISSING')
            require(event.get('predecessor_sha256') == source_bindings[old]['sha256'], 'REVISION_PREDECESSOR_DRIFT')
            require(event.get('successor_sha256') == sha(read(root,new)), 'REVISION_SUCCESSOR_DRIFT')
            require(event.get('scope') and event.get('non_consequences'), 'REVISION_SCOPE_MISSING')
            require(new not in seen_revisions, 'DUPLICATE_REVISION')
            seen_revisions.add(new)
        else:
            raise Defect('UNKNOWN_EVENT_KIND: '+str(event['kind']))
    require(all(t['status'] == states[k] for k,t in by_id.items()), 'UNRECORDED_STATUS_TRANSITION')
    return {'event_count':len(events),'event_tip':previous}

def check_denominator(record):
    require(type(record.get('denominator')) is int and record['denominator'] > 0, 'EMPTY_DENOMINATOR')
    require(type(record.get('numerator')) is int and 0 <= record['numerator'] <= record['denominator'], 'BAD_NUMERATOR')

def check_measurement(record):
    require(record.get('status') in ('MEASURED','UNKNOWN','NOT_APPLICABLE'), 'RESOURCE_STATUS')
    if record['status']=='UNKNOWN':
        require(record.get('value') is None, 'UNMEASURED_RESOURCE_ZERO')
    elif record['status']=='NOT_APPLICABLE':
        require(record.get('value') is None and bool(record.get('reason')), 'RESOURCE_APPLICABILITY_UNJUSTIFIED')
    else:
        require(type(record.get('value')) is int and record['value']>=0, 'RESOURCE_VALUE')
        require(bool(record.get('source')) and bool(record.get('unit')), 'UNCHARGED_RESOURCE')
        check_denominator(record)

def validate_engineering_receipt(receipt, task_id, by_id, checkpoint, source_body):
    """Validate scoped PRE-acceptance check receipt; never grant scientific authority."""
    engineering_ids=[f'OM-WP0-{n:03d}' for n in range(1,10)]
    expected_scope={'task_ids':engineering_ids,
                    'task_identity_sha256':{x:task_identity(by_id[x]) for x in engineering_ids},
                    'source_body_sha256':source_body,
                    'checkpoint_phase':'PRE_ACCEPTANCE'}
    require(receipt.get('engineering_scope')==expected_scope and task_id in engineering_ids,
            'ENGINEERING_RECEIPT_WRONG_SUBJECT')
    require(receipt.get('source_snapshot_sha256')==checkpoint, 'ENGINEERING_RECEIPT_WRONG_CHECKPOINT')
    require(receipt.get('terminal')=='PASS_REQUIRED_ENGINEERING_CHECKS' and
            receipt.get('scientific_admission') is False and
            receipt.get('independent_review_satisfied') is False and
            receipt.get('protected_outcomes_accessed') is False, 'ENGINEERING_RECEIPT_AUTHORITY')
    required_ids={'SPINE','HOSTILES','TRACE_PARENT','REPRESENTATION','COMPILER_CORRECTION','SUBSTRATE'}
    rows=receipt.get('rows',[])
    require(isinstance(rows,list) and len(rows)==7 and {r.get('check_id') for r in rows}==required_ids|{'PROOF_ASSISTANT'}, 'ENGINEERING_RECEIPT_CHECK_INVENTORY')
    required=[]
    previous=checkpoint
    for row in rows:
        require(type(row.get('required')) is bool, 'ENGINEERING_RECEIPT_REQUIRED_TYPE')
        require(row.get('previous_hash')==previous and row.get('receipt_hash')==sha(canonical({k:v for k,v in row.items() if k!='receipt_hash'})), 'ENGINEERING_RECEIPT_CHAIN')
        previous=row['receipt_hash']
        if row['required']:
            required.append(row)
    require(receipt.get('final_receipt_hash')==previous, 'ENGINEERING_RECEIPT_TIP')
    require({r['check_id'] for r in required}==required_ids, 'ENGINEERING_RECEIPT_REQUIRED_INVENTORY')
    check_denominator({'numerator':receipt.get('required_passes'),'denominator':receipt.get('required_checks')})
    require(receipt['required_checks']==len(required) and receipt['required_passes']==len(required) and
            all(r.get('status')=='PASS' and type(r.get('exit_code')) is int and r['exit_code']==0 for r in required), 'ENGINEERING_RECEIPT_FALSE_GREEN')
    hostile=next(r for r in required if r['check_id']=='HOSTILES')['result']
    require(type(hostile.get('tests')) is int and hostile['tests']>0 and type(hostile.get('skips')) is int and hostile['skips']==0,'ENGINEERING_RECEIPT_NO_HOSTILE')
    spine=next(r for r in required if r['check_id']=='SPINE')['result']
    require(type(spine.get('accepted_tasks')) is int and spine['accepted_tasks']==0 and type(spine.get('tasks')) is int and spine['tasks']==231,'ENGINEERING_RECEIPT_NOT_PRE_ACCEPTANCE')
    require(type(receipt.get('all_checks_pass')) is bool and receipt['all_checks_pass']==all(r['status']=='PASS' for r in rows),'ENGINEERING_RECEIPT_ROLLUP')


def validate(root=ROOT, directory=DIRECTORY):
    backlog = load(directory,'OCM_EXECUTION_BACKLOG_V1.json')
    schema = load(directory,'OCM_EXECUTION_BACKLOG_V1.schema.json')
    source = load(directory,'SOURCE_ISSUES_V1.json')
    by_id = validate_backlog(backlog,schema,source)
    snapshot_raw = read(directory,'SOURCE_SNAPSHOT_V1.json')
    require(sha(snapshot_raw) == SNAPSHOT_SHA256, 'TRUST_ROOT_DRIFT')
    snapshot = parse(snapshot_raw)
    require(sha(read(directory,'SOURCE_ISSUES_V1.json')) == snapshot['source_issue_snapshot_sha256'], 'ISSUE_SNAPSHOT_DRIFT')
    graph={k:t['dependencies'] for k,t in by_id.items()}
    require(sha(canonical(graph))==snapshot['dependency_graph_sha256'], 'DEPENDENCY_GRAPH_DRIFT')
    for path,digest in snapshot['derived_artifacts_sha256'].items():
        require(sha(read(root,path))==digest, 'DERIVED_CONTRACT_DRIFT',path)
    bindings = {x['path']:x for x in snapshot['source_bindings']}
    require(len(bindings) == len(snapshot['source_bindings']), 'DUPLICATE_SOURCE_BINDING')
    for binding in bindings.values():
        validate_binding(binding,root)
    for task in by_id.values():
        for path in task['artifacts']:
            safe_file(root,path)
        for evidence in task['evidence']:
            if evidence['kind']=='ENGINEERING_VERIFICATION':
                require('commit' in evidence and 'git_blob' in evidence, 'UNBOUND_ENGINEERING_RECEIPT')
                raw=read(root,evidence['path'])
                validate_binding({**evidence,'bytes':len(raw)},root)
                receipt=parse(raw)
                require(evidence.get('verified_checkpoint_sha256')==SNAPSHOT_SHA256, 'WRONG_ACCEPTANCE_CHECKPOINT')
                validate_engineering_receipt(receipt,task['task_id'],by_id,SNAPSHOT_SHA256,backlog['source_body_sha256'])
            else:
                require(evidence['path'] in bindings, 'STALE_EVIDENCE_POINTER', evidence['path'])
                require(evidence['sha256'] == bindings[evidence['path']]['sha256'], 'STALE_EVIDENCE_POINTER', evidence['path'])
    events = [parse(x) for x in read(directory,'TASK_EVENTS_V1.jsonl').splitlines()]
    report = validate_events(events,by_id,snapshot['genesis_hash'],root=root,source_bindings=bindings)
    require(report['event_count'] == snapshot['event_count'] and report['event_tip'] == snapshot['event_tip'], 'UNANCHORED_EVENT_CHECKPOINT')
    require(events[0]['schema_sha256'] == sha(read(directory,'OCM_EXECUTION_BACKLOG_V1.schema.json')), 'SCHEMA_HASH_DRIFT')
    require(events[0]['theorem_snapshot_sha256'] == sha(read(directory,'THEOREM_CANDIDATE_SNAPSHOT_V1.json')), 'UNRECORDED_THEOREM_REVISION')
    theorem = load(directory,'THEOREM_CANDIDATE_SNAPSHOT_V1.json')
    for row in theorem['theorems']:
        require(row['statement_path'] in bindings and row['statement_sha256'] == bindings[row['statement_path']]['sha256'], 'THEOREM_STATEMENT_HASH_DRIFT')
        require(set(row['task_ids']) <= set(by_id), 'THEOREM_UNKNOWN_TASK')
        require(row['independent_review']=='NOT_OBTAINED' and row['authority_delta']=='NONE', 'THEOREM_AUTHORITY_ESCALATION')
        for path in row['successor_paths']+row['checker_paths']:
            require(path in bindings, 'THEOREM_UNBOUND_SOURCE',path)
    ownership = load(directory,'OCM_PARENT_OWNERSHIP_MAP_V1.json')
    for row in ownership['rows']:
        require(set(row['task_ids']) <= set(by_id), 'OWNERSHIP_UNKNOWN_TASK')
        require(row['authority_delta']=='NONE' and bool(row['gap']), 'OWNERSHIP_AUTHORITY_ESCALATION')
        require(bool(row['source_paths']) and set(row['source_paths']) <= set(bindings), 'OWNERSHIP_UNBOUND_SOURCE')
    resource = load(directory,'OCM_RESOURCE_CONTRACT_V0.json')
    required = {'B_theta','B_static','B_mut_peak','B_mut_total','T_seq','W_total','IO','BW','V_cost','train_cost','Q_resource','energy_if_valid'}
    require({x['name'] for x in resource['coordinates']} == required and len(resource['coordinates'])==12,'MISSING_RESOURCE_COORDINATE')
    for coordinate in resource['coordinates']:
        check_measurement({'status':coordinate['measurement_status'],'value':coordinate['value']})
    return {'terminal':'PASS_ENGINEERING_SPECIFICATION_ONLY','tasks':len(by_id),
            'numbered_source_tasks':214,'completion_package_obligations':17,
            'source_bindings':len(bindings),**report,'accepted_tasks':sum(t['status']=='COMPLETE' for t in by_id.values()),
            'independent_review':'NOT_OBTAINED','scientific_admission':False}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--directory',type=Path,default=DIRECTORY)
    args = parser.parse_args(argv)
    try:
        result = validate(args.root,args.directory)
        code = 0
    except Defect as exc:
        result={'terminal':'FAIL','reason':str(exc)}; code=1
    except (CannotCheck,OSError,subprocess.SubprocessError) as exc:
        result={'terminal':'CANNOT_CHECK','reason':str(exc)}; code=2
    except (KeyError,TypeError,IndexError) as exc:
        result={'terminal':'FAIL','reason':'MALFORMED_INPUT: '+str(exc)}; code=1
    print(json.dumps(result,sort_keys=True,indent=2))
    return code

if __name__=='__main__':
    raise SystemExit(main())
