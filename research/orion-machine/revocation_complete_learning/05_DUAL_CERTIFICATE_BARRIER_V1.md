# RCL dual-certificate barrier V1

**Date:** 2026-09-03  
**Umbrella:** ORION-V2 #194  
**Execution:** ORION-V2 #197  
**Review:** ORION-V2 #245  
**PR:** ORION-V2 #244  
**Status:** `HAND_PROVED_CONDITIONAL_BARRIER2__NOVELTY_NOT_CLAIMED_

## 1. Motivation

An exact revocation-aware learner must sometimes decide two logically different statements:

- **retain*:** at least one surviving warrant exists;
- **retract:** no valid warrant survives.

The first statement is naturally witnessed by one surviving warrant. The second is a universal negative: every candidate warrant fails. For general proof-carrying learning this creates a barrier to expecting short, noninteractive, polynomially checkable certificates for both decisions.

## 2. Formal setting

Let `c` encode a learned skill, its current state, and an admitted intervention. Let `W(works,c)$ be a polynomial-time verifier relation. The **surviving-warrant language** is


[
\mathcal L = {c: \exists w\, V(c,
_