# OpenBSM-21 `amt` PPC Release architecture

## Source identity

- Exact first-party Mac OS X 10.6.8 release member: `OpenBSM-21`, upstream Apple OSS tag object `8aa211264493555c1f8e622270b93b1d7062f5e6`, commit `bb0681420e99d447f466ba70d38589213bb69fea` in `apple-oss-distributions/OpenBSM`.
- Immutable comparison input: `src/releases/10.6.8/OpenBSM-21/`, Git tree `0c3f892cf930b4d536682ed516e64eb3835bcb4d`.
- License: Apple Public Source License 2.0 with Apple OS reference restrictions, retained in the `amt` source headers. No donor code was copied.

## Reason and exact edit

The `amt` Abstract Machine Test utility tests whether privileged instructions fault outside supervisor mode. Its `amt/priv_inst.c` already contains `__ppc__` and `__ppc64__` test definitions for `mfmsr`, `tlbsync` and privileged SPR reads, and `amt.8` says the instruction set is architecture dependent. The Release configuration of the `amt` target nevertheless limits `VALID_ARCHS` to `armv6 i386 x86_64`, preventing its PPC source from being selected. This working-tree edit adds `ppc` and `ppc64` to that single target setting. No other OpenBSM target or pristine release file changes. The exact source diff is `patches/OpenBSM-21-amt-ppc.patch`.

`amt` links against the project `libbsm.0` product and reports to `auditd`; the XNU audit interface, generated headers and target runtime remain dependency and validation work. The pre-edit working project file exactly matched the immutable 10.6.8 release copy. The target mapping, PPC source guards and architecture assignment were checked through authenticated GitHub API. This is source-only evidence; no PPC build, privileged-instruction run or hardware validation was performed on this host.
