#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Script to check for active hosts and shutdown the server if necassary."""
# TODO:
# - add cmd arguments
# - change os.system and os.popen to subprocess

#import logging
from optparse import OptionParser
import logging.handlers
import os


def server_down():
    """Main function of this script."""
    # parse cmd line arguments
    parse_arguments()

    # init the logger
    logger = init_logger()

    if statistics:
        gen_statistics()
    else:
        # get list of hosts from /etc/hosts
        hosts = get_hosts(logger)

        # check if any of the hosts are still alive
        no_clients_alive = check_hosts(logger, hosts)

        # if no clients are alive, shutdown the system
        if (no_clients_alive == True):
            log_traffic(logger)
            shutdown_system(logger)
        else:
            pass


def parse_arguments():
    """Parse command line arguments"""
    pass
    parser = OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="use debug mode")
    parser.add_option("-s", "--statistics", action="store_true", dest="statistics", help="parse log file and generate statistics. This assumes that the log file is \"well\" formatted. This omits the whole shutdown mechanism.")

    (options, args) = parser.parse_args()

    global debug
    global statistics

    debug = False
    statistics = False

    if options.debug:
        debug = True
    if options.statistics:
        statistics = True


def init_logger():
    """Init and return logger."""
    # get logger object
    logger = logging.getLogger('server_down')
    logger.setLevel(logging.DEBUG)
    # set file handle for log file
    # use a rotating log file with max 200kb and backup up to 3 log files
    error = False

    global logfile

    try:
        logfile = '/var/log/server_down.log'
        log_fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=200000, backupCount=3)
    except IOError:
        logfile = './server_down.log'
        log_fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=200000, backupCount=3)
        error = True
    log_fh.setLevel(logging.DEBUG)
    # set formatter for logger
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)-8s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    log_fh.setFormatter(formatter)
    # add file handle to logger
    logger.addHandler(log_fh)

    logger.info("==========")

    # check if /var/log was not accessible.
    # Of course we can't log there to inform the user that we could not log there :-(
    if (error == True):
        logger.error("Could not open file /var/log/server_down.log. Using this file instead!")

    return logger


def get_hosts(logger):
    """Get host list from a file."""
    logger.info("Getting hosts from file /etc/hosts...")
    # open hosts file
    hosts_fh = open("/etc/hosts", "r")
#    hosts_fh = open("/home/erebos/temp/fake_hosts", "r")
    hosts_list = []

    # check for valid IPv4 entries
    # TODO: improve check for valid addresses (maybe regexp)
    for line in hosts_fh:
        temp = line.split()
        if temp and temp[0].count('.') == 3:
            hosts_list.append(temp[0])

    # filter for blacklist
    # TODO: exclude own ip addresses (e.g. through ifconfig)
    black_list = ['127.0.0.1', '127.0.1.1', '192.168.10.2', '192.168.10.17']
    hosts_list = list(set(hosts_list) - set(black_list))

    return hosts_list


def check_hosts(logger, hosts):
    """Check hosts using fping."""
    logger.info("Checking for active hosts...")
    # join hosts to string
    hosts_string = ' '.join(hosts)
    # build command
    cmd = 'fping -a ' + hosts_string + ' | wc -l'
    # execute command
    cmdfd = os.popen(cmd, "r")
    # get return value from commandline
    ret = ""
    for line in cmdfd:
        ret = line

    logger.info(str(ret).strip('\n') + " active host(s) detected!")

    # check if no clients are alive
    if int(ret) != 0:
        return False
    else:
        return True


def log_traffic(logger):
    """Do some logging before shutting down"""
    # open /proc/net/dev to look for net statistics
    fd_traffic = open("/proc/net/dev")

    # read away the first two lines
    fd_traffic.readline()
    fd_traffic.readline()

    # filter the data from the file in a array/dict
    stats = []
    for line in fd_traffic:
        line = line.split()
        stats.append({"iface": line[0].strip(":"), "RX": line[1], "TX": line[9]})

    # output data to logger
    logger.info("Traffic since last shutdown:")
    for data in stats:
        logger.info("\tInterface: " + data["iface"] + "\tRX: " + bytes_to_SI(int(data["RX"])) + "\tTX: " + bytes_to_SI(int(data["TX"])))


def shutdown_system(logger):
    """Shut down the system."""
    logger.info("Shutting down system in 5 seconds")
    # shutdown system with a 5 second delay to exit python
    if debug:
        print "DEBUG: System would shut down!"
    else:
        os.system('/sbin/shutdown -h 1')


def bytes_to_SI(num):
    """Function to convert byte count to readable form.
    Taken out of lib hurry.filesize
    """
    for dimension in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, dimension)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def SI_to_bytes(num):
    temp = num.split()
    ret = 0
    if temp[1] == "bytes":
        ret = float(temp[0])
    if temp[1] == "KB":
        ret = float(temp[0]) * 1000
    if temp[1] == "MB":
        ret = float(temp[0]) * 1000000
    if temp[1] == "GB":
        ret = float(temp[0]) * 1000000000
    if temp[1] == "TB":
        ret = float(temp[0]) * 1000000000000
    return ret


def gen_statistics():
    # data stucture:
    # [{date:DATE, time:TIME, data:{{if:{RX:data,TX:data}},{if:{RX:data,TX:data}}}}, ...]
    data = parse_log()
    
    # generate some output
    fh = open('./server_down.html', 'w')
    # write header...
    fh.write("<html>\
        <table border=\"1\">\
        <tr>\
        <th>Time</th>\
        <th>Date</th>\
        <th>Received</th>\
        <th>Send</th>\
        <th>Traffic/Day</th>\
        </tr>")

    sumRXTX = 0
    count = 0
    for entry in data:
        fh.write("<tr>")

        fh.write("<td>" + entry["time"] + "</td>")
        fh.write("<td>" + entry["date"] + "</td>")
        fh.write("<td>" + str(bytes_to_SI(entry["data"]["eth0"]["RX"])) + "</td>")
        fh.write("<td>" + str(bytes_to_SI(entry["data"]["eth0"]["TX"])) + "</td>")
        temp = entry["data"]["eth0"]["RX"] + entry["data"]["eth0"]["TX"]
        sumRXTX = sumRXTX + temp
        count = count + 1
        fh.write("<td>" + str(bytes_to_SI(temp)) + "</td>")
        fh.write("</tr>")

    # write footer...
    fh.write("</table>")

    avg = sumRXTX / count
    fh.write("Average: " + str(bytes_to_SI(avg)))

    fh.write("</html>")
    

def parse_log():
    fh = open(logfile, 'rb')
    status = 0

    data = []
    index = 0
    for line in fh:
        if line.find('Shutting down system in 5 seconds') != -1:
            status = 0
            index = index + 1
        if status == 1:
            # get dict for if
            ifdict = data[index]["data"]
            # split line
            splitline = line.split()
            # parse data for if
            ifdata = {}
            ifdata[splitline[7].strip(":")] = SI_to_bytes(splitline[8] + " " + splitline[9])
            ifdata[splitline[10].strip(":")] = SI_to_bytes(splitline[11] + " " + splitline[12])
            # store if data           
            ifdict[splitline[6]] = ifdata
        if line.find('Traffic since last shutdown') != -1:
            status = 1
            splitline = line.split()
            data.append({})
            data[index]["date"] = splitline[0]
            data[index]["time"] = splitline[1]
            data[index]["data"] = {}
    fh.close()
    return data


if __name__ == '__main__':
    server_down()
















