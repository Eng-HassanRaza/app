#!/bin/bash


ROOT_DIR="web/templates"

files='
401.html
404.html
500.html
account.html
account2.html
#article_long.html
#articlelist.html
ask.html
company.html
#favorite.html
index.html
kiyaku.html
leave.html
login.html
manage.html
privacypolicy.html
profile.html
profile_long.html
profile_long_private.html
signup.html
thanks.html
about.html
'

for f in $files; do
  if [[ "$f" = \#* ]] ; then
    echo "skip ${f}"
  else
    gsed -i -e "s:^<!DOCTYPE html>$:{% load static %}\n<!DOCTYPE html>:g" ${ROOT_DIR}/${f}

    gsed -i -e "s: src=\"images/\([^\"]*\): src=\"{% static '/images/\1' %}:g" ${ROOT_DIR}/${f}
    gsed -i -e "s: src=\"\./images/\([^\"]*\): src=\"{% static '/images/\1' %}:g" ${ROOT_DIR}/${f}
    gsed -i -e "s: href=\"css/\([^\"]*\): href=\"{% static '/css/\1' %}:g" ${ROOT_DIR}/${f}
    gsed -i -e "s: src=\"js/\([^\"]*\): src=\"{% static '/js/\1' %}:g" ${ROOT_DIR}/${f}

    gsed -i -e "s:<a href=\"account.html\">:<a href=\"/account\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"account2.html\">:<a href=\"/account\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"ask.html\">:<a href=\"/ask\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"company.html\">:<a href=\"/company\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"index.html\">:<a href=\"/\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"kiyaku.html\">:<a href=\"/tos\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"leave.html\">:<a href=\"/leave\">:g" ${ROOT_DIR}/${f}

    gsed -i -e "s:<a href=\"login.html\">:<a href=\"/login\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"manage.html\">:<a href=\"/manage\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"privacypolicy.html\">:<a href=\"/policy\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"profile.html\">:<a href=\"/profile/edit/\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"profile_long.html\">:<a href=\"/profile/\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"signup.html\">:<a href=\"/signup\">:g" ${ROOT_DIR}/${f}
    gsed -i -e "s:<a href=\"thanks.html\">:<a href=\"/thanks\">:g" ${ROOT_DIR}/${f}
  fi

done