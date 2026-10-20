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

默认集成 LuCI、中文界面（含软件包管理中文包）、WireGuard、Android RNDIS/NCM USB 共享组件。
不集成 iPhone 专用组件、ModemManager 或短信工具。CamoDNS-Lite 暂不自动打包，可后续单独部署。
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

## 软件源、daed 和空间占用

最终固件明确写入 25.12.1 官方的 target/base/luci/packages/routing/telephony 六个源，
不写入当前不存在（HTTP 404）的 video 索引，不预设第三方镜像或跳过签名检查。
这个列表只适用于当前固定版本。自编译内核的后续 kmod 必须匹配本次构建的 ABI，
不能靠强制安装官方 kmod 解决版本不匹配。

勾选 daed 时，用项目内的 APK 配方替换 feeds 中的旧版配方，下载并校验上游
v2.1.1 ARM64 发布包，将其程序连同 feeds 中的 procd/UCI 文件打成 `daed 2.1.1-r1`。
此路径打包官方预编译程序，不重新编译上游 daed，也不覆盖原无线工作流的包源。
LuCI 配置入口仍来自固定的官方 LuCI feed；daed 自带网页仍显示其上游前端版本
1.28.0，与程序版本 v2.1.1 不同。升级包不会修复上游统计或 DNS 崩溃问题。

新镜像的 `/rom/usr/bin/daed` 和 APK 版本记录都是新版，不需要刷机后再把新版
复制到可写层。手动升级无法释放只读层中的旧程序；重刷新镜像才会替换它。
新程序会增加只读卷占用，但可避免在可写层再存一份完整新版程序。
旧配置可单独备份；不要将旧 overlay 整体覆盖到新固件，否则会带回旧的程序覆盖文件。

构建会检查 manifest 中的 daed 版本，并直接读取最终 sysupgrade 的 SquashFS，
确认软件源、中文翻译、daed 发布标识及 ARM64 可执行程序确实进入镜像。
