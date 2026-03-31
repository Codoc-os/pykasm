#!/bin/bash

BASE_PATH="$(dirname "$0")"
source "$BASE_PATH/colors.sh"
EXIT_CODE=0

echo ""

################################################################################
#                                 AUTOFLAKE                                    #
################################################################################
echo -n  "${Cyan}Fixing code with autoflake... $Color_Off"
autoflake kasm/ -ri
echo "${Green}Ok ✅ $Color_Off"
echo ""

################################################################################
#                                   ISORT                                      #
################################################################################
echo -n "${Cyan}Formatting import with isort... $Color_Off"
out=$(isort kasm/)
if [ ! -z "$out" ] ; then
  echo ""
  echo -e "$out"
fi
echo "${Green}Ok ✅ $Color_Off"
echo ""


################################################################################
#                                   BLACK                                      #
################################################################################
echo -n "${Cyan}Formatting code with black... $Color_Off"
out=$(black -l 120 kasm/ 2>&1)
if [[ "$out" == *"reformatted"* ]]; then
  echo ""
  echo -e "$out"
fi
echo "${Green}Ok ✅ $Color_Off"
echo ""


################################################################################
#                                PYCODESTYLE                                   #
################################################################################
echo -n "${Cyan}Checking code style with pycodestyle... $Color_Off"
out=$(poetry run pycodestyle kasm/)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################
#                                PYDOCSTYLE                                    #
################################################################################
echo -n "${Cyan}Checking docstring style with pydocstyle... $Color_Off"
out=$(pydocstyle --count kasm/)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################
#                                   MYPY                                       #
################################################################################
echo -n "${Cyan}Checking typing with mypy... $Color_Off"
out=$(mypy kasm/ --disallow-untyped-def)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################
#                                  BANDIT                                      #
################################################################################
echo -n "${Cyan}Checking security issues bandit... $Color_Off"
out=$(bandit --ini=setup.cfg -ll 2> /dev/null)
if [ "$?" -ne 0 ] ; then
  echo "${Red}Error !$Color_Off"
  echo -e "$out"
  EXIT_CODE=1
else
  echo "${Green}Ok ✅ $Color_Off"
fi
echo ""


################################################################################


if [ $EXIT_CODE = 1 ] ; then
   echo "${Red}⚠ You must fix the errors before committing ⚠$Color_Off"
   exit $EXIT_CODE
fi
echo "${Purple}✨ You can commit without any worry ✨$Color_Off"
