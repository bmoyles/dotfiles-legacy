#
# $Id$
#

# source this in the profile.
KILL_STRAY_AGENTS=1
AGENT_FILE_DIR="${HOME}/.ssh/agents/${HOSTNAME}"
AGENT_FILE="${AGENT_FILE_DIR}/ssh-agent.env"
AGENT_CMD="/usr/bin/ssh-agent -s -t 8h"
PIDOF=$(which pidof)


kill_agent_if_running() {
    # kill any stray agents running that we don't have env info for
    # make sure to limit it to processes we own!
    AGENT_PIDS=$(${PIDOF} ssh-agent)
    if [ "x" == "x${AGENT_PIDS}" ]; then
        # if we have nothing running, just return
        return 1
    fi
    # iterate the pids returned by pidof, kill the ones we own using ssh-agent
    # assuming ssh-agent does some cleanup
    for AGENT_PID in ${AGENT_PIDS}; do
        AGENT_UID=$(ps n -f --no-headers -p ${AGENT_PID} | awk '{print $1}')
        if [ "${UID}" == "${AGENT_UID}" ]; then
            export SSH_AGENT_PID=${AGENT_PID} && eval $(/usr/bin/ssh-agent -k)
        fi
    done
}

run_ssh_agent() {
    if [ ${KILL_STRAY_AGENTS} -eq 1 ]; then
        kill_agent_if_running
    fi
    ${AGENT_CMD} > ${AGENT_FILE} 2>/dev/null
    /bin/chmod 600 ${AGENT_FILE}
    source ${AGENT_FILE}
    /usr/bin/ssh-add
}

start_ssh_agent() {                
        if [ ! -d ${AGENT_FILE_DIR} ]; then
            # we assume that if the agent file dir is running, we're setting up for the
            # first time
            mkdir -p ${AGENT_FILE_DIR}
            run_ssh_agent
        elif [ -f ${AGENT_FILE} ]; then
            source ${AGENT_FILE}
            if [ "x${SSH_AGENT_PID}" == "x" ]; then
                # if we have an empty or broken agent file that doesn't properly set
                # SSH_AGENT_PID, restart
                run_ssh_agent
            else
                # if we have 
                /bin/ps -p $SSH_AGENT_PID | grep ssh-agent >& /dev/null
                if [ $? != 0 ]; then
                    run_ssh_agent
                fi
            fi
        else
            # no agent file means we are fresh
            run_ssh_agent
        fi
}

# vim:filetype=sh ts=4 sw=4 sts=4 expandtab
