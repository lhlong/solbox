# SOLBOX
- music box for Sol


## RFID Reader

> sudo apt-get install libusb

### Get Device ID

> lsusb

### Set permission for usb

> sudo nano /etc/udev/rules.d/99-rfid.rules
>
> SUBSYSTEMS=="usb", ATTRS{idVendor}=="08ff", ATTRS{idProduct}=="0009", MODE="666"
>
>sudo udevadm trigger

## Create virtualenv

> pip3 install virtualenv
>
> virtualenv solbox
>
> source solbox/bin/activate
>
> sudo apt-get install libusb-1.0-0-dev
>
> pip install -r requirements.txt

## Run

> sh run.sh
