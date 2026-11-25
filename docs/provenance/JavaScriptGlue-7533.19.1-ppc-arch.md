# JavaScriptGlue 7533.19.1: restore PPC selection for 10.6 development configurations

The working `src/powerpc/JavaScriptGlue-7533.19.1` tree matched both the pristine
`src/releases/10.6.8/JavaScriptGlue-7533.19.1` tree and Apple's official
[`JavaScriptGlue-7533.19.1`](https://github.com/apple-oss-distributions/JavaScriptGlue/tree/JavaScriptGlue-7533.19.1)
tag before this change. All three Git tree IDs were
`377a8446cee07031cf4b72b032392530a9b0fdbd`; the Apple tag commit is
`f90d9bbd34f4a880ac12eae830edd1be2a6e5872`. The repository's
`source-releases/10.6.8.json` names this exact tag.

The 10.5.8 release record names Apple's PPC-era
[`JavaScriptGlue-5530.19`](https://github.com/apple-oss-distributions/JavaScriptGlue/tree/JavaScriptGlue-5530.19)
tag (`e3ebb8d2202d93ee40ebe7cff5756e893c847fa5`). Its configuration
allows `ppc` in `VALID_ARCHS` and uses the native architecture for 10.5.
The 10.6.8 source still allows `ppc` in `VALID_ARCHS`, has PPC-specific
warning settings, and otherwise uses architecture-neutral glue code, but
its Debug/Release `ARCHS_1060` expands only `ARCHS_STANDARD_32_64_BIT`.
That setting does not explicitly select `ppc` for the 10.6 development
configurations.

The working-source correction adds `ppc` to that setting while retaining
the existing standard architecture expansion. It follows the repository's
`CoreOSMakefiles-63-ppc-xcode-arch.patch` convention and leaves the
10.7 architecture setting untouched. The exact one-line release delta is
`patches/JavaScriptGlue-7533.19.1-ppc-arch.patch`. The pristine release
tree remains unchanged. Paired JavaScriptCore release source is
`JavaScriptCore-7533.20.20`; this setting alone does not establish that
dependency's PPC compatibility.

Source-only regression: `python3 -m unittest discover -s tests -p
"test_javascriptglue_ppc_arch.py" -v` compares working bytes against the
exact pristine replacement and checks 10.6 selection, deployment target,
and `VALID_ARCHS`. No compilation, linking, build, or runtime check was run.
