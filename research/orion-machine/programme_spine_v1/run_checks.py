"""Chained, read-only verifier for an explicit allowlist of prefreeze research checks.

No command is accepted from a backlog, issue, JSON plan or shell fragment.
An optional, unregistered proof target is CANNOT_CHECK even if a binary exists.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import validate as V

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
# This reviewed code is the command allowlist. Changing it requires a code review.
COMMANDS = {
    'SPINE': [str(HERE/'validate.py')],
    'HOSTILES': ['-m','unittest','discover','-s',str(HERE),'-p','test_spine.py','-v'],
    'TRACE_PARENT': ['research/orion-machine/reference/ocm_lane200_decomposition_exact.py','--json'],
    'REPRESENTATION': ['research/orion-machine/reference/ocm_lane201_lattice_exact.py','--json'],
    'COMPILER_CORRECTION': ['research/orion-machine/reference/ocm_lane202_invariance_correction_exact.py'],
    'SUBSTRATE': ['research/orion-machine/reference/ocm_reference_semantics.py','--json'],
}
TERMINALS = {
    'SPINE':'PASS_ENGINEERING_SPECIFICATION_ONLY',
    'TRACE_PARENT':'PASS_EVERY_REGISTERED_CLASS_IS_A_DIRECT_PRODUCT_OF_PARENT_PROBLEMS',
    'REPRESENTATION':'PASS_REPRESENTATION_LATTICE_PARENT_OWNED_FINITE',
    'COMPILER_CORRECTION':'SCOPED_COMPILER_BOUND_CORRECTION_CALIBRATED',
    'SUBSTRATE':'PASS_SUBSTRATE_CONSTRAINTS_EXACT',
}

def classify(returncode, *, tool_registered=True):
    if not tool_registered or returncode==2:
        return 'CANNOT_CHECK'
    return 'PASS' if returncode==0 else 'FAIL'

def check_output(ident, stdout, stderr):
    if ident=='HOSTILES':
        # unittest returns zero for zero tests too; pin a nonempty reviewed denominator.
        import re
        match = re.search(r'Ran (\d+) tests? in ',stderr)
        V.require(match is not None and int(match.group(1)) >= 8, 'EMPTY_HOSTILE_TEST_RUN')
        V.require(stderr.rstrip().endswith('OK') and 'skipped=' not in stderr, 'SKIPPED_HOSTILE_TEST')
        return {'tests':int(match.group(1)),'skips':0}
    result = V.parse(stdout)
    V.require(result.get('terminal')==TERMINALS[ident], 'UNEXPECTED_CHECK_TERMINAL',ident)
    if ident=='SPINE':
        V.require(result['tasks']==231 and result['accepted_tasks']==0, 'SPINE_DENOMINATOR')
        return result
    if ident=='TRACE_PARENT':
        V.require(result['denominators']=={'registered_classes':3,'registered_worlds':2048,'planted_classes':3,'planted_worlds':648,'mutations_planted':4},'TRACE_DENOMINATOR')
        return {'terminal':result['terminal'],'denominators':result['denominators']}
    if ident=='REPRESENTATION':
        V.require(result['denominators']=={'partitions_enumerated':8483,'query_orders':6,'planted_failures':4,'mutations':4},'LATTICE_DENOMINATOR')
        return {'terminal':result['terminal'],'denominators':result['denominators']}
    if ident=='COMPILER_CORRECTION':
        V.require(result['directional_program_checks']==512 and result['registered_target_lengths']==128,'COMPILER_DENOMINATOR')
        V.require(result['absolute_bound_zero_overhead_violations']==126,'MISSING_F4_REFUTATION')
        V.require(result['changed_output_mutant_caught'] is True and result['unearned_runtime_factor_mutant_caught'] is True,'MISSING_COMPILER_HOSTILE')
        return result
    c = result['checks']
    V.require(c['S3_revocation_completeness']['liveness_checks']==2688 and c['S3_revocation_completeness']['mismatches']==0,'SUBSTRATE_DENOMINATOR')
    V.require(result['controls']['mutations']['detected']==result['controls']['mutations']['planted'] and result['controls']['mutations']['planted']>0,'MISSING_SUBSTRATE_HOSTILE')
    return {'terminal':result['terminal'],'S3_denominator':2688,'S3_mismatches':0,'mutations':result['controls']['mutations'],'authority':result['authority']}

def run(output=None, require_proof=False):
    rows = []
    initial = V.sha(V.read(HERE,'SOURCE_SNAPSHOT_V1.json'))
    blocked = False
    with tempfile.TemporaryDirectory(prefix='ocm-spine-pycache-') as pycache:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPYCACHEPREFIX=pycache)
        for ident, args in COMMANDS.items():
            start = time.monotonic()
            row = {'check_id':ident,'required':True,'command':[sys.executable,'-E','-B','-X',f'pycache_prefix={pycache}',*args],
                   'previous_hash':rows[-1]['receipt_hash'] if rows else initial}
            if blocked:
                row.update(status='SKIPPED',reason='Required predecessor validation failed or could not run.',exit_code=None)
            else:
                try:
                    proc = subprocess.run([sys.executable,'-E','-B','-X',f'pycache_prefix={pycache}',*args],cwd=ROOT,env=env,text=True,
                                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
                    row.update(status=classify(proc.returncode),exit_code=proc.returncode,
                               stdout_sha256=V.sha(proc.stdout.encode()),stderr_sha256=V.sha(proc.stderr.encode()))
                    if row['status']=='PASS':
                        row['result']=check_output(ident,proc.stdout,proc.stderr)
                    else:
                        row['reason']=(proc.stdout+'\n'+proc.stderr)[-4000:]
                except V.Defect as exc:
                    row.update(status='FAIL',reason=str(exc))
                except (OSError,subprocess.TimeoutExpired) as exc:
                    row.update(status='CANNOT_CHECK',reason=str(exc),exit_code=None)
                blocked = row['status']!='PASS'
            row['elapsed_seconds']=round(time.monotonic()-start,3)
            row['receipt_hash']=V.sha(V.canonical(row)); rows.append(row)
    proof = {'check_id':'PROOF_ASSISTANT','required':require_proof,'status':'CANNOT_CHECK',
             'reason':'No proof-assistant statement/toolchain/dependency identity is registered in this spine checkpoint. Other mechanization lanes are separate evidence.',
             'exit_code':None,'previous_hash':rows[-1]['receipt_hash']}
    proof['receipt_hash']=V.sha(V.canonical(proof)); rows.append(proof)
    required = [x for x in rows if x['required']]
    code = 1 if any(x['status']=='FAIL' for x in required) else 2 if any(x['status']!='PASS' for x in required) else 0
    engineering_scope=None
    if rows[0]['status']=='PASS':
        backlog=V.load(HERE,'OCM_EXECUTION_BACKLOG_V1.json')
        by_id={t['task_id']:t for t in backlog['tasks']}
        task_ids=[f'OM-WP0-{n:03d}' for n in range(1,10)]
        engineering_scope={'task_ids':task_ids,'task_identity_sha256':{x:V.task_identity(by_id[x]) for x in task_ids},'source_body_sha256':backlog['source_body_sha256'],'checkpoint_phase':'PRE_ACCEPTANCE'}
    result = {'engineering_scope':engineering_scope,'schema':'OCM_PROGRAMME_VERIFIER_RUN_V1','terminal':'PASS_REQUIRED_ENGINEERING_CHECKS' if code==0 else 'FAIL' if code==1 else 'CANNOT_CHECK',
              'required_checks':len(required),'required_passes':sum(x['status']=='PASS' for x in required),
              'all_checks_pass':all(x['status']=='PASS' for x in rows),
              'rows':rows,'source_snapshot_sha256':initial,'final_receipt_hash':rows[-1]['receipt_hash'],
              'scientific_admission':False,'independent_review_satisfied':False,'protected_outcomes_accessed':False}
    raw = json.dumps(result,sort_keys=True,indent=2)+'\n'
    if output:
        with Path(output).open('x',encoding='utf-8') as stream:
            stream.write(raw)
    print(raw,end='')
    return code

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--require-proof',action='store_true')
    args=parser.parse_args(argv)
    try:
        return run(args.output,args.require_proof)
    except (OSError,V.CannotCheck) as exc:
        print(json.dumps({'terminal':'CANNOT_CHECK','reason':str(exc)})); return 2

if __name__=='__main__':
    raise SystemExit(main())
