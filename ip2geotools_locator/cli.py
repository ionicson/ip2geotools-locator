# -*- coding: utf-8 -*-

"""Console script for ip2geotools_locator."""
import logging
import click

from ip2geotools_locator import Locator
from ip2geotools_locator.utils import LOGGER as logger

@click.command()
@click.argument('ip_address', type=click.STRING)

@click.option('-g', '--generate-map', 'gen_map', is_flag=True)

@click.option('-a', '--average', 'average', is_flag=True)
@click.option('-c', '--clustering', 'clustering', is_flag=True)
@click.option('-m', '--median', 'median', is_flag=True)

@click.option('--commercial', 'commercial', is_flag=True)
@click.option('--noncommercial', 'noncommercial', is_flag=True)
@click.option('-d', '--database', 'database', type=click.STRING, multiple=True)
@click.option('--logs/--no-logs', default=False)
@click.option('-v', '--verbose', count=True)

def cmd(logs, verbose, ip_address, gen_map, average, clustering, median, commercial, noncommercial, database):
    """Calculate estimate of geographical location for IP address"""
    locator = Locator(gen_map)
    databases = []
    stream_handler = logging.StreamHandler()

    octets = ip_address.split(".")

    if len(octets) is not 4:
        click.echo("IP address is not valid!\nProvided IP address does not have four octets.")
        exit(1)
    for index, octet in enumerate(octets):
        int_octet = int(octet)
        if int_octet not in range(0, 256):
            click.echo("IP address is not valid!\n%i octet value must be between 0 and 255" % index)
            exit(1)

    if logs is False:
        logger.disabled = True

    if verbose != 0:
        log_level = logging.WARNING
        stream_handler_formatter = logging.Formatter('%(levelname)s: %(module)s - %(message)s')

        if verbose == 2:
            log_level = logging.INFO

        elif verbose == 3:
            log_level = logging.DEBUG

        elif verbose >= 4:
            log_level = logging.DEBUG
            stream_handler_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(module)s - %(message)s')

        logger.disabled = False
        logger.setLevel(log_level)
        stream_handler.setFormatter(stream_handler_formatter)
        stream_handler.setLevel(log_level)
        logger.addHandler(stream_handler)

    if commercial is True:
        databases.append("commercial")

    elif noncommercial is True:
        databases.append("noncommercial")

    else:
        databases = list(database)

    locator.fetch_locations(ip_address)

    if len(locator.locations) == 0:
        click.echo("\n No record for IP address %s in selected databases." % ip_address)
        exit(0)

    if (average is False and clustering is False and median is False):
        print("\n")
        locations = locator.get_locations()
        for location in locations:
            click.echo("Location data from %s database - Latitude: %.3f, Longitude %.3f, Country: %s, Region: %s, City: %s" % (location, locations[location].latitude, locations[location].longitude,
                                                                                                                               locations[location].country, locations[location].region,
                                                                                                                               locations[location].city))
    else:
        calculated_locations = locator.calculate(average=average, clustering=clustering, median=median)
        print("\n")
        for calc_loc in calculated_locations:
            click.echo("Location estimated by %s calculation method is: %f N, %f E" % (calc_loc, calculated_locations[calc_loc].latitude, calculated_locations[calc_loc].longitude))
