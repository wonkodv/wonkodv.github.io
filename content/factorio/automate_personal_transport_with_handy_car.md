+++
title = "Factorio: Automate Personal Transportation with Handy Car"
description = "A System of Blueprints and Train Schedule to ease personal transportation trains"
taxonomies.category=["Playing"]
taxonomies.tags=["Factorio"]
date=2022-01-03
extra.image= "factorio/automate_personal_transport_with_handy_car/handy_car.png"
+++

# Automate Personal Transportation with Handy Car


{{ image(path="handy_car.png", alt="Train arriving to pick me up", title="Timmy is coming to pick me up.", center=true) }}

## The Problem

My Base is hard to navigate without Spidertron or train.
There are train tracks everywhere, lots of trains trying to roll over me, and no
safe path to drive a car in.

{{ image(path="too_many_rails.png", alt="Screenshot of a Base with lots of rails", title="2 by 2 chunk squares, only left turns, 1-1 Trains.", center=true, width=500) }}


## The Solution

The solution is __Handy Car__[^1]. (I considered calling it uber).

You place a Train stop called {{ factorio_string(body="[entity=character] L") }} using a blueprint on the nearest track.
Pretty soon there comes Timmy (A Train) and waits for you to enter.
It will start driving immediately. You can:
*   Do nothing and get transported to {{ factorio_string(body="Timmy's HQ") }}
*   Use `CTRL+LEFT_CLICK` in the map to place a temporary Waypoint
*   Let Bots (or other players if you have friends) place
    a Station {{ factorio_string(body="[entity=character] U") }} and automatically
    get taken there.

Once you leave the train, it will drive back to {{ factorio_string(body="Timmy's HQ") }}.

With some circuitry, the pickup and drop off stations will deactivate
automatically after the trains topped there, so that they do not interfere with
your transportation needs later.
Disabled train stops add a pathing penalty so you should remove the unused stops eventually.
A speaker places a blinking icon on the map reminding you to remove the train stops.
You can just hit `CTRL-Z` to let bots undo the placing.

## Implementation

### Train

A dedicated Train With the following configuration:

{{ image(path="train_schedule.png", alt="Screenshot of schedule", title="Handy Car Schedule") }}

The Timeout is to give you some time to enter, but eventually get over it if you
forgot about your appointment.

### Timmy's HQ

A Train Stop  somewhere in the middle, well connected, with refueling.
If your base is large, you can have multiple trains and multiple stations, each
with limit 1.

### Pickup and Dropoff Site

Apart from the Name, the Pickup and Dropoff Stations are the same Blueprint.

*   The Station with this configuration:

    {{ image(path="station_config.png", alt="Station with 'Enable/disable' and 'Read stopped train'") }}

*   Combinator that sends nothing in the beginning (`T == D == 0`). Once the
    train comes (e.g. `T == 4267`) it sends `D` until you destroy it.

    {{ image(path="decider_config.png", alt="Decider combinator with 'if T ≠ D set D to 1'") }}

*   Speaker that shows the map icon.

    {{ image(path="speaker_config.png", alt="Speaker with volume 0, Condition 'anything > 0' T as Icon, the String 'Remove' and 'Show icon on map' checked.") }}

*   an opportunistic power pole to make the speaker and circuitry work.

## Blueprint

```
0eNrtWM1u2zgQfhWDl73IgX4ty0B72R562EO7aE5FIFASLRORSIGi3BqBHmDfYp9tn2RnKFtWGkWWkyz2EgSORA45/zPf2A8kKRpWKS50nEh5TzYP552abL4/XHEAaTyVotuueS5ogXv6UDGyIVyzklhE0BJXhUxlKTXfM9JahIuM/SQbp7VGLu650g3s9He7E8s/Bjfd9s4iTGiuOevkm8UhFk2ZMAWs+9sJz5esYKlWPF1WsmDAuJI13JQCpQK3pQ/HD3DJdv0WdfqFmdsz04pysay1rMa4eCcuAWiacQVCDXllEfCTVrKIE7ajey4V3km5ShuuY6BlPaMtV7WOZzvlEzoFg6ApRsTGRVlRRTXKIB8M+SiHCZoULM54jU+y0aphFlGMZjFaVLEsNvadKGbRk2ar9I20nU6is7/GOw7+UywbxorDyj+rh0unvcPLYE3nD/K9O/sh3YFNqWbqboF58CREXq9FpWSuaFmijcu6YvQe6GMhvwn6cN0E7X8XIioOesdFPh2pj8NI4XbJwFrju45PvKdQeTGv44rrdEc2W1rUDCuihnCV4A/jQeArpGbd+3OByBVj4kIo3C4Uj1WpCnpIaHof72XRoJEgrt/LC5nQojj0qsFC/oih5g7VTorTfosEpp5YuYOzhnDKP7MjRVzS6rSF/eboeaPknGQ8iStZXdMcaX+yUu7ZYiS3bslY/fs914ylPGNqCaFLuDChG0kt+3FiXe4ER7bnNKtfkGfG1Johj6v7xyAR//nrbzglG1011/eh6gA2NJCKWyXLmAvgcYr6i3uCO4jIKTEt4s5uKNZ4unuY3yPBDs6mYQPMd3oJj2Ky34ePo2zQyeDfZgCXFilowopnmtriGy/Lw2/14gtP7xuElz0URsdu7fhh5IZ+FPhh4J1R0Eb13xCP3avw+HZw03tbPHait8Bj13nH42vx2Lsej2+n8XhWy3TW7y3zNS3Te03L9Oa2TP+ZlulfO3w50fvwdSGA78PX1Xh87vdP8Pgp29Vstmcwej3M3/Yw/0nJSm63s3DeGRO0NN/Pz9I+U5EdFr9TrDeQBsgen8aEl80SGatTxatj4/9S0JQtpIDPdgElVVsLxbYNK2DBFgaaFjumEM1nDyHG4Zd+Dpg1t8yePi7mkHdMolU0PXkMFJngEno3UbSyIy/EJicVB35HKLWxBaay6Hpdp2Rutt3IdxwMUhA47ioKPMeFownSIj+ynWjl2Ou1s7YD34ki11mHQKZI9qO17cFOAA/HX3kr17P91doIRz+aWhdNWjCqlhg8dPokes/2V+hMI8N8Rt4ru0DPKGgn6356dvSOw334S9H7w2noVMyfv5LHsZyKVG4qMjEBvxC1Ef3DFzgibLFA6nTHsqY4Vsg5f3HtDuhd5Y7ZaOpz+qcZi/ygQ8juhHVgy+JjSZsR8Phe0bpmIodJrlIM3rSRMnFB8xJLTsPXJGDurWzbxunm4dKQ+grNANPP2t3h32Tff5QV/2t3b/8FltdpAg==
```

The Blueprint is a book that contains:
*   Station with train
*   Another Book that you can place in your hotbar
    *   Pickup
    *   Dropoff

You can select the inner book from the hotbar and cycle through the blueprints with `SHIFT+MOUSE_WHEEL`.

## Random Tip

Instead of going through the Train's Menu to switch it to manual driving, you
can add or remove a wagon.
Modifying the train puts it into manual.

There are two ways:

*   Quickly add a Wagon: Put a Cargo Wagon on Hotbar 4 slot 4, so `SHIFT+4 4 Click` does the trick (if your aim is good). Use `CTRL+Z` to let the bots undo.
*   Quickly remove a wagon: using a deconstruction planner, remove the wagon and
    attach it with `CTRL+Z`. Do not start driving before, or the bots will place
    the wagon at the place you instructed them, while the train will have moved
    on.

    On the handy car train I haul around an empty wagon for just that.

Using `CTRL+Click` on the map adds a temporary waypoint and switches the train to automatic.


## Further Reading

[^1]: <https://southpark.fandom.com/wiki/Handicar>
