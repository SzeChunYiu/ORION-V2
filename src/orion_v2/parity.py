from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class CapabilityCensusValidation:
    valid: bool; capability_count: int; errors: tuple[str,...]; terminal: str

def validate_capability_census(census: Mapping[str,Any], *, expected_count:int=59)->CapabilityCensusValidation:
    errors=[]
    if census.get('schema_version')!='orion.v2.v1-capability-census.v1': errors.append('unexpected schema_version')
    capabilities=census.get('capabilities')
    if not isinstance(capabilities,list): capabilities=[]; errors.append('capabilities must be a list')
    identities=[]
    allowed={'PRESERVE_NATIVE','PRESERVE_AS_SPECIAL_CASE','MERGE_INTO_DEEPER_OBJECT','SPLIT_BY_CONTEXT','REPLACE_WITH_PARENT_METHOD','REPLACE_WITH_DONOR_PRODUCT','GENERALIZE_WITH_NEW_COORDINATE','DEPRECATE_AFTER_PROTECTED_NONINFERIORITY','CANNOT_CHECK'}
    for index,capability in enumerate(capabilities):
        if not isinstance(capability,Mapping): errors.append(f'capability[{index}] must be an object'); continue
        capability_id=str(capability.get('capability_id','')); identities.append(capability_id)
        if not capability_id.strip(): errors.append(f'capability[{index}] lacks identity')
        if not str(capability.get('purpose','')).strip(): errors.append(f'capability {capability_id!r} lacks purpose')
        owners=capability.get('candidate_v2_owner_ids')
        if not isinstance(owners,list) or not owners or any(not str(owner).strip() for owner in owners): errors.append(f'capability {capability_id!r} lacks candidate V2 owners')
        if capability.get('disposition') not in allowed: errors.append(f'capability {capability_id!r} has invalid disposition')
    if len(identities)!=len(set(identities)): errors.append('capability identities must be unique')
    if len(capabilities)!=expected_count: errors.append(f'expected {expected_count} capabilities, observed {len(capabilities)}')
    terminal='V1_CAPABILITY_CENSUS_VALID' if not errors else 'V1_CAPABILITY_CENSUS_INVALID'
    return CapabilityCensusValidation(not errors,len(capabilities),tuple(errors),terminal)

def load_and_validate_capability_census(path:str|Path)->CapabilityCensusValidation:
    with Path(path).open('r',encoding='utf-8') as handle: census=json.load(handle)
    return validate_capability_census(census)
