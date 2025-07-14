## Ubuntu git credential manager setup (HTTPS)
### Install and configure GCM
```
sudo apt update
sudo apt install gnome-keyring
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
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

