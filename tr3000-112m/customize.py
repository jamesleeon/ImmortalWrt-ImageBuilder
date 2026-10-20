"""Prepare the pinned daed package and the firmware's public repositories."""
import pathlib
import shutil
import sys


def install_package(source: pathlib.Path) -> None:
    package = source / "feeds/packages/net/daed"
    # Preserve the feed's tested init/UCI integration; never install systemd units.
    for name in ("daed.init", "daed.config"):
        if not (package / "files" / name).is_file():
            raise ValueError(f"Missing OpenWrt daed integration file: {name}")
    shutil.copyfile(pathlib.Path(__file__).parent / "daed/Makefile", package / "Makefile")


def stage_files(destination: pathlib.Path) -> None:
    directory = destination / "etc/apk/repositories.d"
    directory.mkdir(parents=True, exist_ok=True)
    base = "https://downloads.immortalwrt.org/releases/25.12.1"
    urls = [f"{base}/targets/mediatek/filogic/packages/packages.adb"]
    urls += [f"{base}/packages/aarch64_cortex-a53/{feed}/packages.adb"
             for feed in ("base", "luci", "packages", "routing", "telephony")]
    # The 25.12.1 video index returns HTTP 404. No unverified mirror or snapshot.
    (directory / "distfeeds.list").write_text("\n".join(urls) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "package":
        install_package(pathlib.Path(sys.argv[2]))
    elif sys.argv[1] == "files":
        stage_files(pathlib.Path(sys.argv[2]))
    else:
        raise SystemExit("Expected package SOURCE or files DESTINATION")
