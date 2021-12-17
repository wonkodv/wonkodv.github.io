+++
title = "Fixing the Bluetooth Error `br-connection-unknown`"
description = "Fix `Failed to connect: org.bluez.Error.Failed br-connection-unknown` by pairing again"
date  = "2021-12-14"
taxonomies.category=["Using Unix"]
taxonomies.tags=["Bluetooth"]
+++

# Fixing the Bluetooth Error `br-connection-unknown`

## The Problem

After not using a bluetooth headset for some time, I got the following error
when I tried to connect it to my computer:

```
Failed to connect: org.bluez.Error.Failed br-connection-unknown
```

I used the following commands in `bluetoothctl`:

```
[bluetooth]# power on
[CHG] Controller XX:XX:XX:XX:XX:XX Class: 0x00XXXXXX
Changing power on succeeded
[CHG] Controller XX:XX:XX:XX:XX:XX Powered: yes
[bluetooth]# connect YY:YY:YY:YY:YY:YY
Attempting to connect to YY:YY:YY:YY:YY:YY
[CHG] Device YY:YY:YY:YY:YY:YY Connected: yes
Failed to connect: org.bluez.Error.Failed br-connection-unknown
[CHG] Device YY:YY:YY:YY:YY:YY Connected: no
```

## The Solution

Searching the net gave no quick solution,
but after playing around with it a bit,
I tried to unpair and pair again,
which solved the problem:

``` hl_lines=1 5 14
[bluetooth]# remove YY:YY:YY:YY:YY:YY
[DEL] Device YY:YY:YY:YY:YY:YY btheadphone
Device has been removed
[NEW] Device YY:YY:YY:YY:YY:YY WH-CH510
[bluetooth]# pair YY:YY:YY:YY:YY:YY
Attempting to pair with YY:YY:YY:YY:YY:YY
[CHG] Device YY:YY:YY:YY:YY:YY Connected: yes
[CHG] ...
[CHG] Device YY:YY:YY:YY:YY:YY ServicesResolved: yes
[CHG] Device YY:YY:YY:YY:YY:YY Paired: yes
Pairing successful
[CHG] Device YY:YY:YY:YY:YY:YY ServicesResolved: no
[CHG] Device YY:YY:YY:YY:YY:YY Connected: no
[bluetooth]# connect YY:YY:YY:YY:YY:YY
Attempting to connect to YY:YY:YY:YY:YY:YY
[CHG] Device YY:YY:YY:YY:YY:YY Connected: yes
Connection successful
```

I then remembered, that I had used the headphone last on a different machine,
from which I copied the entire home folder over to the current one.

I imagine the problem was the following:

Bluetooth uses some encryption with keys derived from secrets,
exchanged while pairing, and the mac addresses of both devices.
Since I changed computer, my MAC changed,
but I copied my entire home folder to the new machine,
so `bluetoothctl` used a cached intermediate key that was only valid on the old computer.
When both devices use different crypto keys they can not understand each other.
In such cases it is hard for the tool to give a more helpful error message than "doesn't work".
If this explanation is wrong, please point me at the right resources to read up on it,
I kind of stopped digging when things worked again.
