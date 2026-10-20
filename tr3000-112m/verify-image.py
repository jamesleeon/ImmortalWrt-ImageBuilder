"""Inspect the actual SquashFS payload, not just ImageBuilder input files."""
import argparse
import pathlib
import shutil
import subprocess
import tarfile
import tempfile


def verify(image: pathlib.Path, unsquashfs: str, expected_feeds: pathlib.Path,
           include_daed: bool) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = pathlib.Path(temporary) / "root.squashfs"
        with tarfile.open(image) as archive:
            members = [m for m in archive.getmembers() if m.name.endswith("/root") and m.isfile()]
            if len(members) != 1:
                raise ValueError("Expected one stock-format sysupgrade root filesystem")
            with root.open("wb") as output:
                shutil.copyfileobj(archive.extractfile(members[0]), output)

        def read(name: str) -> bytes:
            return subprocess.check_output([unsquashfs, "-cat", str(root), name])

        if read("etc/apk/repositories.d/distfeeds.list") != expected_feeds.read_bytes():
            raise ValueError("Firmware repositories differ from reviewed official feeds")
        if not read("usr/lib/lua/luci/i18n/package-manager.zh-cn.lmo"):
            raise ValueError("Package manager Chinese translation is empty")
        if include_daed:
            if read("usr/share/daed/upstream-version").strip() != b"v2.1.1":
                raise ValueError("Wrong daed release in the root filesystem")
            executable = read("usr/bin/daed")
            if executable[:4] != b"\x7fELF" or executable[18:20] != b"\xb7\x00":
                raise ValueError("daed is not an ARM64 ELF executable")
            if b"v2.1.1" not in executable:
                raise ValueError("Executable does not contain the expected daed version")
    print("PASS: actual firmware payload has official feeds, Chinese translation and requested daed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=pathlib.Path)
    parser.add_argument("--unsquashfs", required=True)
    parser.add_argument("--feeds", required=True, type=pathlib.Path)
    parser.add_argument("--include-daed", choices=("true", "false"), required=True)
    args = parser.parse_args()
    verify(args.image, args.unsquashfs, args.feeds, args.include_daed == "true")
