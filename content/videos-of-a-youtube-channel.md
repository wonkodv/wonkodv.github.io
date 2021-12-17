+++
title               = "Playlist of all Videos of a Youtube Channel"
description         = "Get a playlist of a youtube channel with all videos in chronological order"
date                = 2022-03-15
updated             = 2024-03-07
taxonomies.category = ["Web"]
taxonomies.tags     = ["javascript"]
+++

# View All videos of a Youtube channel

For most youtube channels I watch, I want a playlist of all videos that channel ever released, sorted from oldest to newest.
This is unofficially supported by adding:

    &list=ULcxqQ59vzyTk

to a video link. If you have

    https://www.youtube.com/watch?v=mL3sho1CpkI

you turn it into

    https://www.youtube.com/watch?v=mL3sho1CpkI&list=ULcxqQ59vzyTk

you should now see a playlist, that shows you the video you were at, and some videos that came before and after it.
There is no easy way to navigate to the very beginning or very end, only relative jumps of +- 10 or 20 videos.
It works best if you navigate to the oldest video of the channel yourself, view it, and then add that string to the url.

Although the string looks random it is not tied to a channel. If you search for this feature, you may stumble over posts claiming you only need to add `&list=UL` but this seems to have changed some years
ago. *(The current approach still works as of 2024-03)*

## Create a Javascript Bookmark for the Lazy

You can store bookmarks in your browser with the URL scheme `javascript:` that,
when clicked, will execute javascript in the page you are viewing.
For our purpose, we want to execute:
```javascript
document.location.href += "&list=ULcxqQ59vzyTk";
```
We therefor need to create a bookmark, with a title like "YT Channel Playlist" and a URL of

    javascript:document.location.href += "&list=ULcxqQ59vzyTk";

Now navigate to a video and hit that bookmark to get the channel playlist.

You [should not drag anyone's link into you bookmark bar](@/bookmarklets.md), so the following is just for me:

<a href="javascript:document.location.href+='&list=ULcxqQ59vzyTk';" title="Drag this to your Bookmark Bar">
<div style="display:block;  margin:auto; width:300px; background-color:#c4c4c4; border: 4px solid #bbb; border-color: #aaa #ccc #ccc #aaa; text-align: center; color:black;">
YT Channel Playlist
</div>
</a>
