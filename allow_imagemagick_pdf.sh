#!/bin/bash

msg="$(convert xc:none pdf:- 2>&1 | grep -i pdf)"
policy="$(grep 'rights=\"none\" pattern=\"PDF\"' /etc/ImageMagick-6/policy.xml)"

if [[ ("$msg" == *"not authorized"* || "$msg" == *"not allowed"*) && policy != "" ]]
then
    cp /etc/ImageMagick-6/policy.xml{,.backup}
    sed -i '/rights="none" pattern="PDF"/d' /etc/ImageMagick-6/policy.xml
fi
