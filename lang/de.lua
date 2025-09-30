-- SPDX-FileCopyrightText: 2025 m00nyONE
-- SPDX-License-Identifier: Artistic-2.0

local strings = {
    LCI_MENU = "LibCustomIcons",
    LCI_MENU_HEADER = "mein benutzerdefiniertes Icon",
    LCI_MENU_GEN_STATIC = "LUA-Code für statisches Icon erzeugen",
    LCI_MENU_GEN_ANIMATED = "LUA-Code für animiertes Icon erzeugen",
    LCI_MENU_LUA = "LUA-Code:",
    LCI_MENU_LUA_TT = "Sende diesen Code an den Addon-Autor.",
    LCI_MENU_INTEGRITY = "INTEGRITÄT",
    LCI_MENU_INTEGRITY_DESCRIPTION = "Überprüft die Integrität von LibCustomIcons",
}

for id, val in pairs(strings) do
    ZO_CreateStringId(id, val)
    SafeAddVersion(id, 1)
end
