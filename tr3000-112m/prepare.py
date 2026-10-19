"""Patch the stock NMBM profile; never substitute the official ubootmod profile."""
import pathlib
import re
import sys


def patch(source: pathlib.Path) -> None:
    dts = source / "target/linux/mediatek/dts/mt7981b-cudy-tr3000-v1.dts"
    image = source / "target/linux/mediatek/image/filogic.mk"
    text = dts.read_text(encoding="utf-8")
    if "mediatek,nmbm;" not in text:
        raise ValueError("Stock TR3000 NMBM support missing; refusing to patch")
    old = "reg = <0x5c0000 0x4000000>;"
    if text.count(old) != 1:
        raise ValueError("Expected exactly one stock 64 MiB UBI definition")
    patched_dts = text.replace(old, "reg = <0x5c0000 0x7000000>;")
    mk = image.read_text(encoding="utf-8")
    pattern = r"(?ms)^define Device/cudy_tr3000-v1\n.*?^endef$"
    blocks = list(re.finditer(pattern, mk))
    if len(blocks) != 1:
        raise ValueError("Stock device profile missing or ambiguous")
    block = blocks[0].group()
    if "KERNEL_IN_UBI := 1" not in block or "sysupgrade-tar" not in block:
        raise ValueError("Unexpected stock kernel/root UBI image format")
    old_limit = "IMAGE_SIZE := 65536k"
    if block.count(old_limit) != 1:
        raise ValueError("Unexpected stock image size limit")
    start, end = blocks[0].span()
    patched_mk = mk[:start] + block.replace(old_limit, "IMAGE_SIZE := 114688k") + mk[end:]
    # Validate every precondition before writing either file.
    dts.write_text(patched_dts, encoding="utf-8")
    image.write_text(patched_mk, encoding="utf-8")
    print("TR3000 NMBM: UBI start 0x5c0000, size 112 MiB; stock kernel/root format")


if __name__ == "__main__":
    patch(pathlib.Path(sys.argv[1]))
