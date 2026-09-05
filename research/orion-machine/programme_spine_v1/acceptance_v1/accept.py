"""Fixed, additive acceptance of nine WP0 engineering deliveries in merged PR356.

This is not a general acceptance service and does not update any issue or old
checkpoint. GitHub observations are operator-captured facts, not signatures.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
SPINE=HERE.parent
ROOT=SPINE.parents[2]
sys.path.insert(0,str(SPINE))
import validate as V

REPOSITORY='SzeChunYiu/ORION-V2'
HEAD='c8bc253151082684448ed414458485981c828754'
MERGE='87332ead9e409fa598a3436a3553e3585d1f023c'
TREE='6c475636b549b26d555cd0cb8427189abe68e3a0'
BASE='9a7e6e1f2e4bfb015bd66a058477c5849571b0b4'
CHECKPOINT='23e2d2047bc436f23d71b9a397b2c2cf646badf3689e9675c2295d0aab294ffc'
RECEIPT_PATH='research/orion-machine/completion_audit_v1/spine-final-reviewed-v2-run.json'
RECEIPT_SHA='dee8af06de474a115f484d29cea3b369c0f78a58b2c3d9b90a927d24cd6f89db'
CHECKS={'Cursor Bugbot','custody-and-finite-replay (3.12)','custody-and-finite-replay (3.13)',
        'exact-finite-checks','freeze-binding-scan','programme-spine','exact-foundation (3.12)',
        'exact-foundation (3.13)','authority-reconciliation','public-native-fit','receipt-boundaries'}
IDS=[f'OM-WP0-{n:03d}' for n in range(1,10)]
PREFIX='research/orion-machine/programme_spine_v1/'


def git(*args):
    try:
        result=subprocess.run(['git',*args],cwd=ROOT,stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,timeout=30)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise V.CannotCheck('GIT_UNAVAILABLE: '+str(exc)) from exc
    if result.returncode:
        raise V.CannotCheck('GIT_OBJECT_UNAVAILABLE: '+' '.join(args))
    return result.stdout


def blob(path):
    return git('show',MERGE+':'+path)


def read_original(name):
    return V.parse(blob(PREFIX+name))


def observe(source):
    """Project actual captured API JSON; never fill pending facts with defaults."""
    filenames=['pr356-merged-0.json','pr356-merged-1.json','pr356-merged-2.json',
               'pr356-check-runs.json','pr356-repository.json']
    raw={n:V.read(source,n) for n in filenames}
    ref,commit,pull,checks,repo=[V.parse(raw[n]) for n in filenames]
    return {'schema':'OCM_WP0_MERGED_DELIVERY_OBSERVATION_V1',
            'raw_api_snapshot_sha256':{n:V.sha(raw[n]) for n in filenames},
            'repository':repo.get('repository_full_name',repo.get('full_name')),
            'default_branch':repo.get('default_branch'),
            'pull_request':{'number':pull.get('number'),'url':pull.get('html_url'),
                            'state':pull.get('state'),'merged':pull.get('merged'),
                            'merged_at':pull.get('merged_at'),'merge_commit':pull.get('merge_commit_sha'),
                            'head':pull.get('head',{}).get('sha'),
                            'base_ref':pull.get('base',{}).get('ref'),
                            'base_repository':pull.get('base',{}).get('repo',{}).get('full_name')},
            'merged_git_object':{'sha':commit.get('sha'),'tree':commit.get('tree',{}).get('sha'),
                                 'parents':[x.get('sha') for x in commit.get('parents',[])]},
            'observed_main_ref':{'ref':ref.get('ref'),'sha':ref.get('object',{}).get('sha')},
            'total_check_count':checks.get('total_count'),
            'checks':[{k:c.get(k) for k in ('id','name','head_sha','status','conclusion','completed_at','html_url')}
                      for c in checks.get('check_runs',[])],
            'authority_delta':'NONE'}


def validate_observation(observation):
    V.require(observation['repository']==REPOSITORY,'WRONG_REPOSITORY')
    V.require(observation['default_branch']=='main','WRONG_DEFAULT_BRANCH')
    pr=observation['pull_request']
    V.require(pr['number']==356 and pr['url']=='https://github.com/'+REPOSITORY+'/pull/356','WRONG_DELIVERY_PULL')
    if pr['merged'] is not True or pr['state']!='closed' or not pr['merged_at']:
        raise V.CannotCheck('DELIVERY_NOT_MERGED')
    V.require(pr['head']==HEAD and pr['merge_commit']==MERGE,'WRONG_DELIVERY_IDENTITY')
    V.require(pr['base_ref']=='main' and pr['base_repository']==REPOSITORY,'WRONG_DELIVERY_BASE')
    V.require(observation['merged_git_object']=={'sha':MERGE,'tree':TREE,'parents':[BASE,HEAD]},'WRONG_MERGE_OBJECT')
    V.require(observation['observed_main_ref']=={'ref':'refs/heads/main','sha':MERGE},'MERGE_NOT_OBSERVED_ON_MAIN')
    rows=observation['checks']
    V.require(type(observation['total_check_count']) is int and observation['total_check_count']==len(rows)==11,'INCOMPLETE_CHECK_INVENTORY')
    V.require({r['name'] for r in rows}==CHECKS and len({r['id'] for r in rows})==11,'WRONG_CHECK_INVENTORY')
    for row in rows:
        V.require(row['head_sha']==HEAD,'WRONG_CHECK_HEAD')
        if row['status']!='completed' or row['conclusion'] is None:
            raise V.CannotCheck('CHECK_NOT_COMPLETED: '+row['name'])
        V.require(row['conclusion']=='success' and bool(row['completed_at']),'CHECK_NOT_SUCCESSFUL',row['name'])
        V.require(type(row['id']) is int and row['id']>0 and
                  row['html_url'].startswith('https://github.com/'+REPOSITORY+'/'),'CHECK_IDENTITY_MISSING')
    V.require(observation['authority_delta']=='NONE','AUTHORITY_ESCALATION')


def originals():
    V.require(git('show','-s','--format=%T',MERGE).decode().strip()==TREE,'LOCAL_MERGE_TREE_MISMATCH')
    V.require(git('show','-s','--format=%P',MERGE).decode().strip().split()==[BASE,HEAD],'LOCAL_MERGE_PARENT_MISMATCH')
    # A mutable local worktree cannot substitute another validator for the merged one.
    V.require(blob(PREFIX+'validate.py')==(SPINE/'validate.py').read_bytes(),'PREDECESSOR_CHECKER_DRIFT')
    names=['SOURCE_ISSUES_V1.json','OCM_EXECUTION_BACKLOG_V1.json',
           'OCM_EXECUTION_BACKLOG_V1.schema.json','SOURCE_SNAPSHOT_V1.json','TASK_EVENTS_V1.jsonl']
    sources={n:blob(PREFIX+n) for n in names}
    for name,raw in sources.items():
        V.require(raw==git('show',HEAD+':'+PREFIX+name),'MERGE_CHANGED_TESTED_SOURCE',name)
    V.require(V.sha(sources['SOURCE_SNAPSHOT_V1.json'])==CHECKPOINT,'WRONG_PREDECESSOR_CHECKPOINT')
    receipt_raw=blob(RECEIPT_PATH)
    V.require(receipt_raw==git('show',HEAD+':'+RECEIPT_PATH) and V.sha(receipt_raw)==RECEIPT_SHA,'WRONG_PREACCEPTANCE_RECEIPT')
    return sources,receipt_raw


def derive(observation):
    validate_observation(observation)
    sources,receipt_raw=originals()
    backlog=V.parse(sources['OCM_EXECUTION_BACKLOG_V1.json'])
    schema=V.parse(sources['OCM_EXECUTION_BACKLOG_V1.schema.json'])
    source_issues=V.parse(sources['SOURCE_ISSUES_V1.json'])
    snapshot=V.parse(sources['SOURCE_SNAPSHOT_V1.json'])
    by_id=V.validate_backlog(backlog,schema,source_issues)
    receipt=V.parse(receipt_raw)
    for ident in IDS:
        V.validate_engineering_receipt(receipt,ident,by_id,CHECKPOINT,backlog['source_body_sha256'])
    original_events=sources['TASK_EVENTS_V1.jsonl']
    V.require(original_events.endswith(b'\n'),'INVALID_EVENT_PREFIX')
    events=[V.parse(x) for x in original_events.splitlines()]
    V.validate_events(events,by_id,snapshot['genesis_hash'])
    V.require(len(events)==19 and events[-1]['event_hash']==snapshot['event_tip'],'WRONG_PREDECESSOR_TIP')
    evidence={'kind':'ENGINEERING_VERIFICATION','path':RECEIPT_PATH,'sha256':RECEIPT_SHA,
              'commit':MERGE,'git_blob':git('rev-parse',MERGE+':'+RECEIPT_PATH).decode().strip(),
              'verified_checkpoint_sha256':CHECKPOINT,
              'scope':'Nine WP0 engineering artifacts delivered in PR356. Actual pre-acceptance checks and exact-head CI; no scientific or external-review admission.'}
    changes=[]
    appended=[]
    for ident in IDS:
        task=by_id[ident]
        V.require(task['status']=='READY_FOR_REVIEW' and task['terminal'] is None,'UNEXPECTED_PREDECESSOR_STATE',ident)
        task['status']='COMPLETE';task['terminal']='PASS';task['evidence'].append(copy.deepcopy(evidence))
        changes.append({'task_id':ident,'task_identity_sha256':V.task_identity(task),
                        'from_status':'READY_FOR_REVIEW','to_status':'COMPLETE','terminal':'PASS',
                        'verification_evidence':copy.deepcopy(evidence)})
        event={'sequence':len(events),'previous_hash':events[-1]['event_hash'],
               'kind':'STATUS_TRANSITION','task_id':ident,'task_identity_sha256':V.task_identity(task),
               'from_status':'READY_FOR_REVIEW','to_status':'COMPLETE','authority_delta':'NONE',
               'verification_receipt_sha256':RECEIPT_SHA,'verified_checkpoint_sha256':CHECKPOINT,
               'delivery_merge_commit':MERGE,'delivery_ci_head':HEAD,
               'delivery_observation_sha256':V.sha(V.canonical(observation))}
        event['event_hash']=V.sha(V.canonical(event));events.append(event)
        appended.append(V.canonical(event)+b'\n')
    V.validate_backlog(backlog,schema,source_issues)
    chain=V.validate_events(events,by_id,snapshot['genesis_hash'])
    V.require(by_id['OM-WP0-010']['status']=='OPEN','EXTERNAL_REVIEW_LAUNDERING')
    overlay={'schema':'OCM_EXECUTION_BACKLOG_ACCEPTANCE_OVERLAY_V1',
             'effective_status':'NINE_ENGINEERING_TASKS_ACCEPTED__PROGRAMME_OPEN',
             'predecessor_commit':MERGE,'predecessor_backlog_path':PREFIX+'OCM_EXECUTION_BACKLOG_V1.json',
             'predecessor_backlog_sha256':V.sha(sources['OCM_EXECUTION_BACKLOG_V1.json']),
             'predecessor_checkpoint_sha256':CHECKPOINT,'predecessor_event_tip':snapshot['event_tip'],
             'original_task_count':231,'accepted_task_ids':IDS,'changes':changes,
             'unchanged_task_count':222,'WP0_010_status':'OPEN',
             'external_science_reviews':{'199':'NOT_OBTAINED','245':'NOT_OBTAINED'},
             'authority_delta':'NONE','issue_checkbox_mutation_performed':False}
    report={'terminal':'WP0_NINE_ENGINEERING_DELIVERIES_ACCEPTED','accepted_tasks':9,
            'total_tasks':231,'unchanged_tasks':222,'source_check_count':11,
            'pre_acceptance_required_checks':receipt['required_checks'],
            'pre_acceptance_hostile_tests':next(r['result']['tests'] for r in receipt['rows'] if r['check_id']=='HOSTILES'),
            'original_events':19,'appended_events':9,**chain,
            'original_event_prefix_sha256':V.sha(original_events),
            'delivery_head':HEAD,'delivery_merge_commit':MERGE,'delivery_merge_tree':TREE,
            'scientific_admission':False,'independent_review_satisfied':False,
            'master_issue_197_closed':False,'issue_checkbox_mutation_performed':False}
    return {'BACKLOG_ACCEPTANCE_OVERLAY_V1.json':V.canonical(overlay)+b'\n',
            'TASK_EVENTS_WITH_ACCEPTANCE_V1.jsonl':original_events+b''.join(appended),
            'ACCEPTANCE_VALIDATION_V1.json':V.canonical(report)+b'\n'}


def materialize(source,output):
    observation=observe(source)
    derived=derive(observation) # Validate everything before making the new directory.
    derived['MERGED_DELIVERY_OBSERVATION_V1.json']=V.canonical(observation)+b'\n'
    output.mkdir(parents=True,exist_ok=False)
    for name,raw in derived.items():
        with (output/name).open('xb') as stream:stream.write(raw)
    manifest={'schema':'OCM_WP0_ACCEPTANCE_PACKET_MANIFEST_V1',
              'files':{name:V.sha(raw) for name,raw in derived.items()},
              'delivery_merge_commit':MERGE,'authority_delta':'NONE'}
    with (output/'MANIFEST_V1.json').open('xb') as stream:stream.write(V.canonical(manifest)+b'\n')
    return verify(output)


def verify(directory):
    manifest=V.load(directory,'MANIFEST_V1.json')
    expected_names={'MERGED_DELIVERY_OBSERVATION_V1.json','BACKLOG_ACCEPTANCE_OVERLAY_V1.json',
                    'TASK_EVENTS_WITH_ACCEPTANCE_V1.jsonl','ACCEPTANCE_VALIDATION_V1.json'}
    V.require(set(manifest['files'])==expected_names,'PACKET_INVENTORY_DRIFT')
    V.require({p.name for p in directory.iterdir()}==expected_names|{'MANIFEST_V1.json'},'UNREGISTERED_PACKET_FILE')
    for name,digest in manifest['files'].items():
        V.require(V.sha(V.read(directory,name))==digest,'PACKET_HASH_DRIFT',name)
    observation=V.load(directory,'MERGED_DELIVERY_OBSERVATION_V1.json')
    expected=derive(observation)
    for name,raw in expected.items():
        V.require(V.read(directory,name)==raw,'ACCEPTANCE_DERIVATION_DRIFT',name)
    V.require(manifest['delivery_merge_commit']==MERGE and manifest['authority_delta']=='NONE','PACKET_AUTHORITY_DRIFT')
    return V.parse(expected['ACCEPTANCE_VALIDATION_V1.json'])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--materialize-from',type=Path)
    parser.add_argument('--packet',type=Path,default=HERE/'packet')
    args=parser.parse_args(argv)
    try:
        result=materialize(args.materialize_from,args.packet) if args.materialize_from else verify(args.packet)
        code=0
    except V.Defect as exc:result={'terminal':'FAIL','reason':str(exc)};code=1
    except (V.CannotCheck,OSError) as exc:result={'terminal':'CANNOT_CHECK','reason':str(exc)};code=2
    except (KeyError,TypeError,ValueError) as exc:result={'terminal':'FAIL','reason':'MALFORMED_INPUT: '+str(exc)};code=1
    print(json.dumps(result,sort_keys=True,indent=2));return code

if __name__=='__main__':raise SystemExit(main())
