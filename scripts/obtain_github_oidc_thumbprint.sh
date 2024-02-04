###########################
#docs on how to obtain the the thumbprint of an OIDC provider:
#https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
###########################


openssl s_client -servername token.actions.githubusercontent.com \
-showcerts -connect token.actions.githubusercontent.com:443

# obtains the root certificate thumbprint
openssl x509 -in github_root_cert.crt -fingerprint -sha1 -noout \
| sed 's/.*=//;s/://g;y/ABCDEF/abcdef/' \
| pbcopy


