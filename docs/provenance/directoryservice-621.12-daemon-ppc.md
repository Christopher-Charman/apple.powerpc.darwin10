# DirectoryService-621.12 daemon PPC architecture restoration

Official Apple 10.6.8 DirectoryService project: its daemon target excludes PPC from `VALID_ARCHS` in Development, Deployment and Default configurations; Development and Deployment also explicitly restrict `ARCHS` to Intel. This patch adds PPC to the valid architecture lists and enables PPC in each daemon configuration, leaving other targets and pristine source untouched. This is source-only architecture eligibility; actual PPC API, ABI and runtime behavior remain unverified. No compilation on PowerPC-Darwin.org.
