# -*- coding: utf-8 -*-

"""Console script for ip2geotools_locator."""
import logging
import click

from ip2geotools_locator import Locator

LOCATOR = Locator()

@click.group()
@click.option('--logs/--no-logs', default=False)
def cmd(logs):
    """Console script for ip2geotools_locator."""
    logger = logging.getLogger()

    if logs is False:
        logger.disabled = True

@cmd.command()
@click.argument('ip_address', type=click.STRING)

@click.option('-g', '--generate-map', 'gen_map', is_flag=True)

@click.option('-a', '--average', 'average', is_flag=True)
@click.option('--no-average', 'average', flag_value=False, default=True)
@click.option('-c', '--clustering', 'clustering', is_flag=True)
@click.option('-m', '--median', 'median', is_flag=True)

@click.option('--commercial', 'commercial', is_flag=True)
@click.option('--noncommercial', 'noncommercial', is_flag=True)
@click.option('-d', '--database', 'database', type=click.STRING, multiple=True)
# pylint: disable=too-many-arguments
def locate(ip_address, gen_map, average, clustering, median, commercial, noncommercial, database):
    """Calculate estimate of geographical location for IP address"""
    databases = []

    match = ip_address.split(".")
    # pylint: disable=too-many-boolean-expressions, literal-comparison
    if (len(match) is not 4 or int(match[0]) < 0 or int(match[0]) > 255 or int(match[1]) < 0 or
            int(match[1]) > 255 or int(match[2]) < 0 or int(match[2]) > 255 or int(match[3]) < 0 or
            int(match[3]) > 255):
        click.echo("IP address is not valid!")
        exit(1)

    if commercial is True:
        databases.append("commercial")

    elif noncommercial is True:
        databases.append("noncommercial")

    else:
        databases = list(database)
    LOCATOR.generate_map = gen_map
    LOCATOR.get_locations(ip_address, databases)

    calculated_locations = LOCATOR.calculate(average=average, clustering=clustering, median=median)

    for calc_loc in calculated_locations:
        click.echo("Location estimated by %s is: %f N, %f E" %
                   (calc_loc, calculated_locations[calc_loc].latitude,
                    calculated_locations[calc_loc].longitude))


@cmd.command()
def setup():
    """Database setup:"""
