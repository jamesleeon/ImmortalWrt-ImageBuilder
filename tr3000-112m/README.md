# TR3000 v1：112 MiB NMBM 专用构建

此入口适用于 128 MiB 闪存、已经安装第三方多布局 U-Boot，并准备使用
`mod-112m` 的 TR3000 v1。不是官方 `cudy_tr3000-v1-ubootmod` 布局，
也不适用于 `maximum-114m`、256 MiB 型号或原厂引导。

## 如何构建

1. 将本次修改推送到自己的仓库后，在 Actions 中打开 **Build TR3000 112m NMBM**。
2. 点击 Run workflow，选择是否集成 daed；额外软件包填官方软件源中的准确包名。
3. 等待构建完成，在该次运行的 Artifacts 下载构建结果。首次从源码编译可能需要数小时。
4. 固件名称包含 `112m-nmbm-squashfs-sysupgrade.bin`；同时提供专用 ImageBuilder、
   编译后的 DTB、源码补丁、配置、包清单、源码提交及校验值。

默认集成 LuCI、中文界面、WireGuard、Android RNDIS/NCM 和 iPhone USB 共享组件。
不集成 ModemManager 或短信工具。CamoDNS-Lite 暂不自动打包，可后续单独部署。
daed 可与其他功能共存，但运行时 DNS、分流及路由需另行配置。

## 与原工作流的区别

原无线构建工作流不变。新工作流从固定发行标签 `v25.12.1` 获取源码，保留普通
`cudy_tr3000-v1` 的 NMBM 属性、分区起点和 kernel/root 卷格式，仅把设备树 UBI
容量改为 `0x7000000`（112 MiB），镜像容量限制改为 `114688k`。
它重新编译内核和 ImageBuilder，再通过这份 ImageBuilder 组合软件包。
不是修改官方预编译 ImageBuilder 的 rootfs 大小，也不拼接旧内核。

源码标签固定，feeds 更新及下载依赖仍可能变化；提交号和 feeds 信息随产物保存。
升级源码版本时需要重新检查适配，脚本遇到结构变化会失败，不会静默替换。
ImageBuilder 内部 profile/兼容标识仍是普通 `cudy_tr3000-v1`，务必通过产物名称、
补丁及 DTB 区分布局；普通 sysupgrade 的机型检查无法检测这个容量差异。

## 刷入边界

此工作流只生成产物，不操作路由器、不刷引导、不自动发布 Release。
首次迁移前，将全部可读分区（尤其 Factory、bdinfo、BL2、FIP）及配置备份到电脑，
确认现有 U-Boot 的恢复流程可用。迁移需要配套处理 U-Boot 的 `mod-112m` 选择和
UBI/可写卷初始化；不能仅在当前 LuCI 强制升级后就假定卷会自动扩大。
不要直接套用来源不明的擦除命令，也不要将官方 ubootmod 的镜像混入此流程。

构建成功不等于已通过实机测试。实际刷入步骤需对照当前 U-Boot 页面及其实现确认。
启动后核对 `/proc/mtd` 中 UBI 为 `07000000`，再用 `ubinfo -a`、`df -h /overlay`
确认可写卷使用新增容量，并验证手机 USB 共享、Wi-Fi、WireGuard 和 DNS。
