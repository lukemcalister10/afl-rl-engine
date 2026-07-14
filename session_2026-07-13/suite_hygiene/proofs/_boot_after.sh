set -euo pipefail                        # bootstrap.sh header AFTER
M=$(md5sum /home/claude/__NO_SUCH_STORE__ | cut -c1-8)
echo "REACHED-PAST-PIPE M=[$M]"
