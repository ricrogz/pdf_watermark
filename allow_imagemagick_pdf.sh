#!/bin/bash

msg="$(convert xc:none pdf:- 2>&1 | grep pdf)"
policy="$(grep 'rights=\"none\" pattern=\"PDF\"' /etc/ImageMagick-6/policy.xml)"

if [[ "$msg" == *"not authorized"* && policy != "" ]]
then
    cp /etc/ImageMagick-6/policy.xml{,.backup}
    sed -i "/PDF/d" /etc/ImageMagick-6/policy.xml
fi
