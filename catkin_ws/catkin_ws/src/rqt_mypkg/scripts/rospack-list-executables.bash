#!/bin/bash

# if [[ $# -lt 1 ]]; then
#     echo "usage: $(basename $0) <pkg_name>"
#     echo ""
#     echo "       To get a list of all package names use the command"
#     echo "          'rospack list-names'"
#     exit
# fi

# pkgname=${1}

# #pkgdir="$(catkin_find --first-only --without-underlays --libexec ${pkgname})"
# #pkgdir="$(rospack find ${pkgname})"
# pkgdirs="$(catkin_find --without-underlays ${pkgname})"
# pkgdirs=(${pkgdirs// / })

# if [[ -n "${pkgdirs}" ]]; then
#    #find -L "${pkgdir}" -executable -type f ! -regex ".*/[.].*" ! -regex ".*${pkgdir}\/build\/.*" -print0 | tr '\000' '\n' | sed -e "s/.*\/\(.*\)/\1/g" | sort
#     for pkgdir in ${pkgdirs[@]} ;
#         do
#             if [[ -n "${pkgdir}" ]]; then
#                 find -L "${pkgdir}" -executable -type f ! -regex ".*/[.].*" ! -regex ".*${pkgdir}\/build\/.*" -print0 | tr '\000' '\n' | sed -e "s/.*\/\(.*\)/\1/g" | sort
#             fi 
#         done
# else
#     echo "Cannot find package '${pkgname}'." >&2
#     exit 1
# fi
