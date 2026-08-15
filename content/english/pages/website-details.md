---
title: "Website Instructions"
# meta title
meta_title: "Website Instructions"
# meta description
description: "Instructions, mostly for Michael's reference on how to manage this site."
# save as draft
draft: false
---

#### Setup on a new Windows PC

Install and setup required components:
```powershell
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install GoLang.Go
winget install Hugo.Hugo.Extended
```

Open new Terminal:

```powershell
cd D:\dev
git clone https://github.com/michaelp85/3malbec.com.git
cd 3malbec.com
npm install
npm run dev
```