---
title: "Website Instructions"
# meta title
meta_title: "Website Instructions"
# meta description
description: "Instructions, mostly for Michael's reference on how to manage this site."
# save as draft
draft: false
---

## Setup on a new Windows PC

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
npm  install
npm run dev
```

## Camera Live Stream

See snapshot/nx_snapshot.py in the repo.

/etc/systemd/system/snapshot.service
```bash
[Unit]
Description=Publish camera snapshot
After=network-online.target

[Service]
Type=oneshot
EnvironmentFile=/etc/snapshot.env
ExecStart=/usr/bin/python3 /opt/snapshot/nx_snapshot.py
TimeoutStartSec=90
```

/etc/systemd/system/snapshot.timer
```bash
[Unit]
Description=Snapshot cadence

[Timer]
OnCalendar=*-*-* 07..18:00/2:00
OnCalendar=*-*-* 19..23,00..06:00/10:00
Persistent=false
AccuracySec=1s

[Install]
WantedBy=timers.target
```

Setup:
```bash
sudo systemctl enable --now snapshot.timer
sudo systemctl start snapshot.service
```

Confirm working via:
```bash
systemctl list-timers snapshot.timer
```