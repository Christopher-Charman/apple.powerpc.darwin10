# RubyGems-17.1: match PowerPC and universal gems on Darwin 10

## Source pins

- Apple's [RubyGems-17.1 release](https://github.com/apple-oss-distributions/RubyGems/tree/RubyGems-17.1) resolves to commit `b0272b85f2c2f73cd56e6b63d994741f8034b688` and tree `e0ef979c20ab2d3e873fce93f42e0abd0158ffc2`. Both the pristine `src/releases/10.6.8/RubyGems-17.1/` and the initial working `src/powerpc/RubyGems-17.1/` have that tree ID. The original [platform.rb](https://github.com/apple-oss-distributions/RubyGems/blob/RubyGems-17.1/rubygems/lib/rubygems/platform.rb) is Git blob `bfa8fca0ffaa46189b0ba7e493c4e8c49117541b`.
- Apple's PPC-era [RubyGems-15.2 predecessor](https://github.com/apple-oss-distributions/RubyGems/tree/RubyGems-15.2) resolves to commit `7e49d988487e05d529cabd75ef92d31c1cdb2081`, tree `3efa6fa49bf31149d9a21583837be37b5ba89f6c`, and [platform.rb](https://github.com/apple-oss-distributions/RubyGems/blob/RubyGems-15.2/rubygems/lib/rubygems/platform.rb) blob `7abc15ef94289b5682fab63feb50ec3572f2ad39`. It supports PowerPC Darwin 7/8 and universal gems, but its legacy string matchers also capture just one Darwin version digit.

## Defect and correction

`Gem::Platform.new('powerpc-darwin10.0')` parses the local OS version as `10`. The legacy `=~` conversion of a gem's `powerpc-darwin10.0` or `universal-darwin10.0` platform string captured only `1`, so `Gem::Platform.match` rejected a same-version PowerPC or universal binary gem. A source-script probe against the unmodified Apple file reproduced `Gem::Platform.match('powerpc-darwin10.0') == false` for a PowerPC Darwin 10 local platform. The existing Apple tests exercise Darwin 7–9, leaving this transition uncovered.

The working source now captures all consecutive digits in the PowerPC and universal legacy Darwin string matchers. This preserves the existing Darwin 7/8 cases, unversioned PowerPC strings, CPU matching, and rejection of gems for other Darwin major versions. The exact two-line delta is `patches/RubyGems-17.1-ppc-darwin10-platform.patch`. The official release snapshot and bundled `rubygems-1.3.5.tgz` remain unchanged.

## Verification and limits

`python3 -m unittest discover -s tests -p 'test_rubygems_ppc_platform.py' -v` checks the original Apple blob, exact patch, and platform behavior by loading only the historical Ruby platform source with gems disabled. The dedicated CI workflow runs only that source-script test. No compile, link, build, gem setup, extension build, image integration, or PowerPC hardware validation was performed.
