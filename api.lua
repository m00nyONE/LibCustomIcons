-- SPDX-FileCopyrightText: 2025 m00nyONE
-- SPDX-License-Identifier: Artistic-2.0

local lib_name = "LibCustomIcons"
local lib = _G[lib_name]
local s = lib.GetStaticTable()
local a = lib.GetAnimatedTable()

--[[ doc.lua begin ]]
local currentFolder = "misc" .. tostring(os.date("%Y") - 2018)

--- Retrieves the current folder where the icons are stored.
--- @return string folder The current folder name
function lib.GetCurrentFolder()
    return currentFolder
end

--- Checks whether a static icon exists for the given username.
--- @param username string The player's account name (e.g., "@m00nyONE").
--- @return boolean hasStaticIcon `true` if a custom static icons exists, `false` otherwise.
function lib.HasStatic(username)
    return s[username] ~= nil
end
--- Checks whether an animated icon exists for the given username.
--- @param username string The player's account name (e.g., "@m00nyONE").
--- @return boolean hasAnimatedIcon `true` if a custom animated icons exists, `false` otherwise.
function lib.HasAnimated(username)
    return a[username] ~= nil
end
--- Checks if a custom icon (either static or animated) exists for the given username.
--- @param username string The player's account name (e.g., "@m00nyONE").
--- @return boolean hasStaticIcon `true` if a custom static icons exists, `false` otherwise.
function lib.HasIcon(username)
    return lib.HasStatic(username) or lib.HasAnimated(username)
end


--- Retrieves the texturePath of the static icon for the user or nil if none exists.
--- @param username string The player's account name (e.g., "@m00nyONE").
--- @return string|nil, number, number, number, number texturePath or `nil` if no static icon exists, textureCoordsLeft, textureCoordsRight, textureCoordsTop, textureCoordsBottom
function lib.GetStatic(username)
    if type(s[username]) == "table" then -- compiled icon
        local texture, left, right, top, bottom, width, height = unpack(s[username])
        return texture, left/width, right/width, top/height, bottom/height
    end
    return s[username], 0, 1, 0, 1
end
--- Retrieves the texturePath and animation parameters of the animated icon for the user or nil if none exists.
--- @param username string The player's account name (e.g., "@m00nyONE").
--- @return string|nil, number, number, number, number, number, number, number `texturePath, textureCoordsLeft, textureCoordsRight, textureCoordsTop, textureCoordsBottom, columns, rows, fps` or `nil` if no animated icon exists
function lib.GetAnimated(username)
    -- TODO: uncomment when animated icons get merged textures
    --local anim = a[username]
    --if not anim then
    --    return nil, 0, 1, 0, 1, nil, nil, nil
    --end
    --if #anim > 4 then -- compiled animation
    --    local texturePath, columns, rows, fps, left, right, top, bottom, width, height = unpack(anim)
    --    return texturePath, left/width, right/width, top/height, bottom/height, columns, rows, fps
    --end
    --
    --return anim[1], 0, 1, 0, 1, anim[2], anim[3], anim[4]

    return a[username]
end

-- cached Clones of the internal tables for the GetAll* function. As these tables should always be readOnly and do nothing if edited, there is no need for them to be cloned each time they're requested
local cachedStaticIconsTableClone = nil
local cachedAnimatedIconsTableClone = nil

--- Retrieves all registered static icons from the internal table as a deep copy.
--- Editing the returning table has no effect to the internal one that is used to retrieve actual icons.
--- @return table<string,string> staticTable mapping `@accountname` to `texturePath` for all static icons
function lib.GetAllStatic()
    if not cachedStaticIconsTableClone then
        cachedStaticIconsTableClone = ZO_DeepTableCopy(s)
    end
    return cachedStaticIconsTableClone
end

--- Retrieves all registered animated icons from the internal table as a deep copy.
--- Editing the returning table has no effect to the internal one that is used to retrieve actual icons.
--- @return table<string,table> animTable mapping `@accountname` to `{texturePath, width, height, fps}` for all animated icons
function lib.GetAllAnimated()
    if not cachedAnimatedIconsTableClone then
        cachedAnimatedIconsTableClone = ZO_DeepTableCopy(a)
    end
    return cachedAnimatedIconsTableClone
end

-- The number of static and animated icons is fixed at runtime (icons are registered once and not modified later). To optimize performance, counts are calculated only once when first requested and then cached for future calls.
local cachedStaticIconCount = 0
local cachedAnimatedIconCount = 0
local cachedTotalIconCount = 0

--- Returns the number of registered static icons.
--- The result is cached after the first computation.
--- @return number count The number of static icons
function lib.GetStaticCount()
    if cachedStaticIconCount == 0 then
        for _ in pairs(s) do
            cachedStaticIconCount = cachedStaticIconCount + 1
        end
    end
    return cachedStaticIconCount
end

--- Returns the number of registered animated icons.
--- The result is cached after the first computation.
--- @return number count The number of animated icons
function lib.GetAnimatedCount()
    if cachedAnimatedIconCount == 0 then
        for _ in pairs(a) do
            cachedAnimatedIconCount = cachedAnimatedIconCount + 1
        end
    end
    return cachedAnimatedIconCount
end

--- Returns the total number of registered icons (static + animated).
--- The result is cached after the first computation.
--- @return number count The total number of icons
function lib.GetIconCount()
    if cachedTotalIconCount == 0 then
        cachedTotalIconCount = lib.GetStaticCount() + lib.GetAnimatedCount()
    end
    return cachedTotalIconCount
end

--[[ doc.lua end ]]
