[size=6][b]LibCustomIcons[/b][/size]

[i]LibCustomIcons[/i] is a lightweight library for [i]The Elder Scrolls Online[/i] that allows custom icons for players.
Originally part of [b]HodorReflexes[/b], this library was separated out to improve modularity and reduce overhead.
Dependencies: [URL="https://www.esoui.com/downloads/info7-LibAddonMenu.html"]LibAddonMenu-2.0[/URL]

Whether you're a streamer, guild leader, or just want to stand out with a personalized icon, this library gives you that little touch of customization — shared across all supported addons.


[size=4][b] Features[/b][/size]

[list]
[*]Assign custom icons to ESO players
[*]Centralized and easy-to-maintain icon list
[*]Designed for reuse in multiple addons (e.g., HodorReflexes)
[*]Lightweight and dependency-free
[/list]


[size=4][b] Get Your Custom Icon[/b][/size]

Want to be featured with your own custom icon?

[size=3][b] How to participate:[/b][/size]
[list]
[*][b]Create a Pull Request[/b] adding your icon entry to the list
[*]Or [b]send a donation[/b] to @m00nyONE in-game (EU server) and your request will be added
[/list]

This helps support development and keeps the ESO addon ecosystem fun and alive!


[size=4][b]Usage[/b][/size]

If you're an addon developer and want to use [b]LibCustomIcons[/b]:

Have a look at the full documentation here: [URL="https://m00nyone.github.io/LibCustomIcons/"]Github Pages[/URL]

[code]
local icon, coordsLeft, coordsRight, coordsTop, coordsBottom = LibCustomIcons.GetStatic("@accountName")
textureControl:SetTexture(icon)
textureControl:SetTextureCoords(coordsLeft, coordsRight, coordsTop, coordsBottom) -- do not forget todo that ;-)
[/code]

Documentation will be expanded as needed — feel free to open an issue if you need help integrating it.

[size=4][b]Repository Structure[/b][/size]
[list]
[*][b]icons/[/b]: Contains all custom icon definitions
[*][b]LibCustomIcons.lua[/b]: Core logic to retrieve and manage custom icons
[/list]

[size=4][b]Contributing[/b][/size]

[SIZE="4"][URL="https://github.com/m00nyONE/LibCustomIcons"]https://github.com/m00nyONE/LibCustomIcons[/URL]
[/SIZE]
Community contributions are welcome and appreciated!

[list]
[*]Fork the repo
[*]Add your custom icon to the data file
[*]Open a Pull Request with a short description
[/list]

[i]Make sure to keep icons appropriate and tasteful. Offensive or misleading content will not be accepted.[/i]


[size=4][b]Credits[/b][/size]

[img]https://contrib.rocks/image?repo=m00nyONE/LibCustomIcons[/img]
[i]Made with [url=https://contrib.rocks]contrib.rocks[/url][/i]


[size=4][b]Contact[/b][/size]

For questions, contributions, or donations:

[list]
[*]GitHub: [url=https://github.com/m00nyONE/LibCustomIcons/issues]Issues & PRs[/url]
[/list]