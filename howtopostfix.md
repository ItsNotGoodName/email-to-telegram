Install postfix and cyrus sasl
```
sudo pacman -S cyrus-sasl posftix
```

Add following to main.cf
```
myorigin = localhost.com
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain, localhost.com

smtpd_sasl_path = smtpd
smtpd_sasl_auth_enable = yes

maillog_file = /var/log/postfix.log
```

Create `/etc/sasl2/smtpd.conf`
```
pwcheck_method: saslauthd
mech_list: PLAIN LOGIN
```

Use shadow file for sasl
```
saslauthd -a shadow
```
Create the user



