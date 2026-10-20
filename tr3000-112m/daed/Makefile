# SPDX-License-Identifier: GPL-2.0-only
# Package the verified upstream ARM64 release, keeping OpenWrt/procd integration.
include $(TOPDIR)/rules.mk

PKG_NAME:=daed
PKG_VERSION:=2.1.1
PKG_RELEASE:=1
PKG_SOURCE:=daed-$(PKG_VERSION)-linux-arm64.zip
PKG_SOURCE_URL:=https://github.com/daeuniverse/daed/releases/download/v$(PKG_VERSION)
PKG_SOURCE_URL_FILE:=daed-linux-arm64.zip
PKG_HASH:=96e1dcae1cc88d434c59eb41cee74e6119505ba9ab3e64fd40196eaddaab137a
PKG_LICENSE:=AGPL-3.0-only MIT
PKG_BUILD_DIR:=$(BUILD_DIR)/daed-$(PKG_VERSION)-linux-arm64

include $(INCLUDE_DIR)/package.mk

define Package/daed/Default
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Web Servers/Proxies
  URL:=https://github.com/daeuniverse/daed
endef

define Package/daed
  $(call Package/daed/Default)
  TITLE:=dae dashboard (upstream ARM64 release)
  DEPENDS:=@aarch64 +ca-bundle +kmod-sched-core +kmod-sched-bpf +kmod-xdp-sockets-diag +kmod-veth
endef

define Package/daed-geoip
  $(call Package/daed/Default)
  TITLE:=GeoIP data for daed
  DEPENDS:=+daed +v2ray-geoip
  PKGARCH:=all
endef

define Package/daed-geosite
  $(call Package/daed/Default)
  TITLE:=Geosite data for daed
  DEPENDS:=+daed +v2ray-geosite
  PKGARCH:=all
endef

define Package/daed/conffiles
/etc/daed/wing.db
/etc/config/daed
endef

define Build/Prepare
	$(INSTALL_DIR) $(PKG_BUILD_DIR)
	unzip -p $(DL_DIR)/$(PKG_SOURCE) daed-linux-arm64/daed-linux-arm64 > $(PKG_BUILD_DIR)/daed
	test -s $(PKG_BUILD_DIR)/daed
	printf '%s\n' 'v$(PKG_VERSION)' > $(PKG_BUILD_DIR)/upstream-version
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/daed/install
	$(INSTALL_DIR) $(1)/usr/bin $(1)/etc/config $(1)/etc/init.d $(1)/usr/share/daed
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/daed $(1)/usr/bin/daed
	$(INSTALL_CONF) $(CURDIR)/files/daed.config $(1)/etc/config/daed
	$(INSTALL_BIN) $(CURDIR)/files/daed.init $(1)/etc/init.d/daed
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/upstream-version $(1)/usr/share/daed/upstream-version
endef

define Package/daed-geoip/install
	$(INSTALL_DIR) $(1)/usr/share/daed
	$(LN) ../v2ray/geoip.dat $(1)/usr/share/daed/geoip.dat
endef

define Package/daed-geosite/install
	$(INSTALL_DIR) $(1)/usr/share/daed
	$(LN) ../v2ray/geosite.dat $(1)/usr/share/daed/geosite.dat
endef

$(eval $(call BuildPackage,daed))
$(eval $(call BuildPackage,daed-geoip))
$(eval $(call BuildPackage,daed-geosite))
