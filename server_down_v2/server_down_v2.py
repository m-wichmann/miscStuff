#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Script to check for active hosts and shutdown the server if necassary."""
# TODO:
# - add cmd arguments
# - change os.system and os.popen to subprocess

#import logging
import logging.handlers
import os


def server_down():
    """Main function of this script."""
    # parse cmd line arguments
    parse_arguments()

    # init the logger
    logger = init_logger()

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
#    parser = OptionParser()
#    parser.add_option("-g", "--generate", action="store_true", dest="generate", help="generate the html documents")
    #parser.add_option("-c", "--configfile", dest="config_file",
    #    help="path to config file with the profiles and show ids",
    #    metavar="FILE")

#    (options, args) = parser.parse_args()

#    if options.clean:
#        self.remove()


def init_logger():
    """Init and return logger."""
    # get logger object
    logger = logging.getLogger('server_down')
    logger.setLevel(logging.DEBUG)
    # set file handle for log file
    # use a rotating log file with max 200kb and backup up to 3 log files
    error = False
    try:
        log_fh = logging.handlers.RotatingFileHandler('/var/log/server_down.log', maxBytes=200000, backupCount=3)
    except IOError:
        log_fh = logging.handlers.RotatingFileHandler('./server_down.log', maxBytes=200000, backupCount=3)
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
        logger.info("\tInterface: " + data["iface"] + "\tRX: " + sizeof_fmt(int(data["RX"])) + "\tTX: " + sizeof_fmt(int(data["TX"])))


def shutdown_system(logger):
    """Shut down the system."""
    logger.info("Shutting down system in 5 seconds")
    # shutdown system with a 5 second delay to exit python
#    print "shutdown!"
    os.system('/sbin/shutdown -h 1')


def sizeof_fmt(num):
    """Function to convert byte count to readable form.
    Taken out of lib hurry.filesize
    """
    for dimension in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, dimension)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


if __name__ == '__main__':
    server_down()
