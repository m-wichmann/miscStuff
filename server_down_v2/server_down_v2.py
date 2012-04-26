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
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from time import time
import matplotlib
from pylab import figure
from datetime import datetime
import glob
import numpy
import matplotlib.pyplot as plt


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
    if debug:
        return True
    else:
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
    generate_graphs_matplotlib(data)
    generate_graphs_R(data)
    
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

    fh.write("</table>")

    try:
        avg = sumRXTX / count
    except ZeroDivisionError:
        avg = 0
    fh.write("Average: " + str(bytes_to_SI(avg)))
    fh.write("<br/>")

    # include all png files that start with "sd_graph_" in html document
    script_path = os.path.realpath(__file__)
    img_path = script_path[0:script_path.rindex("/") + 1]

    for infile in glob.glob( os.path.join(img_path, 'sd_graph_*.png') ):
        fh.write("<img src=\"" + os.path.basename(infile) + "\">")

    fh.write("</html>")
    

def generate_graphs_R(data):
    # requirements: TODO...

    # get r "main" object
    r = robjects.r

    # open device for files
    grdevices = importr('grDevices')
    # set output file
    grdevices.png(file="./sd_graph_r_test.png", width=512, height=512)
    # plot stuff
    x = []
    y = []
    for entry in data:
#        print entry["date"]
#        print entry["time"]
#        print entry["data"]["eth0"]["RX"]
        x.append(entry["time"].replace(":",""))
        y. append(entry["data"]["eth0"]["RX"])

    r.plot(x, y, ylab="foo/bar", xlab="temp", col="red")
    # close device
    grdevices.dev_off()

#    grdevices = importr('grDevices')
#    grdevices.png(file="./file2.png", width=512, height=512)
#    r.plot(x, y, ylab="foo/bar", xlab="temp", col="red")
#    grdevices.dev_off()


def generate_graphs_matplotlib(data):

    # graph: traffic over time
 
    # This version prints only one interface but is fairly clean   
#    dates = []
#    values = []
#    for entry in data:
        # split date and time and convert to matplotlib format
#        time_split = entry["time"].split(":")
#        date_split = entry["date"].split("-")
#        temp = datetime(year = int(date_split[0]), month = int(date_split[1]), day = int(date_split[2]), hour = int(time_split[0]), minute = int(time_split[1]), second = int(time_split[2]))
#        temp = matplotlib.dates.date2num(temp)
#
#        dates.append(temp)
#
#        rx_tx_sum = entry["data"]["eth0"]["RX"] + entry["data"]["eth0"]["TX"]
#        values.append(rx_tx_sum)
#
#    fig = figure()
#    ax = fig.add_subplot(111)
#    ax.plot_date(dates, values, '-')
#    bx = fig.add_subplot(111)
#    bx.plot_date(dates, values, '-')
#    fig.autofmt_xdate()
#    fig.savefig("sd_graph_mpl_traffic_over_time.png")


    # TODO: this version should print all interfaces but is really badly designed!
    graph_data = {}
    if_keys = data[0]["data"].keys()

    for interface in if_keys:
        graph_data[interface] = {"values": []}

    for entry in data:
        for interface in if_keys:
            graph_data[interface]["values"].append({"date":entry["date"], "value":entry["data"][interface]["RX"]})

    fig = figure()

    for entry in graph_data:
        dates = []
        values = []
        for x in graph_data[entry]["values"]:
            date_split = x["date"].split("-")
            temp = datetime(year = int(date_split[0]), month = int(date_split[1]), day = int(date_split[2]))
            temp = matplotlib.dates.date2num(temp)
            dates.append(temp)
            values.append(x["value"])
        ax = fig.add_subplot(111)
        ax.plot_date(dates, values, '-')

    fig.autofmt_xdate()
    fig.savefig("sd_graph_mpl_traffic_over_time.png")





    # graph 2: RX and TX stacked per day
    fig = figure()

    labels = []
    RX = []
    TX = []

    for entry in data:
        labels.append(entry["date"])
        RX.append(int(entry["data"]["eth0"]["RX"]))
        TX.append(int(entry["data"]["eth0"]["TX"]))

    ind = numpy.arange(len(RX))    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, RX, width, color='r')
    p2 = plt.bar(ind, TX, width, color='g', bottom=RX)

    plt.ylabel('Data [byte]')
    plt.title('Data RX/TX per day')
    plt.xticks(ind+width/2., labels )
    plt.yticks(numpy.arange(0,max(RX) + max(TX), (max(RX) + max(TX))/11))
    plt.legend( (p1[0], p2[0]), ('RX', 'TX') )

    plt.savefig("sd_graph_mpl_rx_tx_stacked.png")




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
















