# LibCustomIcons

**LibCustomIcons** is a lightweight library for *The Elder Scrolls Online* that allows custom icons for players. Originally part of **HodorReflexes**, this library was separated out to improve modularity and reduce overhead.

Whether you're a streamer, guild leader, or just want to stand out with a personalized icon, this library gives you that little touch of customization — shared across all supported addons.

---

## 🔧 Features

- Assign custom icons to ESO players
- Centralized and easy-to-maintain icon list
- Designed for reuse in multiple addons (e.g., HodorReflexes)
- Lightweight and dependency-free

---

## 🎉 Get Your Custom Icon

Want to be featured with your own custom icon?

### 📝 How to participate:
- **Create a Pull Request** adding your icon entry to the list.
- Or **send a donation** to `@m00nyONE` in-game (EU server) and your request will be added.

This helps support development and keep the ESO addon ecosystem fun and alive!

---

## 💡 Usage

If you're an addon developer and want to use `LibCustomIcons`:

Have a look at the full documentation here: [Github Pages](https://m00nyone.github.io/LibCustomIcons/)


```lua
local icon, coordsLeft, coordsRight, coordsTop, coordsBottom = LibCustomIcons.GetStatic("@accountName")
textureControl:SetTexture(icon)
textureControl:SetTextureCoords(coordsLeft, coordsRight, coordsTop, coordsBottom) -- do not forget todo that ;-)
```
Documentation will be expanded as needed — feel free to open an issue if you need help integrating it.

## 📁 Repository Structure
icons/: Contains all custom icon definitions.

LibCustomIcons.lua: Core logic to retrieve and manage custom icons.

## 🤝 Contributing
Community contributions are welcome and appreciated!

- Fork the repo
- Add your custom icon to the data file
- Open a Pull Request with a short description
- Make sure to keep icons appropriate and tasteful. Offensive or misleading content will not be accepted.

## 🙏 Credits
<a href="https://github.com/m00nyONE/LibCustomIcons/graphs/contributors">
<img src="https://contrib.rocks/image?repo=m00nyONE/LibCustomIcons" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
## 📬 Contact
For questions, contributions, or donations:

GitHub: Issues & PRs