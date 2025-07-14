# Toolbox
## Ubuntu git credential manager setup (HTTPS)
### Install and configure GCM
```
sudo apt update
sudo apt install gnome-keyring
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
sudo apt --fix-broken install
git-credential-manager configure
git config --global credential.credentialStore secretservice
```
### In case of error try these
```
sudo apt install gnome-keyring
```
```
sudo apt install libsecret-1-dev
```

## Ubuntu mouse lag fix
```
sudo su -
modprobe drm_kms_helper
echo N> /sys/module/drm_kms_helper/parameters/poll
echo 'drm_kms_helper' >> /etc/modules-load.d/local.conf
echo "options drm_kms_helper poll=N" >> /etc/modprobe.d/local.conf
```

## Git branch name in CLI (Ubuntu)
### In ~/.bashrc replace this:
```
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```
### with this:
```
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
if [ "$color_prompt" = yes ]; then
 PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
else
 PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w $(parse_git_branch)\$ '
fi
```