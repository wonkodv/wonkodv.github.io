+++
title               = "A Short Code for Factorio Rich Text in Zola"
description         = "Adding a shortcode that shows in-game rich text in my blog"
taxonomies.category = ["Programming"]
taxonomies.tags     = ["factorio", "rust", "zola", "tera", "regex"]
date                = 2022-01-04
+++

# A Short Code for Factorio Rich Text in Zola

Yesterday I wanted to write a [quick post](@/factorio/automate_personal_transport_with_handy_car.md) about a neat little blueprint I made in factorio.

I typed it out, took some screenshots, and decided that I should just polish it
a little and put it online. 
Factorio has Rich Text which turns `[item=iron-plate]` into
{{ factorio_string(body="[item=iron-plate]") }}. I thought I'd add a little
[short code](https://www.getzola.org/documentation/content/shortcodes/) and
continue playing.

At the start of every little project is a thought like

> That shouldn't take any time at all.\
> It's just a little Regex to replace `[X=Y]`
> with `<img src="factorio.com/images/X/Y.png">`

And I wasn't entirely wrong.

## Adding Regex to Zola

[Zola](https://www.getzola.org/)
uses
[Tera](https://tera.netlify.app/) as template engine,
and Tera does not have a regex-replace.
Zola didn't add one either.
But it's open source and I know a little rust so this should be easy right?

I modified Zola a little to have a `regex_replace` filter.
This is registered with `tera.register_filter` in `tpls.rs` (that name tho).

After maybe an hour, I could use `regex_replace` in Zola templates (and thereby shortcodes). (Could have been closer to 2 hours?).
It's useful enough that I thought it might even be added to Zola.

## Writing the Short Code

10 minutes later I had the short code working using a regex that replaced the
rich text elements with `<img>` tags that did not resolve yet, everything else
was good.

```jinja
<span style="background-color: #444344; color: #f1f1f1;" title="{{ body }}">
    {{- body | escape | regex_replace(
        pattern="\[(?P<type>[^\]=]+)=(?P<name>[^\]=]+)]",
        replace="<img src='example.com/factorio/$1/$2.png' alt='$0'>"
    ) | safe -}}
</span>
```


The entire text is put into a span with dark background and the unmodified text
as title.

The Regex does:
*   Match `[`
*   Capture Group with name `type`
    *   Match 1 or more characters that are not `]` or `=`
*   Match `=`
*   Capture Group with name `name`
    *   Match 1 or more characters that are not `]`
*   Match `]`

## Finding the Icons

Ok. Hard part done, now to the easy part.
Finding a URL that hosts `/item/iron-ore.png` should be easy cause there is
this great wiki and 100 fan sites, blueprint editors, ...


Spoiler: finding icons is hard, you can skip this section.


No, nothing is ever easy. I Closed the game and browsed through all the factorio
links I keep around.

The wiki does this media wiki thing of using capitalized names and have a
[wiki-syntax template](https://wiki.factorio.com/Template:Icon/doc)
to deal with it.
(It has 467 characters, 186 of which are `! " # . / : ; < = > [ ] { | }`)

The blueprint editor I looked at does some canvas magic and
the resources are hidden in some javascript thing.

2 fan sites have the image base64 encoded in a css style sheet.

There is [factorioiconselect.com](https://www.factorioiconselect.com/) that has
sane URLs but they made up there own schema (steam is in `fluid/misc/steam.png`)
and don't have the character icon.

[Factorio Lab](https://factoriolab.github.io/) has all the icons in one png:
{{ image(path="zola-shortcode-factorio/sprites.png", alt="all icons in one file", width=400, center=true) }}

It is worth mentioning at this point, that templates in Zola/Tera have some scripting
support but not a full programming languages like python or lua with a huge string
manipulation library (because those projects do NOT WANT one).
Templates are supposed to be templates not programs.

I realized I probably have all the files on my local machine anyway, most likely
even with good file names because why would the devs make their own life harder?

I did the easy thing and put a symlink to the graphics directory of my factorio
install (`/base/graphics/icons/`) into the blog's static directory.
There is an `icons/` directory with all the items and fluids.

Feeling good, I spent an hour writing a first draft of this post.

Going back to the rich text short code I realized `character.png` was missing
(for when you have  `[entity=character]`).
That is __the only one__ which I wanted to use in the post I was actually trying to write.
I did find `entity/bigass-explosion/` which made me smile but did not help.

I later found the character icon in `/core/graphics/icons/entity/` (core not base).

Placing the symlink to graphics in `static` ensures that all graphics end up in
my public directory, so I removed the symlink and only copied the images I need.

I then noticed, that those "icons" are not icons as I understand them, but icons as a game
engine understands them. 4 images of different resolution inside the same png.
But, I can use the trick with css `background-position` I picked up on the way
and make an `<img>` with a transparent pixel as `src` and the "icon" as
background, using a constant offset. It somehow worked out that the second
resolution fits nicely in my line.
As soon as I change anything about the line size this will probably break and
future me will have to write a script that crops the image instead and places
*normal* icons in my static folder.

## The Final Short Code

`templates/shortcodes/factorio_string.html` now looks like this:

```jinja
<span style="background-color: #444344; color: #f1f1f1; padding-x:0 2px;" title="{{ body }}">
    {{- body | escape | regex_replace(
        pattern="\[(?P<type>[^\]=]+)=(?P<name>[^\]=]+)]",
        replace="<img
            src='/factorio/transparent.gif'
            style='
                background-image:url(&quot;/factorio/${name}.png&quot;);
                background-position: -95px 2px;
                height:1.3em;
                width:1em;
                margin:-4px 0;'
            alt='$0'>"
    ) | safe -}}
</span>
```
