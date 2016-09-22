#!/usr/bin/env ksh


typeset SN=$(hostname)
typeset F_DOWNLOAD_FLUME="False"


########################################################################################################
##
## used to test network connection
##
##   TestTcp hmc111:22,hmc122:22
##
##   hmc111:22:Connected
##   hmc122:22:Connected
##
alias TestTcp="perl -le 'use IO::Socket;@SvrList=split(\",\",\$ARGV[0]);
\$Conn=0;\$i=0;
while (\$i<@SvrList)
{
  (\$Addr,\$Port)=split(\":\",\$SvrList[\$i]); \$i++;
  if (\$sock = new IO::Socket::INET (PeerAddr => \$Addr, PeerPort => \$Port, Timeout=>1, Proto => 'tcp'))
  {print STDOUT \"\$Addr:\$Port:Connected\"}
  else {print STDOUT \"\$Addr:\$Port:Failed\"}
  close(\$sock);
};'"



export TZ=BEIST-8
function get_time { date +%Y-%m-%d','%T; }


function log {
    typeset msg=$*
    echo "#[INF][$(get_time)] ${SN} :  ${msg}"
}


function logerr {
    typeset msg=$*
    echo "#[ERR][$(get_time)] ${SN} :  ${msg}"
}


function logdeb {
    typeset msg=$*
    echo "#[DEB][$(get_time)] ${SN} :  ${msg}"
}


function logwar {
    typeset msg=$*
    echo "#[WAR][$(get_time)] ${SN} :  ${msg}"
}


function download_flume_from_ftp {
    log "downloading flume from 10.1.18.36"
    cd /opt;
    case $(uname) in
    Linux)
        curl -O ftp://ho198606:password@10.1.18.36/flume.tar
        typeset rtcode=$?
            ;;
    AIX)
        ftp -n  <<EOF
open 10.1.18.36
user ho198606 password
bin
get flume.tar
by
EOF
        typeset rtcode=$?
            ;;
    esac
    if [[ rtcode -eq 0 ]]
    then
        F_DOWNLOAD_FLUME="True"
    else
        logerr "error found when download flume from cmbyum : $rtcode"
        return
    fi
    #
    tar xvf flume.tar
    rm -f flume.tar
}


function download_flume_from_yum {
    # check connectivity to cmbyum.cmbchina.cn
    typeset check=$(TestTcp 10.1.250.3:80|awk -F':' '{print $NF}')
    if [[ ${check} != "Connected" ]]
    then
        logerr "could not reach cmbyum.cmbchina.cn"
        return
    fi
    cd /opt;
    curl -O http://cmbyum.cmbchina.cn/flume.tar
    typeset rtcode=$?
    if [[ rtcode -eq 0 ]]
    then
        F_DOWNLOAD_FLUME="True"
    else
        logerr "error found when download flume from cmbyum : $rtcode"
        return
    fi
    tar xvf flume.tar
}


function download_flume_from_nim {
    typeset ip=$1
    [[ -z ${ip} ]] && return
    scp "operator:tank@MATRIX"@${ip}:/soft/rs6000/flume/flume.tar .
}


function download_flume_for_aix {
    logdeb "func download_flume_for_aix"
    typeset check=$(TestTcp 10.1.18.36:21|awk -F':' '{print $NF}')
    if [[ ${check} == "Connected" ]]
    then
        download_flume_from_ftp
        return
    fi
    # check nim
    typeset nim_ip_list="10.0.170.124 10.3.139.25 10.0.9.113  10.3.128.128"
    # for nim_ip in ${nim_ip_list}
    # do
    #     check=$(TestTcp ${nim_ip}:22|awk -F':' '{print $NF}')
    #     if [[ ${check} == "Connected" ]]
    #     then
    #         download_flume_from_nim ${nim_ip}
    #         break
    #     fi
    # done
    
    # get nim server from /etc/niminfo
    typeset ip
    if [[ -s /etc/niminfo ]]
    then
        ip=$(awk '/^export NIM_HOSTS=/ {split($(NF-1),a,":"); print a[1];}' /etc/niminfo)
    fi
    # if failed to get nim ip, try every possible ones
    if [[ -z ${ip} ]]
    then
        log "trying every nim server"
        for ip in ${nim_ip_list}
        do
            check=$(TestTcp ${ip}:2049|awk -F':' '{print $NF}')
            if [[ ${check} == "Connected" ]]
            then
                break
            fi
        done
    fi
    #  
    if [[ -z ${ip} ]]
    then
        logerr "failed to get nim server"
        return
    fi
    #
    function check_nfs_mount {
        mount 2>/dev/null|awk '
        $4~"nfs" && $2=="/soft" && $3=="/mnt" {print $0;}'
    }
    # mount nm:/soft to /mnt
    mount ${ip}:/soft /mnt
    typeset rtcode=$?
    if [[ rtcode -gt 0 && -z $(check_nfs_mount) ]]
    then
        logerr "failed to mount ${ip}/soft"
        return
    fi
    # copy flume.tar
    typeset source="/mnt/rs6000/flume/flume.tar"
    if [[ ! -s ${source} ]]
    then
        logerr "missing ${source} on ${ip}"
        umount /mnt
        return
    fi
    cp ${source} /opt
    rtcode=$?
    if [[ rtcode -eq 0 ]]
    then
        F_DOWNLOAD_FLUME="True"
    else
        logerr "error when copying flume.tar : ${rtcode}"
        umount /mnt
        return
    fi
    cd /opt
    tar xvf flume.tar
    umount /mnt
}


function download_flume {
    log "func download_flume"
    case $(uname) in
    AIX)
        download_flume_for_aix
            ;;
    Linux)
        # check connectivity to 10.1.18.36
        typeset check=$(TestTcp 10.1.18.36:21|awk -F':' '{print $NF}')
        if [[ ${check} == "Connected" ]]
        then
            download_flume_from_ftp
            # logerr "could not reach 10.1.18.36"
            # return
        else
            logwar "could not reach 10.1.18.36"
            download_flume_from_yum
        fi
        # log "downloading flume from 10.1.18.36"
        # cd /opt;
        # curl -O ftp://ho198606:password@10.1.18.36/flume.tar
        # tar xvf flume.tar
        # rm -f flume.tar

        if [[ ${F_DOWNLOAD_FLUME} == "True" ]]
        then
            log "flume has been successfully downloaded"
        else
            logerr "failed to download flume"
            return
        fi

        # check user opswareusr 
        if [[ -z $(id opswareusr 2>/dev/null) ]]
        then
            log "creating user opswareusr"
            useradd -c "sysadmin_maintenance_low_previleged_account-$(date +%Y%m%d)" opswareusr
        fi
        # chowner
        cd /opt
        chown -R opswareusr:opswareusr flume
        log "starting flume agent"
        su - opswareusr -c /opt/flume/bin/run-flume-daemon.sh
            ;;
    esac
}

function adaptive_conf_toflume {
    typeset conf1="/opt/flume/conf/flume-conf.properties"
    typeset conf2="/opt/flume/conf/collect-conf.properties"
    typeset conf3="/opt/flume/conf/predator-conf.properties"
    for conf in $conf1 $conf2 $conf3
    do
        if [[ -f ${conf} ]]
        then
            echo $conf
        fi
    done
}

function add_config {
    # typeset conf="/opt/flume/conf/flume-conf.properties"
    #typeset conf="/opt/flume/conf/collect-conf.properties"
    typeset conf=$(adaptive_conf_toflume)
    if [[ -z $conf ]]
    then
        logerr "flume config file is not exists and exit the programe!"
        exit 188
    fi
    log "flume config file is $conf"
    log "checking flume existence"
    # check if flume has been installed
    if [[ ! -f ${conf} ]]
    then
        logerr "missing file :  ${conf}"
        typeset old_conf="/opt/flume/conf/flume-conf.properties"
        if [[ -f  ${old_conf} ]]
        then
            logerr "flume verison has not been updated"
        else
            logerr "flume has not been installed"
        fi
        exit 100
        # download_flume
    else
        log "flume has been installed"
    fi
    # check again
    if [[ ! -f ${conf} ]]
    then
        logerr "failed to download flume"
        return
    fi
    # check platform
    typeset key1 key2
    case $(uname) in
    AIX)
        key1="process";
        key2="netconn";
            ;;
    Linux)
        key1="linux.process";
        key2="linux.netconn";
            ;;
    esac
    # check if process and netconn has been added
    # sample:
    #   varLogDir4.analyser=varLogDir4-an
    #   varLogDir4.path=/usr/local/scripts/apps
    #   varLogDir4.pattern=^(process.csv)$
    #   varLogDir4.instant=true
    #   varLogDir4.isRecursive=false
    #   varLogDir4-an.encode=UTF-8
    #   varLogDir4-an.position=-1
    #   varLogDir4-an.extends.SOURCE_TYPE=opsware
    #   varLogDir4-an.extends.TOPIC=app.process
    if [[ -z $(grep -w "TOPIC=app.${key1}" ${conf}) ]]
    then
        targets="${key1}"
    fi
    if [[ -z $(grep -w "TOPIC=app.${key2}" ${conf}) ]]
    then
        targets="${targets} ${key2}"
    fi
    #
    log "checking if collect-conf.properties has been set already"
    typeset num_of_targets=$(echo $targets|awk '{print NF}')
    if [[ num_of_targets -eq 0 ]]
    then
        log "nothing need to be done"
        return
    fi
    # sample:
    # process.watcher=varLogDir2 varLogDir3 varLogDir varLogDir4
    log "generating new labels for flume conf setting"
    typeset num=$(awk -F'=' '
                  $1=="process.watcher" {
                      split($2,a," ");
                      x=0;
                      for(t in a) {
                          if(a[t]!~"varLogDir[0-9]") continue;
                          num=a[t]; sub(/varLogDir/,"",num); if(x<num) x=num;
                      }
                      print x+1; exit;
                  }' ${conf})
    typeset labels label
    typeset check
    typeset counter=0
    while [[ num -lt 999 && counter -lt num_of_targets ]]
    do
        label="varLogDir${num}"
        check=$(awk -v label="${label}" '
                $1=="dirs" {
                    for(i=3;i<=NF;i++) {
                        if($i==label) { print $i; exit; };
                    };
                }' ${conf})
        ((num+=1))
        if [[ ! -z ${check} ]]
        then
            # logerr "label confict, abort : ${label}"
            continue
        fi
        [[ -z ${labels} ]] && labels=${label} || labels="${labels} ${label}"
        ((counter+=1))
    done
    #
    log "generating content for flume conf setting"
    # add label to head
    typeset content
    # content=$(awk -v labels="${labels}" -v targets="${targets}" '
    #     $1=="dirs" {
    #         printf "%s %s\n",$0,labels;
    #         num=NF-2+split(labels,a," ");
    #     }
    #     $1=="dirs.thread" {
    #         printf "%s = %s\n",$1,num;
    #     }
    #     $1!="dirs" && $1!="dirs.thread" { print $0; }
    #     END {
    #         len=split(targets,a," "); split(labels,b," ");
    #         for(i=1;i<=len;i++) c[a[i]]=b[i];
    #         for(key in c) {
    #             label=c[key];
    #             printf "\n";
    #             printf "dirs.%s.path = /usr/local/scripts/apps\n",label;
    #             len=split(key,fn,"."); fkey=fn[len];
    #             printf "dirs.%s.file-pattern = \^(%s.csv)\$\n",label,fkey;
    #             printf "dirs.%s.cpusleep = 200\n",label;
    #             printf "dirs.%s.bufMax = 1048576\n",label;
    #             printf "dirs.%s.code = GBK\n",label;
    #             printf "dirs.%s.redFromBegin = false\n",label;
    #             printf "dirs.%s.otherInfo = SOURCE_TYPE,,opsware\n",label;
    #             printf "dirs.%s.isWindows = false\n",label;
    #             printf "dirs.%s.encode = 0\n",label;
    #             printf "dirs.%s.topic = app.%s\n",label,key;
    #         }
    #     }' ${conf} 2>/dev/null)

    #
    # sample:
    # varLogDir5.analyser=varLogDir5-an
    # varLogDir5.path=/usr/local/scripts/apps
    # varLogDir5.pattern=^(netconn.csv)$
    # varLogDir5.instant=true
    # varLogDir5.isRecursive=false
    # varLogDir5-an.encode=UTF-8
    # varLogDir5-an.position=-1
    # varLogDir5-an.extends.SOURCE_TYPE=opsware
    # varLogDir5-an.extends.TOPIC=app.netconn
    #
    # sample:
    # process.watcher=varLogDir2 varLogDir3 varLogDir varLogDir4
    #
    content=$(awk -v labels="${labels}" -v targets="${targets}" -F'=' '
        $1=="process.watcher" {
            printf "%s %s\n",$0,labels;
        }
        $1!="process.watcher" { print $0; }
        END {
            len=split(targets,a," "); split(labels,b," ");
            for(i=1;i<=len;i++) c[a[i]]=b[i];
            for(key in c) {
                label=c[key];
                printf "\n";
                printf "%s.analyser=%s-an\n",label,label;
                printf "%s.path=/usr/local/scripts/apps\n",label;
                len=split(key,fn,"."); fkey=fn[len];
                printf "%s.file-pattern = \^(%s.csv)\$\n",label,fkey;
                printf "%s.instant=true\n",label;
                printf "%s.isRecursive=false\n",label;
                printf "%s-an.encode=UTF-8\n",label;
                printf "%s-an.position=-1\n",label;
                printf "%s-an.extends.SOURCE_TYPE=opsware\n",label;
                printf "%s.TOPIC=app.%s\n",label,key;
            }
        }' ${conf} 2>/dev/null)
    
    # backup flume-conf.properties before update
    typeset nf="${conf}.sav.$(date +%Y%m%d.%H%M%S)"
    log "backup config file to ${nf}"
    cp ${conf} ${nf}

    # update flume-conf.properties
    log "updating flume-conf.properties"
    echo "${content}" > ${conf}

    # restarting flume process
    restart_flume_process

    #
    return
}


function restart_flume_process {
    # identify running user
    typeset list=$(ps -eo ruser,pid,comm,args|awk '
                   $3=="java" && $0~"/opt/flume/" { printf "%s|%s ",$1,$2; }')
    if [[ -z ${list} ]]
    then
        log "failed to detect flume process"
        return
    fi
    #
    log "killing flume process"
    for comp in ${list}
    do
        user=$(echo "${comp}"|cut -f1 -d'|')
        # on linux you just get user id, deal with it
        if [[ -z $(id ${user} 2>/dev/null) ]]
        then
            user=$(awk -F':' -v id="${user}" '
                   $3==id {print $1;exit;}' /etc/passwd)
        fi
        pid=$(echo "${comp}"|cut -f2 -d'|')
        cmd="su - ${user} \"-c kill ${pid}\""
        log "$cmd"
        eval ${cmd}
    done
    # start flume
    log "starting flume process"
    cmd="su - ${user} -c /opt/flume/bin/run-flume-daemon.sh"
    log "${cmd}"
    eval "$cmd"
}


function set_yum_linux {
    # check redhat realease
    typeset release_version=$(awk '
        {
            for(i=1;i<=NF;i++) {
                if($i~"[0-9]") { x=$i; break; };
            };
            split(x,a,"."); print a[1];
        }' /etc/redhat-release)
    typeset cmd
    case ${release_version} in
    5) cmd="wget http://cmbyum.cmbchina.cn/rhel5.repo; cp -f rhel5.repo /etc/yum.repos.d/" ;;
    6) cmd="wget http://cmbyum.cmbchina.cn/rhel6.repo; cp -f rhel6.repo /etc/yum.repos.d/" ;;
    7) cmd="wget http://cmbyum.cmbchina.cn/rhel7.repo; cp -f rhel7.repo /etc/yum.repos.d/" ;;
    *) ;;
    esac
    if [[ -z ${cmd} ]]
    then
        logerr "does not support version [${release_version}]"
        return
    fi
    # # remove old yum repo config file in /etc/yum.repo.d
    # cmd=$(find /etc/yum.repos.d -type f | awk '
    #       $1!~"rhel-source.repo$" { printf "mv %s /tmp;\n",$1; }')
    # if [[ ! -z ${cmd} ]]
    # then
    #     log "removing old yum repo config file"
    #     eval ${cmd}
    #     yum clean all
    # fi
    #
    log "download yum config file from cmbyum.cmbchina.cn"
    eval ${cmd}
    yum clean
    yum makeache
}


#
# TODO: check if yum has been correctly configured
#
function install_java_on_linux {
    # check connectivity to cmbyum.cmbchina.cn
    log "checking network connection to cmbyum.cmbchina.cn"
    typeset check=$(TestTcp 10.1.250.3:80|awk -F':' '{print $NF}')
    if [[ ${check} != "Connected" ]]
    then
        logerr "could not connect to cmbyum.cmbchina.cn"
        return
    fi
    # check if cmbyum.cmbchina.cn could be resolve
    log "checking if cmbyum.cmbchina.cn could be resolved"
    if [[ -z $(ping -w 1 -c 1 cmbyum.cmbchina.cn 2>/dev/null) ]]
    then
        log "adding cmbyum.cmbchina.cn to /etc/hosts"
        echo "10.1.250.3    cmbyum.cmbchina.cn" >> /etc/hosts
    fi
    # check if yum has been configured
    log "checking if repo has been configed"
    # yum clean
    # typeset num=$(yum repolist 2>/dev/null|awk '
    #               $1=="repolist:" {print $2}')
    # if [[ $num == "0" ]]
    # then
    #     set_yum_linux
    # fi

    # remove old yum repo config file in /etc/yum.repo.d
    cmd=$(find /etc/yum.repos.d -type f | awk '
          $1!~"rhel[5,6,7].repo$" { printf "mv %s /tmp;\n",$1; }')
    log "cmd = [$cmd]"
    if [[ ! -z ${cmd} ]]
    then
        log "removing old yum repo config file"
        eval ${cmd}
        yum clean all
        set_yum_linux
    fi

    # install jdk
    yum install java-1.7.0-openjdk.x86_64 -y
    return
    # check redhat realease
    typeset release_version=$(awk '
        {
            for(i=1;i<=NF;i++) {
                if($i~"[0-9]") { x=$i; break; };
            };
            split(x,a,"."); print a[1];
        }' /etc/redhat-release)
}


# check if java has been installed
function check_java {
    case $(uname) in
    AIX) return ;;
    esac
    log "checking if java has been installed"
    # for SuSE
    if [[ -s /etc/SuSE-release ]]
    then
        handle_java_on_suse
        return
    fi
    # check if not redhat
    check_linux_release
    # for redhat
    if [[ -z $(which java 2>/dev/null) ]]
    then
        logerr "java has not been installed yet"
        install_java_on_linux
    fi
    # check again
    if [[ -z $(which java 2>/dev/null) ]]
    then
        logerr "failed to install jdk-1.7.0"
        return
    fi
}


function handle_java_on_suse {
    # typeset java=$(/usr/bin/which java 2>/dev/null)
    # log "java= $java"
    typeset java="/opt/jdk1.6.0_38/bin/java"
    if [[ ! -s ${java} ]]
    then
        logerr "failed to locate java for SuSe"
        return
    fi
    # make soft link /usr/bin/java
    if [[ ! -f /usr/bin/java ]]
    then
        log "making soft link /usr/bin/java -> ${java}"
        ln -s ${java} /usr/bin/java
    fi
    return
}


function check_linux_release {
    if [[ ! -s /etc/redhat-release ]]
    then
        logwar "not RedHat, skip"
        exit 0
    fi
}


function backup_crontab_linux {
    log "backup crontab file"
    typeset conf="/var/spool/cron/root"
    if [[ ! -s ${conf} ]]
    then
        log "crontab $conf has not been set"
        return
    fi
    typeset fname="root.sav.$(date +%Y%m%d.%H%M%S)"
    typeset nf="/var/spool/cron/${fname}"
    log "backup [root] to [${fname}]"
    log "cp ${conf} ${nf}"
    cp ${conf} ${nf}
}


function backup_crontab_aix {
    log "backup crontab file"
    typeset conf="/var/spool/cron/crontabs/root"
    if [[ ! -s ${conf} ]]
    then
        log "crontab $conf has not been set"
        return
    fi
    typeset fname="root.sav.$(date +%Y%m%d.%H%M%S)"
    typeset nf="/var/spool/cron/crontabs/${fname}"
    log "backup [root] to [${fname}]"
    log "cp ${conf} ${nf}"
    cp ${conf} ${nf}
}


function check_flume_daemon {
    # check root crontab, set flume daemon if not
    #     # flume log collecting-20150902
    #     * * * * * su - opswareusr -c /opt/flume/bin/run-flume-daemon.sh
    log "checking flume daemon"
    if [[ ! -z $(crontab -l 2>/dev/null|grep "/opt/flume/bin/run-flume-daemon.sh") ]]
    then
        log "flume daemon has been set already"
        return
    fi
    # backup crontab first
    typeset cron_file
    case $(uname) in
    Linux)
        cron_file="/var/spool/cron/root"
        backup_crontab_linux
            ;;
    AIX)
        cron_file="/var/spool/cron/crontabs/root"
        backup_crontab_aix
            ;;
    esac
    # add item
    function echo_content {
        echo "# flume daemon @$(get_time)"
        echo "* * * * * su - opswareusr -c /opt/flume/bin/run-flume-daemon.sh"
    }
    # typeset conf="/var/spool/cron/root"
    log "adding run-flume-daemon.sh to ${cron_file}"
    echo_content >> ${cron_file}
}


function main {
    [[ $1 == "-s" && ! -z $2 ]] && SN=$2
    check_java
    add_config
    check_flume_daemon
}

main $*
exit $?
