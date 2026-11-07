#!/usr/bin/env python3
"""Check Darwin 9/10 source graph and reject unqualified modern source trees."""
import configparser
import subprocess
import sys
from pathlib import Path

SNOW = 'src/apple-darwin-10.6.8/'
EXPECTED = {
    'src/releases/10.5/xnu-1228.15.4': ('9d80f9528906753d682f9d65d56a0276bad56b4d', 3156),
    'src/releases/10.6/xnu-1456.1.26': ('46708ce5a6d4a42164ddb67a90fa6fbc7f986430', 3379),
    'src/releases/10.6.8/xnu-1504.15.3': ('0ffff24afe52ed47d20c5a06f07a10200f89f32b', 3386),
    'src/releases/10.6/cups-218': ('9938def0573b75abc0d2394b8a5e9ad66eca6609', 1336),
    'src/releases/10.6/libxml2-21': ('fc7b70e014720bcd2841ea820dcd796857f73380', 3786),
    'src/releases/10.6.8/cctools-750': ('fd5088e19976086ee468e14f7ac9d99aea9feb67', 434),
    'src/releases/10.6.8/ld64-95.2.12': ('6eddbd84730dc25fb0e273d21dc60b484cb2a6a1', 757),
    'src/releases/10.6.8/Libc-594.9.5': ('c577656a4766b334a0c8e0d6bc8dbd68c2bb4ae0', 2737),
    'src/releases/10.6.2/xnu-1486.2.11': ('1b4d746adf265f0459a9a3a87dcb9d483f085208', 3379),
    'src/releases/10.6.3/xnu-1504.3.12': ('c1c00d94faad04b56ded4d40e21a1724898c3e13', 3386),
    'src/releases/10.5.8/notify-16': ('bdf9bfe291059e6e8d3958b653e88d9da8728407', 24),
    'src/releases/10.6/notify-23': ('38946c7473e54cd68bbe85d8b6c907f835ba9d2c', 22),
    'src/releases/10.6.8/notify-25.1': ('11e89af8448d664497294015b8f128878b16b4de', 21),
    'src/releases/10.6/Libnotify-53': ('f403157be8da7e5a737a0d218f02683731737800', 22),
    'src/releases/10.6.8/Libnotify-54.3': ('7e626c25a337eeebdddd3a2f6640354f304b5cb6', 23),
    'src/releases/10.6/Libc-583': ('75515abbc4ece291741c3d9129eceef5a85e913e', 2732),
    'src/releases/10.6/kext_tools-177': ('0de81839fd993341ff03e412969f47ff72fa9936', 76),
    'src/releases/10.6.8/kext_tools-180.2.1': ('191e8d87a847864dde821469ffd23b10315e31c2', 77),
    'src/releases/10.6/DirectoryService-621': ('bd53241aacad6a7e39e953a02f8663508bab9ce5', 391),
    'src/releases/10.6.8/libgcc-13': ('1b8d9722b0aebee3a8f250015e147d5138219677', 2),
    'src/releases/10.6.8/libedit-13': ('13615e39a599110aad2a4306cdfa2eb58cb744b9', 69),
    'src/releases/10.6.8/expat-9': ('4eb08fafdc775ee7a6a8664ebde11252cc7622e8', 136),
    'src/releases/10.6.8/zlib-23.4': ('8629af342e92903696cb2748281e70dff1905f93', 212),
    'src/releases/10.6.8/DiskArbitration-213.1': ('4fa11ca41624e9a00a2eacabd428144a62945fa5', 66),
    'src/releases/10.6.8/IOKitUser-514.16.50': ('94160a3426312298b83cf11c1715299891e5a70b', 157),
    'src/releases/10.6.8/OpenSSL098-35.1': ('a7a892ee95c12b5d59c947b759fb283982206c97', 2159),
    'src/releases/10.6.8/CF-550.43': ('979bfb3871fa956cb8b537eda1bea777a663a90c', 145),
    'src/releases/10.6.8/graphviz-1009': ('3594d6513e353e9cadadb3f2853a53715bccf4dc', 1360),
    'src/releases/10.6.8/libiconv-30': ('c472d4048e963885829046356260b0fabdbec717', 789),
    'src/releases/10.6.8/ncurses-27': ('264f40283fb785d408b110bc141907867411eec4', 1042),
    'src/releases/10.6.8/dyld-132.13': ('24bbd98dada6742b194fbf0b9f236ce93e80ee69', 729),
    'src/releases/10.6.8/launchd-329.3.3': ('de2e1307a0fea7673db994b2b417caad86d2fe33', 82),
    'src/releases/10.6.8/bootstrap_cmds-72': ('dc3e678ebd2950cbced29edbb5a0d544a6c42908', 103),
    'src/releases/10.6.8/system_cmds-498.2': ('6a688063697971a76ec548a7d898d66bba6f5499', 230),
    'src/releases/10.6.8/configd-293.8': ('4464e775e1623031a5a749ec1c93a35b9907d32e', 245),
    'src/releases/10.6.8/CoreOSMakefiles-63': ('b8bd3ab03845f06d71fdd70a330dcc6baddf9d93', 31),
    'src/releases/10.6.8/IOHIDFamily-315.7.16': ('981b406e576b1714b94946b18942143ae94fc220', 164),
    'src/releases/10.6.8/IOStorageFamily-116.1.41': ('c04a62175aea17a0c46a086ab91fa3e8aeab4cc5', 31),
    'src/releases/10.6.8/libdispatch-84.5.5': ('c5b42ddb7f3106cd0cdb7a4a664e5603f1e7cbd2', 125),
    'src/releases/10.6.8/Apple16X50Serial-24': ('cb17e868b0af18e8986e100969b7c0ab65ee5198', 18),
    'src/releases/10.6.8/AppleAPIC-13': ('688a10d09241cc76890c7b1a3b3920e954098004', 6),
    'src/releases/10.6.8/AppleFileSystemDriver-13': ('e740bf3ee6bf3f3945d1bddd55f199be89de55f8', 6),
    'src/releases/10.6.8/AppleHWSensor-193': ('f21d8ab6d204b6df1beefdeb10b1090ab279bb10', 54),
    'src/releases/10.6.8/AppleRAID-4.0.6': ('d5355694430c699c3ef09429917ab3c628330602', 33),
    'src/releases/10.6.8/AppleRTL8139Ethernet-153': ('bb467d1ca8fe283974a678f9afe08703adcb6020', 18),
    'src/releases/10.6.8/AppleTalk-95': ('adc95709a08ed425d0a4bbe1643f3b583e2fc8e9', 38),
    'src/releases/10.6.8/AppleUSBCDCDriver-4005.4.2': ('7e3465bf5d0300d5e0d8e4716abd95bc2014eb90', 43),
    'src/releases/10.6.8/IOGraphics-392.1': ('ed07eb1e310d0f0a2ac01946619e0590e37ce60d', 73),
    'src/releases/10.6.8/IOPCIFamily-144': ('a28234e869540fc69c14f1545a35091ee644a809', 24),
    'src/releases/10.6.8/IOFireWireFamily-426.4.1': ('26cae0d41edc63ce6cd26fd6aedc671711bf78a4', 192),
    'src/releases/10.6.8/IOUSBFamily-424.4.1': ('e32592374f0a601b680edc764cb84c1f5a845100', 296),
    'src/releases/10.6.8/IOATAFamily-251.0.1': ('c76f80368c48ada82086596f2a6972d0cbd413aa', 27),
    'src/releases/10.6.8/IOAudioFamily-183.4.2': ('703741f7622df17bb30d594ce9035d28910ee9f5', 46),
    'src/releases/10.6.8/IOACPIFamily-8': ('8c0924ee83f003e666c9d8e4d7f8c2d5d8f839d4', 9),
    'src/releases/10.6.8/IOCDStorageFamily-47.1': ('5daee20e31d6cb84e99a133295d87dfe342e314a', 18),
    'src/releases/10.6.8/IOBDStorageFamily-10': ('d28973d37ae0d69aa778bbf9f9dd0d8224c6ce90', 16),
    'src/releases/10.6.8/IOATAPIProtocolTransport-251.0.1': ('93873670cad58b6b807562ab7e1fdc43d32ae3ac', 9),
    'src/releases/10.6.8/AppleSMBIOS-42': ('abc7e08ad60efa541c67d0028cdaa1e6ef3691d7', 5),
    'src/releases/10.6.8/BootCache-64.2': ('4defb3ff35c438f4bfa1592910e410243fd50d9c', 7),
    'src/releases/10.6.8/IONetworkingFamily-65.2.1': ('2598ea2ba9141b0cf50be229f1fa739fd0c98c30', 44),
    'src/releases/10.6.8/Libcpp_kext-8': ('f2a3d7d3b443cfe055c40d4ba0f765c59ef8e046', 13),
    'src/releases/10.6.8/network_cmds-329.2.2': ('36623dbdff6963ece6defcc0e2b4e3b537f48a7e', 131),
    'src/releases/10.6.8/bootp-198.2': ('20b183edbf0fbca10cf791193f3c246d1397140b', 128),
    'src/releases/10.6.8/libsecurity_codesigning-55005': ('64c0de7cb7e940199b1529ab1b3a98aa250cdf06', 99),
    'src/releases/10.6.8/IOKitTools-78': ('c684c84aaf15faf330e18f3965376613e66bd9d7', 7),
    'src/releases/10.6.8/libclosure-38': ('431a7849ba34cd6526c332fe3fe70d544a405dcb', 164),
    'src/releases/10.6.8/libsecurity_keychain-55017': ('a58df3f1b414901c75a9569b21c6b7b15ae221bc', 159),
    'src/releases/10.6.8/libsecurity_authorization-36329': ('40f5fad125de2f87cc470f6106670bc3e7c6e8ae', 15),
    'src/releases/10.6.8/Security-55002': ('bfe629cbdcc22866ecfa3a726acd551a7608d2e1', 26),
    'src/releases/10.6.8/libsecurity_ssl-40581': ('5d6021ba0818869af8cdade05dd58e3096fe3e48', 61),
    'src/releases/10.6.8/libsecurity_cms-36064': ('51f9babd877883c1935ee7824155ec4ee27636a5', 10),
    'src/releases/10.6.8/libsecurity_utilities-55010': ('ac77b4bbcfdcf67d2401aa3fc37207806467ba42', 128),
    'src/releases/10.6.8/libsecurity_asn1-36064': ('44965932028c948b4c147af2e5fc53ba045597d8', 89),
    'src/releases/10.6.8/libsecurity_cssm-40418': ('f91e7e4c293d1639899da8d8a2d540730f4434cb', 61),
    'src/releases/10.6.8/libsecurity_cdsa_client-36213': ('dd1b05fa9f83e2e78a6f3543aabbe9fc6addb383', 45),
    'src/releases/10.6.8/libsecurity_apple_x509_tp-55006': ('1b2487af9b899eda1e74230ebf123d7e91d3973f', 40),
    'src/releases/10.6.8/libsecurity_agent-36399': ('8e1128e00519c982a54cd19b2043c6518f9f66e0', 10),
    'src/releases/10.6.8/libsecurity_checkpw-36064': ('d6484c119b2a751d480c1222e357aca2a092c063', 5),
    'src/releases/10.6.8/libsecurity_pkcs12-40627': ('2a3e01de8c513a6116819bde2e56fdbc52a31084', 25),
    'src/releases/10.6.8/libsecurity_smime-36873': ('551e84b848ef04f7a007eadc604e1ebc0b15d75d', 58),
    'src/releases/10.6.8/libxml2-21.11.1': ('72340bc682b64623434ce3e69da19bc94712a3f2', 3787),
    'src/releases/10.6.8/libxslt-10.9.1': ('cff2edcf28f212c50daf3058e1921d8bf4829540', 2091),
    'src/releases/10.6.8/libsecurity_ocspd-55004': ('33da1264b2a21dda67cc1b36bd9d7157d632e389', 16),
    'src/releases/10.6.8/libsecurity_apple_x509_cl-36064': ('aaa6b8c436199510aa6694d4ac95067ec62575db', 42),
    'src/releases/10.6.8/gcc_select-70': ('0941beaa2079ab7cbe5687e4bce3e0c72df3c2c8', 6),
    'src/releases/10.6.8/libsecurity_cdsa_plugin-36327': ('5e48b3e76caaef66743f77a8e50ef54a22fac723', 25),
    'src/releases/10.6.8/libsecurity_cdsa_utilities-36658': ('1cf25a29f8e1854a8fd01183afbdfb31b80e8dd4', 91),
    'src/releases/10.6.8/libsecurity_filedb-36725': ('d9b4cdc3057802e57ba542ccf45818e4dbc2a7d0', 21),
    'src/releases/10.6.8/gcc-5646': ('33d57846660f3c1c94d8fd5b66f64f44931a3b21', 20958),
    'src/releases/10.6.8/llvmCore-2120': ('5518b8dbe1bb7b1582cc478b6b576577dfa0e950', 5757),
    'src/releases/10.6.8/llvmgcc42-2118': ('27ca0b6f5232f349777a1db57f99fc0e38cd834a', 25174),
    'src/releases/10.6.8/net_snmp-127': ('04dacf06c43ce7f564e8529779d9a76f6d0e3ba4', 32),
    'src/releases/10.6.8/Libsystem-125.2.11': ('44420cfcf31da8aa56fd3fca740fe8c47b72cd32', 16),
    'src/releases/10.6.8/DirectoryService-621.12': ('f29ae461575b52e3061d6178d9ee34e15cb14acd', 393),
    'historical-vendored/xnu-1228.15.4': ('9d80f9528906753d682f9d65d56a0276bad56b4d', 3156),
    'historical-vendored/xnu-1456.1.26': ('46708ce5a6d4a42164ddb67a90fa6fbc7f986430', 3379),
    'historical-vendored/xnu-1504.15.3': ('0ffff24afe52ed47d20c5a06f07a10200f89f32b', 3386),
}
EXCLUDED = ('src/xnu/', 'src/apple-distributions-macos11/')


def run(*args):
    return subprocess.check_output(['git', *args], universal_newlines=True)


def verify():
    cfg = configparser.ConfigParser()
    if not cfg.read('.gitmodules'):
        raise ValueError('missing root .gitmodules')
    paths = [cfg.get(section, 'path') for section in cfg.sections()]
    if len(paths) != len(set(paths)) or len(cfg.sections()) != len(paths):
        raise ValueError('duplicate submodule path')
    entries = run('ls-tree', '-r', 'HEAD').splitlines()
    links = {line.split('\t', 1)[1] for line in entries if line.startswith('160000 commit ')}
    if set(paths) != links or len(links) != 367:
        raise ValueError('gitlink mapping mismatch')
    if sum(path.startswith(SNOW) for path in paths) != 353:
        raise ValueError('10.6.8 component graph mismatch')
    if sum(path.startswith('historical/') for path in paths) != 14:
        raise ValueError('10.5/10.6 historical graph mismatch')
    for path in EXCLUDED:
        if any(line.split('\t', 1)[1].startswith(path) for line in entries):
            raise ValueError('unqualified modern source tree: ' + path)
    for path, (tree_sha, count) in EXPECTED.items():
        if run('rev-parse', 'HEAD:' + path).strip() != tree_sha:
            raise ValueError('source tree hash mismatch: ' + path)
        if len(run('ls-tree', '-r', '--name-only', 'HEAD', path).splitlines()) != count:
            raise ValueError('source tree file count mismatch: ' + path)
    pin = run('ls-tree', 'HEAD', SNOW + 'xnu').strip()
    if not pin.startswith('160000 commit 99c11f3f90a18f35d3692ea77444b51fd972a4f4\t'):
        raise ValueError('10.6.8 XNU pin mismatch')
    xnu = sum('/xnu-' in path for path in EXPECTED)
    print('PASS: 353 Snow Leopard + 14 historical source pins; {} verified XNU snapshots; modern whole-tree exclusions'.format(xnu))


if __name__ == '__main__':
    try:
        verify()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('source graph invalid: {}'.format(exc), file=sys.stderr)
        sys.exit(1)
