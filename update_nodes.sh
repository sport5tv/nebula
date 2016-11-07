#!/bin/bash

for SERVER in '192.168.32.10' '192.168.32.11' '192.168.32.187'; do
    echo ""
    echo "****** UPDATING $SERVER *******"
    echo ""
    ssh root@$SERVER "cd /opt/nx.server && git pull"
done
