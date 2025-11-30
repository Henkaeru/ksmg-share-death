### Notice
This project includes files from **Kaizo Super Mario Galaxy Rebalanced**, which is created and owned by **TGWaluigi**.  
I do **not** claim ownership of Kaizo Super Mario Galaxy Rebalanced. All rights belong to the original creator.

# **Shared Death – KSMG**

Synchronizes player deaths across multiple Dolphin Emulator clients for **Kaizo Super Mario Galaxy**.
When one player dies, everyone dies.



## **Requirements**

* **Dolphin Emulator**
* **Riivolution enabled**
* **Included Riivolution patch (KaizoMarioGalaxyRebalancedV2.1)**
  *This patch is required. It contains the trampoline used to trigger death via memory write.*
* Python 3.9+
* `pip install -r requirements.txt`

## **How It Works**

1. The script detects the **0 HP death screen** using image matching.
2. When detected, it reports a death to the server.
3. All clients poll the server:
   * If a death is active, they trigger a **forced death** using Dolphin Memory Engine.

## **Folder Structure**

```
shared-death-LAN/
│
├── main.py
├── config.py
├── shared_death_config.json
├── image_detector.py
├── dolphin.py
├── server_client.py
├── requirements.txt
│
├── 0-hp.png
└── KaizoMarioGalaxyRebalancedV2.1/
---

## **Setup**

### **1. Install Python dependencies**

```
pip install -r requirements.txt
```

### **2. Install Riivolution Patch**

Copy:

```
KaizoMarioGalaxyRebalancedV2.1/
```

into:

```
Dolphin Emulator/Load/Riivolution/
```

Then enable it in Dolphin.

## **Run**

Start Dolphin, load SMG2, enable the Riivolution patch.
Then:

```
python main.py
```
