# Native PowerPC CI integration

The source baseline's native acceptance entrypoint is `sh tools/native-ppc-darwin10-smoke.sh`, executed on an owned Mac running Darwin 10 with an installed PowerPC-capable Xcode toolchain.

The script checks the actual host, compiles a 32-bit PPC Mach-O executable, checks its architecture and header, and executes it. It writes only into `SLPPC_WORKDIR` (default: `$HOME/slppc-native-qualification`); the caller manages cleanup.

GitHub's stock Actions runner and `actions/checkout` must **not** be assumed to execute on Mac OS X 10.6. Connect the physical Macs through a compatible, independently verified controller/transport and publish authenticated results back to GitHub. Do not label a job `self-hosted` on a physical Mac until the runner implementation is proven to support Darwin 10.

The 11-machine fleet requires individual machine inventory, OS/SDK/toolchain qualification, authentication, isolation and result provenance before automatic dispatch. No secrets or machine identifiers are embedded here.
