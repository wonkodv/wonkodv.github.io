+++
title               = "Sudo Button"
description         = "Press a button on your U2F instead of typing the sudo password"
taxonomies.category = ["Using Unix"]
taxonomies.tags     = ["u2f", "sudo"]
+++

Sudo Button
===========

You can configure PAM to accept u2f as an authentication mechanism for using
`sudo`.

1.  Install `pam_u2f`.
1.  Add the following line to the top  of `/etc/pam.d/sudo`:
    ```
    auth sufficient pam_u2f.so authfile=/etc/u2f_keys
    ```
1.  Generate `/etc/u2f_keys` by executing `pamu2fcfg`.

This is especially useful inside neovim when you execute `:w ! sudo dd of=%` to
write a root owned file. In VIM, you would get the `sudo-askpass` password prompt, but in
neovim the command is executed in a different session that has no access to your
tty so it can not ask you for your password. With this setup, your u2f button
blinks and you push it.
