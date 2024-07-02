+++
title               = "Security of Bookmarklets"
description         = "Use `javascript:` bookmarks to enhance website functionality (or get your identity stolen)"
date                = 2024-03-07
# updated           = 2023-07-29
taxonomies.category = ["Web"]
taxonomies.tags     = ["javascript", "web", "security"]
+++

# Bookmarklets Are Cool


Bookmarklets are bookmarks that start with `javascript:`.
Power users like them, to add functionality to a site.

Here, I'm listing the ones that I usually have with me.
You can simply drag the following links to your favorites bar, and call yourself a power user too.


*   <a href= "javascript:window.open('http://chart.apis.google.com/chart?cht=qr&chs=500x500&chl='+encodeURIComponent(document.location.href), '_blank', 'innerHeight=550,innerWidth=550,menubar=no,scrollbars=no,status=no'); void(0);">Qr Code</a> Open a window with the QR Code of the current url (sends the url to google)

*   [Scroll Top](javascript:scroll(0,0);void(0);) Scroll to the top of the page.

*   <a href="javascript:document.location.href+=&quot;&list=ULcxqQ59vzyTk&quot; ;" onmousedown="this.href='javascript:document.location.href+=&quot;&list=ULcxqQ59vzyTk&quot;;                                                            if(document.location.host.search(&quot;youtube&quot;)>0)console.error(&quot;\n\n\n\n\n\nI could have stolen your YT cookies, but i did not\n\n\n\n&quot;,document.cookie);'" onclick=" this.href='javascript:document.location.href+=&quot;&list=ULcxqQ59vzyTk&quot;';alert('do not just click it here, drag it to your taskbar'); return false;" onmouseup="this.href='javascript:document.location.href+=&quot;&list=ULcxqQ59vzyTk&quot;'" ondragstart="this.href='javascript:document.location.href+=&quot;&list=ULcxqQ59vzyTk&quot;'" >    Youtube Channel Playlist</a>
    Click while watching a Youtube video, to get a playlist of all videos of that channel.
    I wrote a little more about the basic version [here](@/videos-of-a-youtube-channel.md).
    But this is the enhanced version.

## Dragging Links is Dangerous

When you use the last one, you get the desired effect.
But I also put an error entry in your browser's debugging console with your YT cookies. How did that happen?
The url changes in the `onmosedown` event. The changed url is put in the Bookmark. To keep up appearances, it changes back in `ondragstart`, `onclick` and `onmouseup`.
The changed url has some additional javascript, where I could do all kinds of shenanigans.

Chromium (v122) will just accept this.

Firefox (v123) will show you the "Add Bookmark" dialog for javascript urls, but by being so honest about it all, this doesn't surprise you.
The evil part comes after enough whitespaces, that you don't see it.

## Is this a Bug ?

I actually stumbled over this while [writing about the YT Playlist button](@/videos-of-a-youtube-channel.md),
so I opened security bugs for firefox and chromium.


### Chromium

<https://issues.chromium.org/issues/40059144?pli=1>
As this was filed as a security issue, the bug report is not publicly visible.

The severity of the vulnerability was set to low, as this XSS involves user interaction and users could be "social engineered" into dragging a `javascript:` link directly.
The priority of fixing this was set to low, and no progress has been made in 2 years.

### Firefox

<https://bugzilla.mozilla.org/show_bug.cgi?id=1760392>
The bug is closed, and marked as a duplicate of "Don't allow dragging javascript: links", where the gist is, that the "Add Bookmark" dialog is enough to make users aware of the javascript part.

## So...

Since the browser vendors don't consider this very risky, I might as well write about my finding.
Could I have tricked you into executing my javascript code in your youtube session?
