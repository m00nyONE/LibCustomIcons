-- SPDX-FileCopyrightText: 2025 m00nyONE
-- SPDX-License-Identifier: Artistic-2.0

local strings = {
    LCI_MENU = "LibCustomIcons",
    LCI_MENU_HEADER = "my custom icon",
    LCI_MENU_GEN_STATIC = "generate static icon LUA code",
    LCI_MENU_GEN_ANIMATED = "generate animated icon LUA code",
    LCI_MENU_LUA = "LUA code:",
    LCI_MENU_LUA_TT = "Send this code to the addon author.",
    LCI_MENU_INTEGRITY = "INTEGRITY",
    LCI_MENU_INTEGRITY_DESCRIPTION = "Check the integrity of LibCustomIcons",
}

for id, val in pairs(strings) do
    ZO_CreateStringId(id, val)
    SafeAddVersion(id, 1)
end