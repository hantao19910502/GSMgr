#!/bin/bash



#起服check.起服
check_start(){
    ssh $1 "cd $3
    bin/lcserver \`sh run.sh args $2\`&
    pid=\$!
    sleep 1
    
    lc=\`ps axu|grep -w $2|grep -v grep|wc -l\`
    if [ \"\$lc\" -ne 1 ]
    then 
        echo -e \"\033[49;31;5;1m\$lc\033[49;31;0m\"
        echo -e \"\033[49;31;5;1m$2 starting fail\033[49;31;0m\"
        exit 1
    else 
        npid=\`ps axu|grep -w $2|grep -v grep|awk '{print \$2}'\`
        nnpid=\`echo \$npid|sed 's/[\t\n ]/b/g'\`
        if [ "\$npid" -eq "\$nnpid" ]
        then
            kill \$npid
            cd $3
            sh run.sh start $2
        fi
    fi"
}
check_start $1 $2 $3
