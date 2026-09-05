"""Source-bound research rule resolution, never an adoption or truth authority.

New imports must select an exact rule with its scope. Historical MEG/primitive
status labels are deliberately not accepted as selections. Standard library only.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

PACKAGE = Path('research/machine-epistemics-theory/authority_reconciliation_v1')
SNAPSHOT = '096e6f3df1854dede3c8a0fbe63d05ec30bcb119'
MANIFEST_SHA256 = 'b85e2c633f96e0bf89fa757b5a8e9baf837bd181c17a5eb157e55c53febfad07'
OVERLAY_SHA256 = 'e62b640b8436c68cf4f6264c3448febcfeb198201890f3f479f7eeb8e1e15f2d'
ATLAS_IDS = {f'MEG-{i:02d}' for i in range(1, 37)}
PRIMITIVE_IDS = {f'FND-P{i:02d}' for i in range(1, 21)}
ROW_STATUSES = {'SCOPED_FRAGMENT_WITH_OPEN_BOUNDARY', 'OPEN', 'CANNOT_CHECK'}
HISTORICAL_STATUSES = {'PROVED', 'ADOPTED', 'PARENT_OWNED', 'FINITE_CALIBRATION',
                       'OPEN', 'CANNOT_CHECK', 'PROPOSED_PENDING_PR'}


class CannotCheck(ValueError):
    """Incomplete, unbound, drifted or inadmissible research metadata."""


def require(condition, reason):
    if not condition:
        raise CannotCheck(reason)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys), f'{label}: fields/type')


def nonempty(value):
    return type(value) is str and bool(value.strip())


def unique(items, label):
    require(type(items) is list, f'{label}: list required')
    ids = []
    for item in items:
        require(type(item) is dict and nonempty(item.get('id')), f'{label}: id')
        ids.append(item['id'])
    require(len(ids) == len(set(ids)), f'{label}: duplicate id')
    return set(ids)


def regular(root, relative):
    """Allow a checkout beneath a symlink; refuse symlinks inside that checkout."""
    require(type(relative) is str and bool(relative), 'path: string required')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and relative == path.as_posix()
            and '..' not in path.parts and '.' not in path.parts, 'path: noncanonical')
    current = Path(root).resolve()
    for component in path.parts:
        current /= component
        require(not current.is_symlink(), f'path: symlink {relative}')
    require(current.is_file(), f'path: absent/nonregular {relative}')
    return current


def read_json(data):
    def pairs(entries):
        out = {}
        for key, value in entries:
            require(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(CannotCheck('nonfinite JSON')))
    except (ValueError, TypeError, UnicodeError) as exc:
        raise CannotCheck(f'JSON: {exc}') from exc


def _validate_overlay(data, manifest, source_bytes):
    """Strict structure plus exact correspondence to pinned historical records.

    This function is not the public trust boundary: load() additionally verifies
    the reviewed catalogue seal and Git source identities before returning it.
    """
    exact_keys(data, {'schema', 'snapshot_commit', 'source_manifest_sha256', 'terminal',
                     'historical_registry_policy', 'new_import_policy', 'scientific_completion',
                     'independent_external_review', 'rows', 'rules', 'corrections'}, 'overlay')
    require(data['schema'] == 'ME_EFFECTIVE_AUTHORITY_V1' and data['snapshot_commit'] == SNAPSHOT,
            'overlay identity')
    require(data['source_manifest_sha256'] == MANIFEST_SHA256, 'manifest identity')
    require(data['terminal'] == 'INTERNAL_SPECIFICATION_CANDIDATE', 'unknown/promoted terminal')
    require(data['scientific_completion'] is False and data['independent_external_review'] == 'NOT_OBTAINED',
            'external/programme promotion')
    require(data['historical_registry_policy'] == 'IMMUTABLE_SOURCE_RECORDS_NOT_STANDALONE_AUTHORITY'
            and data['new_import_policy'] == 'MANDATORY_NAMED_RULE_RESOLUTION_THEN_INDEPENDENT_PARITY_AND_EXTERNAL_ADOPTION',
            'consumer policy weakened')
    require(unique(data['rows'], 'rows') == ATLAS_IDS | PRIMITIVE_IDS, '56-row totality')
    require(unique(data['rules'], 'rules') == {x + ':SCOPED_FRAGMENT_V1' for x in ATLAS_IDS}, 'rule totality')
    correction_ids = unique(data['corrections'], 'corrections')
    require(len(correction_ids) == 18, 'correction coverage')
    sources = {item['path'] for item in manifest['files']}
    prefix = 'research/machine-epistemics-theory/'
    original = read_json(source_bytes[prefix + 'MACHINE_EPISTEMICS_FOUNDATION_V1.json'])
    original_rows = {**original['atlas'], **{x['id']: x for x in original['primitives']}}
    for row in data['rows']:
        exact_keys(row, {'id', 'kind', 'effective_status', 'terminal', 'candidate_rules',
                         'historical_records', 'atlas_entries', 'current_boundary', 'remaining_scope_policy'}, 'row')
        require(row['kind'] == ('ATLAS' if row['id'] in ATLAS_IDS else 'PRIMITIVE'), 'row kind')
        require(row['effective_status'] in ROW_STATUSES and row['terminal'] == 'NO_ROW_LEVEL_AUTHORITY', 'row status/terminal')
        require(type(row['atlas_entries']) is list, 'atlas entries type')
        require(row['historical_records'].get('canonical') == original_rows[row['id']], 'rewritten historical row')
        require(row['historical_records']['canonical']['status'] in HISTORICAL_STATUSES, 'historical status')
        require(type(row['candidate_rules']) is list and len(row['candidate_rules']) == len(set(row['candidate_rules'])), 'candidate list')
        require(all(r in {x + ':SCOPED_FRAGMENT_V1' for x in ATLAS_IDS} for r in row['candidate_rules']), 'unknown candidate')
        if row['effective_status'] in {'OPEN', 'CANNOT_CHECK'}:
            require(row['candidate_rules'] == [], 'open row minted authority')
        require(nonempty(row['current_boundary']) and nonempty(row['remaining_scope_policy']), 'row scope missing')
    for rule in data['rules']:
        exact_keys(rule, {'id', 'atlas_id', 'status', 'terminal', 'statement', 'scope', 'parent', 'checker',
                          'resources', 'excluded_claims', 'scientific_truth_authorized',
                          'ocm_adoption_authorized', 'independent_external_review', 'rule_sha256'}, 'rule')
        require(rule['id'] == rule['atlas_id'] + ':SCOPED_FRAGMENT_V1' and rule['atlas_id'] in ATLAS_IDS, 'rule atlas mismatch')
        require(rule['status'] == 'SCOPED_REFERENCE_FRAGMENT' and rule['terminal'] == 'PARITY_AND_EXTERNAL_ADOPTION_REQUIRED', 'rule status/terminal')
        require(rule['scientific_truth_authorized'] is False and rule['ocm_adoption_authorized'] is False
                and rule['independent_external_review'] == 'NOT_OBTAINED', 'rule authority promotion')
        require(all(nonempty(rule[field]) for field in ['scope', 'parent', 'resources']), 'rule premise missing')
        validate_reference(rule['statement'], sources, source_bytes, bounded_section=True)
        exact_keys(rule['checker'], {'path', 'scope'}, 'checker')
        require(rule['checker']['path'] in sources and rule['checker']['scope'] == 'PACKAGE_FINITE_CALIBRATION_ONLY_NOT_AN_ALL_SIZE_PROOF_OR_EXTERNAL_REVIEW', 'checker identity/scope')
        require(type(rule['excluded_claims']) is list and len(set(rule['excluded_claims'])) == len(rule['excluded_claims'])
                and set(rule['excluded_claims']) <= correction_ids, 'exclusion mismatch')
        payload = {k: v for k, v in rule.items() if k != 'rule_sha256'}
        require(rule['rule_sha256'] == sha256(canonical(payload)), 'rule semantic identity mismatch')
    for correction in data['corrections']:
        exact_keys(correction, {'id', 'atlas_id', 'disposition', 'authority', 'source', 'reason'}, 'correction')
        require(correction['atlas_id'] in ATLAS_IDS and correction['authority'] == 'NONE', 'correction authority')
        require(correction['disposition'] in {'REFUTED', 'UNSUPPORTED_EXTENSION'}, 'correction status')
        require(nonempty(correction['reason']), 'correction reason')
        validate_reference(correction['source'], sources, source_bytes)
        rule = next(r for r in data['rules'] if r['atlas_id'] == correction['atlas_id'])
        require(correction['id'] in rule['excluded_claims'], 'correction omitted from effective rule')
    return {'rows': len(data['rows']), 'rules': len(data['rules']), 'corrections': len(data['corrections'])}


def validate_overlay(data, manifest, source_bytes):
    try:
        return _validate_overlay(data, manifest, source_bytes)
    except CannotCheck:
        raise
    except (TypeError, KeyError, AttributeError, UnicodeError, ValueError) as exc:
        raise CannotCheck(f'malformed overlay: {exc}') from exc


def validate_reference(reference, sources, source_bytes, bounded_section=False):
    keys = {'path', 'clause', 'section_sha256'} if bounded_section else {'path', 'clause'}
    exact_keys(reference, keys, 'clause reference')
    require(reference['path'] in sources and nonempty(reference['clause']), 'unbound clause reference')
    text = source_bytes[reference['path']].decode('utf-8')
    require(reference['clause'] in text, 'clause absent from source')
    if bounded_section:
        require(reference['section_sha256'] == sha256(clause_section(text, reference['clause'])), 'clause section identity drift')


def clause_section(text, marker):
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if re.match(r'^#{1,6} ', line)
            and re.search(r'(?<![A-Za-z0-9])' + re.escape(marker) + r'(?![A-Za-z0-9])', line)]
    require(len(hits) == 1, 'ambiguous/missing clause heading')
    start = hits[0]
    level = len(lines[start]) - len(lines[start].lstrip('#'))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r'^#{1,6} ', lines[i]) and len(lines[i]) - len(lines[i].lstrip('#')) <= level:
            end = i
            break
    return ''.join(lines[start:end]).encode()


def load(root):
    root = Path(root).resolve()
    manifest_bytes = regular(root, (PACKAGE / 'SOURCES_V1.json').as_posix()).read_bytes()
    require(sha256(manifest_bytes) == MANIFEST_SHA256, 'source inventory seal drift')
    manifest = read_json(manifest_bytes)
    exact_keys(manifest, {'schema', 'repository', 'snapshot_commit', 'files'}, 'manifest')
    require(manifest['schema'] == 'ME_AUTHORITY_SOURCES_V1'
            and manifest['repository'] == 'SzeChunYiu/ORION-V2'
            and manifest['snapshot_commit'] == SNAPSHOT, 'manifest source identity')
    require(type(manifest['files']) is list and len(manifest['files']) == 43, 'source coverage')
    source_bytes, seen = {}, set()
    for source in manifest['files']:
        exact_keys(source, {'path', 'source_commit', 'sha256', 'git_blob_sha1'}, 'source')
        require(source['path'] not in seen and source['source_commit'] == SNAPSHOT, 'duplicate/wrong source')
        seen.add(source['path'])
        data = regular(root, source['path']).read_bytes()
        require(sha256(data) == source['sha256'], f'source bytes drift: {source["path"]}')
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == source['git_blob_sha1'], 'source Git blob drift')
        try:
            recorded = subprocess.run(['git', '-C', str(root), 'cat-file', 'blob', SNAPSHOT + ':' + source['path']],
                                      check=True, capture_output=True, timeout=20).stdout
        except (OSError, subprocess.SubprocessError) as exc:
            raise CannotCheck('source Git snapshot unavailable') from exc
        require(data == recorded, 'source does not match recorded snapshot')
        source_bytes[source['path']] = data
    overlay_bytes = regular(root, (PACKAGE / 'EFFECTIVE_AUTHORITY_V1.json').as_posix()).read_bytes()
    overlay = read_json(overlay_bytes)
    validate_overlay(overlay, manifest, source_bytes)
    # An attacker/caller cannot rewrite scope and recompute its local digest.
    # A reviewed source-level successor is needed to change this trust root.
    require(sha256(overlay_bytes) == OVERLAY_SHA256, 'reviewed clause catalogue seal drift')
    return overlay


def select(root, request):
    exact_keys(request, {'schema', 'rule_id', 'rule_sha256', 'scope_sha256',
                         'source_snapshot', 'source_manifest_sha256'}, 'selection')
    require(request['schema'] == 'ME_RULE_SELECTION_V1', 'legacy registry label is not a rule selection')
    overlay = load(root)
    require(request['source_snapshot'] == SNAPSHOT and request['source_manifest_sha256'] == MANIFEST_SHA256,
            'selection snapshot drift')
    rule = next((r for r in overlay['rules'] if r['id'] == request['rule_id']), None)
    require(rule is not None, 'unknown/refuted/broad rule')
    row = next(r for r in overlay['rows'] if r['id'] == rule['atlas_id'])
    require(row['effective_status'] == 'SCOPED_FRAGMENT_WITH_OPEN_BOUNDARY'
            and rule['id'] in row['candidate_rules'], 'rule unavailable in effective row')
    require(request['rule_sha256'] == rule['rule_sha256']
            and request['scope_sha256'] == sha256(rule['scope'].encode()), 'selection scope or statement drift')
    return {'terminal': 'SCOPED_RULE_IDENTIFIED_NO_ADOPTION_AUTHORITY', 'rule': copy.deepcopy(rule),
            'source_snapshot': SNAPSHOT, 'source_manifest_sha256': MANIFEST_SHA256,
            'scientific_truth_authorized': False, 'ocm_adoption_authorized': False,
            'required_next': ['source theorem premises verified for actual subject',
                              'independently verified exact-source OCM parity',
                              'authenticated external adoption decision for that subject and epoch']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--selection', type=Path)
    args = parser.parse_args()
    try:
        if args.selection:
            result = select(args.root, read_json(args.selection.read_bytes()))
        else:
            data = load(args.root)
            result = {'terminal': 'EFFECTIVE_AUTHORITY_REGISTRY_VALID', 'rows': len(data['rows']),
                      'rules': len(data['rules']), 'corrections': len(data['corrections']),
                      'scientific_completion': False, 'ocm_adoption_authorized': False}
        print(json.dumps(result, indent=2, sort_keys=True))
    except (CannotCheck, OSError) as exc:
        print(json.dumps({'terminal': 'CANNOT_CHECK', 'reason': str(exc)}))
        raise SystemExit(2)
