"""Verify local receipt bytes and claim-DAG consistency; NOT scientific authority."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from zipfile import ZipFile, BadZipFile

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def main():
    try:
        receipt = json.loads((BASE/'RECEIPT.json').read_text())
        claims = json.loads((BASE/'CLAIMS.json').read_text())
        verified = 0
        for name, expected in receipt['package_sha256'].items():
            path = Path(name)
            require(not path.is_absolute() and '..' not in path.parts, 'unscoped receipt path')
            require(sha256((BASE/path).read_bytes()).hexdigest() == expected, 'byte drift: '+name)
            verified += 1
        workflow = ROOT/'.github/workflows/me-certificate-transport.yml'
        require(sha256(workflow.read_bytes()).hexdigest() == receipt['workflow_sha256'], 'workflow drift')
        with ZipFile(BASE/'VERIFICATION_LOGS.zip') as archive:
            for record in receipt['commands']:
                require(sha256(archive.read(record['log'])).hexdigest() == record['log_sha256'], 'log drift')
        rows = {r['id']: r for r in claims['claims']}
        require(len(rows) == len(claims['claims']) and bool(rows), 'empty or duplicate claim ids')
        seen = set()
        def visit(key, active):
            require(key in rows, 'unknown claim dependency: '+key)
            require(key not in active, 'claim dependency cycle')
            if key in seen:
                return
            for dep in rows[key]['depends_on']:
                visit(dep, active|{key})
            seen.add(key)
        for key, row in rows.items():
            visit(key, set())
            require((BASE/row['proof_file']).is_file(), 'missing proof file')
            require(row['independent_review'] == 'NOT_OBTAINED', 'unearned review state')
            require(row['OCM_adoption'] == 'NOT_IMPLEMENTED', 'unearned OCM adoption')
            require(row['novelty'] == 'NOT_ESTABLISHED', 'unearned novelty state')
        for name, result in receipt['results'].items():
            require(json.loads((BASE/name).read_text())['counts'] == result['counts'], 'result count drift')
        print(json.dumps({'status':'LOCAL_BINDINGS_AND_CLAIM_DAG_MATCH',
                          'files':verified, 'claims':len(rows),
                          'independent_review':False, 'scientific_authority':False},sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, BadZipFile) as exc:
        print(json.dumps({'status':'CANNOT_CHECK','reason':str(exc)})); return 2
    except AssertionError as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)})); return 1


if __name__ == '__main__':
    sys.exit(main())
