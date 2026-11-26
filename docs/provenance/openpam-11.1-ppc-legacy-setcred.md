# OpenPAM-11.1: preserve legacy credential flags for PowerPC clients

## Source pins

- Target: Apple's Mac OS X 10.6.8 release manifest names `OpenPAM-11.1`. The official [Apple OpenPAM-11.1 tree](https://github.com/apple-oss-distributions/OpenPAM/tree/OpenPAM-11.1) is `11a88f164bbb8aa9e07a26f9fd02fede77d0da9d`. The pristine `src/releases/10.6.8/OpenPAM-11.1/` and initial `src/powerpc/OpenPAM-11.1/` trees both have that exact Git tree ID.
- PPC-era predecessor: Apple's [pam-31 header](https://github.com/apple-oss-distributions/pam/blob/83bcd51b6122e467815175b28277ee38ffc28c78/pam/libpam/include/pam/_pam_types.h) defines `PAM_SILENT=0x8000`, `PAM_ESTABLISH_CRED=0x0002`, `PAM_DELETE_CRED=0x0004`, `PAM_REINITIALIZE_CRED=0x0008`, and `PAM_REFRESH_CRED=0x0010`. The Mac OS X 10.5 SDK header retains these values for Leopard applications, including PowerPC applications. Apple's [OpenPAM-11 predecessor](https://github.com/apple-oss-distributions/OpenPAM/blob/b75124d42c9e3eb7cfffef1ffd078d5fbb8350ab/compat/pam_shim.c) has the same shim mistake; the 10.6.0 release manifest names `OpenPAM-11`.
- Destination: [OpenPAM-11.1 `pam_constants.h`](https://github.com/apple-oss-distributions/OpenPAM/blob/OpenPAM-11.1/openpam/include/security/pam_constants.h) defines the corresponding credential bits as `0x1`, `0x2`, `0x4`, `0x8`, with `PAM_SILENT` as the high bit. [OpenPAM-11.1 `pam_setcred.c`](https://github.com/apple-oss-distributions/OpenPAM/blob/OpenPAM-11.1/openpam/lib/pam_setcred.c) accepts those credential flags.

## Defect and correction

The `libpam.1.dylib` compatibility shim serves legacy PAM callers through `libpam.2.dylib`. Its `pam_setcred()` used the authentication flag translator. That translator ignores the predecessor's credential bits, so all four credential operations reach the destination as zero. It also interprets the legacy authentication bit `0x0001` as `PAM_DISALLOW_NULL_AUTHTOK`, which happens to alias the destination's `PAM_ESTABLISH_CRED` bit. This is a source contract failure for retained PowerPC Leopard clients, independent of the machine's endian order or pointer width.

The working-tree correction calls the existing credential translator, gives its generated legacy constants a distinct `COMPAT_SETCRED_` prefix, and adds `PAM_SILENT` to that translator. The exact two-file delta is `patches/OpenPAM-11.1-ppc-legacy-setcred-flags.patch`. The official release snapshot is unchanged. Existing copyright and license text is retained.

## Verification and limits

`python3 -m unittest discover -s tests -p 'test_openpam_ppc_legacy_setcred.py' -v` is a source-only regression test. It pins both pristine Git blobs, checks the exact patch against the working source, verifies the shim calls the credential translator and its flag mapping, and checks a combined silent plus delete-credentials case. No compile, link, build, image integration, or G4/G5 runtime test was performed. The fix does not claim that other legacy shim signatures or PAM modules are validated.
