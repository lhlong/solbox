# SOLBOX

- music box for Sol

This repository provide a source code for music box - a tool for kids.
Just swipe the card and enjoy your favorite music.

![](./src/data/image/solbox1.jpg)

![](./src/data/image/solbox2.jpg)

## 1. RFID Reader

> sudo apt-get install libusb

### 1.1. Get Device ID

> lsusb

Here is my current values:

```text
# RFID Device ID
VENDOR_ID = 0x08ff
PRODUCT_ID = 0x0009
```

### 1.2. Set permission for usb

> sudo nano /etc/udev/rules.d/99-rfid.rules

```text
SUBSYSTEMS=="usb", ATTRS{idVendor}=="08ff", ATTRS{idProduct}=="0009", MODE="666"
```

>sudo udevadm trigger

## 2. Create virtualenv

```bash
pip3 install virtualenv
virtualenv solbox
source solbox/bin/activate
sudo apt-get install libusb-1.0-0-dev
pip install -r requirements.txt
```

## 3. Run

Update your tags id to `code.json` file and save your music to `data` folder.
Then,

> sh run.sh
