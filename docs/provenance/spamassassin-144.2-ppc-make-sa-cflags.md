# SpamAssassin-144.2: pass PowerPC CFLAGS through the default recipe

## Source pins

- Apple's Mac OS X 10.6.8 release manifest names `SpamAssassin-144.2`. The [official Apple tag](https://github.com/apple-oss-distributions/SpamAssassin/tree/SpamAssassin-144.2) resolves to commit `a1ed711b62e1d86311408f211fe5c5ab49deadd7`. Its `Makefile` Git blob is `ec88be5ca8d7d03bf8eb839c4eb30d0dfa0a78b9`, identical to both the untouched `src/releases/10.6.8/SpamAssassin-144.2/Makefile` and the initial PowerPC working file.
- Apple's 10.5.8 release manifest names the PowerPC-era [SpamAssassin-137.1 tag](https://github.com/apple-oss-distributions/SpamAssassin/tree/SpamAssassin-137.1), commit `8d19ed3b828b5571f7d51e91799fe91b5289bc9e`. Its `Makefile` blob `2ccb0620814a8bd7cb53d8d5d96a2d9fc89e3d22` has the same malformed `make_sa` line. The official tag comparison lists no changes in `SpamAssassin/spamc/` between these two releases.
- The bundled SpamAssassin `LICENSE` and Apple's `SpamAssassin.OpenSourceInfo/SpamAssassin.plist` identify Apache License 2.0. Existing notices and source attribution are retained.

## Defect and correction

The wrapper's default target invokes `make_sa`. That recipe passes `CFLAGS="$(CFLAGS))` to its inner command, leaving the shell double quote open. After make variable expansion, the command cannot be tokenized by `/bin/sh`; it never reaches the native `spamc` build. The separate `make_sa_install` recipe already uses `CFLAGS="$(CFLAGS)"`, showing the intended quoting. This inherited defect is architecture independent, but it blocks the default recipe when restoring the 10.6.8 component with PowerPC `RC_CFLAGS`, such as `-arch ppc` or `-arch ppc64`.

The working-tree correction adds the missing closing quote in `src/powerpc/SpamAssassin-144.2/Makefile`. The exact one-line delta is `patches/SpamAssassin-144.2-ppc-make-sa-cflags.patch`. No other recipe, upstream release snapshot, dependency project, or owned architecture record changes.

## Source-only verification and limits

`python3 -m unittest discover -s tests -p 'test_spamassassin_ppc_make_sa.py' -v` reads source text, pins the pristine Git blob, checks that the patch exactly equals the working-versus-release diff, confirms the original quote defect, and tokenizes the corrected command with `ppc` and `ppc64` flags using Python `shlex`. It does not execute a shell or build tool. No compilation, linking, installation, or PowerPC runtime test was performed; the native `spamc` and Perl dependency closure remain unverified.
