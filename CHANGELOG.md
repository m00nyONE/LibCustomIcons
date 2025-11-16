## 2025.11.16
- BREAKING CHANGE FOR DEVELOPERS:
- removed GetIcon() - use GetStatic() or GetAnimated() instead
- BREAKING CHANGES IN THE NEAR FUTURE:
- GetStatic() now returns `texturePath, textureCoordsLeft, textureCoordsRight, textureCoordsTop, textureCoordsBottom` instead of only texturePath
- GetAnimated() now returns `texturePath, textureCoordsLeft, textureCoordsRight, textureCoordsTop, textureCoordsBottom, columns, rows, framerate` instead of a table.
- If you are a developer, and you have problems migrating, message me on Discord :-) I'll help you out.

## 2025.08.16
- merge even more contributions

## 2025.08.04
- merged HREI by @sshogrin

## 2025.08.02
- merged Piou Icons by @TenshiRaitoEso
- HasIcon bugfix by @WashedNotSloshed
- unify API
- fix some icons that went missing during migration

## 2025.07.22
- Addon now automatically releases every sunday if there are changes in the files
- remove orphaned icons
- remove duplicate entries
- new contributions
- add a few tests like sanity-check, include-check, duplicate-check to the github pipeline

## 2025.07.20
- update menu
- Dolgubon you coulda just asked :D

## 2025.07.01
- add integrity check /lci integrity
- add menu

## 2025.06.27
- first usable version
- add api function to be used by other addons
- porting over all custom icons from HodorReflexes