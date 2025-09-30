-- SPDX-FileCopyrightText: 2025 m00nyONE
-- SPDX-License-Identifier: Artistic-2.0

local lib_name = "LibCustomIcons"

local lib = _G[lib_name]
local s = lib.GetStaticTable()
local a = lib.GetAnimatedTable()
local sLength = 0
local aLength = 0

local EM = EVENT_MANAGER
local LAM = LibAddonMenu2

local WM = GetWindowManager()
local GUIControl = LibCustomIcons_IntegrityCheck

local iconSize = 32
local SCREEN_WIDTH = GuiRoot:GetWidth()
local SCREEN_HEIGHT = GuiRoot:GetHeight()
--local maxColumns = zo_floor(SCREEN_WIDTH / iconSize)
--local maxRows = zo_floor(SCREEN_HEIGHT / iconSize)

local LOAD_DELAY = 5 --5ms
local checkAfter = 0
local unloadAfter = 5000
local reportAfter = 1000

local iconPool = {}
local scannedIcons = 0
local failedList = {}

local function len(T)
    local count = 0
    for _ in pairs(T) do count = count + 1 end
    return count
end

local function resetValues()
    checkAfter = 0
    iconPool = {}
    scannedIcons = 0
    failedList = {}
    sLength = 0
    aLength = 0
end

local function GetResults()
    zo_callLater(function()
        local failed = len(failedList)

        local integrityFailed = failed > 10
        local color = "00FF00"
        local status = "passed"
        local message = "all fine :-)"

        local function colorize(str)
            return "|c" .. color .. str .. "|r"
        end

        if integrityFailed then
            color = "FF0000"
            status = "failed"
            message = colorize(
                    "\nThere might be an issue with your LibCustomIcons installation.\n" ..
                            "please consider reinstalling the addon\n"
            )

            d(colorize("Missing icons:"))
            for user, icon in pairs(failedList) do
                d(colorize(user .. " (" .. icon .. ")"))
            end
            d("")
        end

        d(colorize("summary:"))
        d(colorize("icons scanned: " .. scannedIcons))
        d(colorize("icons failed: " .. failed))
        d("")

        PlaySound(SOUNDS.BOOK_COLLECTION_COMPLETED)
        if not ZO_Dialogs_IsShowingDialog() then
            LAM.util.ShowConfirmationDialog(
                    "LibCustomIcons Integrity check",
                    "Integrity check ".. colorize(status) .. "\n" ..
                            "icons scanned: " .. scannedIcons .. "\n" ..
                            "icons failed: " .. colorize(failed) .. "\n" ..
                            message,
                    nil)
        end

    end, 1000)
end

local function createTexture(iconNumber, userName, iconPath)
    --local iconColumn = iconNumber % maxColumns
    --local iconRow = (zo_floor((iconSize * iconNumber) / SCREEN_WIDTH)) % maxRows
    local iconX = zo_floor(math.random(0, SCREEN_WIDTH - iconSize))
    local iconY = zo_floor(math.random(0, SCREEN_HEIGHT - iconSize))

    local icon = WM:CreateControl( GUIControl:GetName() .. "_" .. GetGameTimeMilliseconds() .. "_Icon_" .. tostring(iconNumber), GUIControl, CT_TEXTURE)

    icon.userName = userName
    icon.iconPath = iconPath
    icon:ClearAnchors()
    --icon:SetAnchor( TOPLEFT, GUIControl, TOPLEFT, (iconColumn * iconSize), (iconRow * iconSize))
    icon:SetAnchor( TOPLEFT, GUIControl, TOPLEFT, iconX, iconY)
    icon:SetTextureReleaseOption(RELEASE_TEXTURE_AT_ZERO_REFERENCES)
    icon:SetHidden(false)
    icon:SetTexture(iconPath)
    icon:SetDimensions(iconSize, iconSize)

    iconPool[iconNumber] = icon
    scannedIcons = scannedIcons + 1
end

local function checkTexture(iconNumber)
    local icon = iconPool[iconNumber]
    local isLoaded = icon:IsTextureLoaded()

    if isLoaded then
        iconPool[iconNumber]:SetTexture("LibCustomIcons/assets/check.dds")
    else
        --table.insert(failedList, icon.userName)
        failedList[icon.userName] = icon.iconPath
        iconPool[iconNumber]:SetTexture("LibCustomIcons/assets/cross.dds")
    end
end

local function deleteTexture(iconNumber)
    iconPool[iconNumber]:SetHidden(true)
    iconPool[iconNumber]:SetTexture("none")
    iconPool[iconNumber] = nil
end

local function calculateCheckTime()
    return (sLength + aLength) * LOAD_DELAY
end

local function integrityCheck()
    local limit = 9999999
    local iconNumber = 1

    LibCustomIcons_IntegrityCheck:SetHidden(false)

    d("loading animated icons ...")
    for userName, userData in pairs(a) do
        if iconNumber >= limit then
            break
        end

        local iconPath = userData[1]
        createTexture(iconNumber, userName, iconPath)
        iconNumber = iconNumber + 1
    end

    d("loading static icons ...")
    for userName, _ in pairs(s) do
        if iconNumber >= limit then
            break
        end

        local iconPath = s[userName]
        if iconPath then
            createTexture(iconNumber, userName, iconPath)
            iconNumber = iconNumber + 1
        end
    end

    d("loaded " .. iconNumber .. " icons")

    zo_callLater(function()
        d("checking icons...")
        for i, _ in pairs(iconPool) do
            checkTexture(i)
        end

        zo_callLater(function()
            d("unloading icons ...")
            for i, _ in pairs(iconPool) do
                deleteTexture(i)
            end

            zo_callLater(function()
                LibCustomIcons_IntegrityCheck:SetHidden(true)
                d("writing report ...")
                GetResults()
                d("done")
                end, reportAfter)
            end, unloadAfter)
        end, checkAfter)
end



function lib.IntegrityCheck()
    resetValues()

    sLength = len(s)
    aLength = len(a)

    checkAfter = calculateCheckTime()

    local calculatedTime = (reportAfter + unloadAfter + checkAfter) / 1000

    d("starting integritycheck")
    d("this will take aproximatly " .. calculatedTime .. " seconds")
    d("please wait and let it do its thing :-)")


    if not ZO_Dialogs_IsShowingDialog() then
        LAM.util.ShowConfirmationDialog(
                "LibCustomIcons Integrity check",
                "Do you want to perform an integrity check? This will take approximately ".. calculatedTime .." seconds",
                function() LAM.util.ShowConfirmationDialog(
                        "LibCustomIcons Integrity check",
                        "Please do not interrupt the check. Just let it do its thing. You will get the results after it's finished",
                        function()
                            zo_callLater(integrityCheck, 250)
                        end)
                end)
    end

end