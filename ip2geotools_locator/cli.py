# -*- coding: utf-8 -*-

"""Console script for ip2geotools_locator."""
import logging
import click

from ip2geotools_locator import Locator
from ip2geotools_locator.utils import LOGGER as logger

# Arguments and options of Click CLI
@click.command()
@click.argument('ip_address', type=click.STRING, required=False)

@click.option('--generate-map/--no-map', default=True, help="Save calculation data into Folium map. Default: generate map.")
@click.option('-f', '--filename', 'filename', type=click.STRING, default="locations", help="Filaname of Folium map. Default: locations.html.")

@click.option('-a', '--average', 'average', is_flag=True, help="Calculate average location. At least 2 valid DB responses are needed.")
@click.option('-c', '--clustering', 'clustering', is_flag=True, help="Calculate median of provided locations. At least 2 valid DB responses are needed.")
@click.option('-m', '--median', 'median', is_flag=True, help="Calculate location of centroid in data clusters from K-Means model. At least 3 valid DB responses are needed.")

@click.option('--logs/--no-logs', default=True, help="Store calculation progress in ip2geotools-locator.log file. Default level is Info.")
@click.option('-v', '--verbose', count=True, help="Verbose mode.")

@click.option('-l', '--list', 'list_dbs', is_flag=True, help="List all available databases.")
@click.option('--settings', 'settings', is_flag=True, help="Review settings of calculation.")
@click.option('--commercial', 'commercial', is_flag=True, help="Use all commercial databases.")
@click.option('--noncommercial', 'noncommercial', is_flag=True, help="Use all noncommercial databases.")
@click.option('-d', '--database', 'databases', type=click.STRING, multiple=True, help="Specify databases for calculation. You can select all with asterisk sign.")
@click.option('--save', 'save', is_flag=True, help="Save calculation settings into settings.json file.")

def cmd(ip_address, generate_map, filename, average, clustering, median, logs, verbose, list_dbs, settings, commercial, noncommercial, databases, save):
    """Calculate estimate of geographical location for IPv4 address"""
    # Instance of locator class
    locator = Locator(generate_map, filename)
    stream_handler = logging.StreamHandler()

    # Default stream handler level is Error
    log_level = logging.ERROR
    stream_handler_formatter = logging.Formatter('%(levelname)s: %(message)s')

    #settings for Verbose mode
    if verbose == 1:
        log_level = logging.WARNING
        stream_handler_formatter = logging.Formatter('%(levelname)s: %(module)s - %(message)s')

    if verbose == 2:
        log_level = logging.INFO
        stream_handler_formatter = logging.Formatter('%(levelname)s: %(module)s - %(message)s')

    elif verbose == 3:
        log_level = logging.DEBUG
        stream_handler_formatter = logging.Formatter('%(levelname)s: %(module)s - %(message)s')

    elif verbose >= 4:
        log_level = logging.DEBUG
        stream_handler_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(module)s - %(message)s')

    # Enabling logging module and stream handler
    logger.disabled = False
    logger.setLevel(log_level)
    stream_handler.setFormatter(stream_handler_formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    # Disable loging module if needed
    if logs is False:
        logger.disabled = True

    # List all available databases in settings
    if list_dbs:
        click.echo("\nAvailable databases: ")
        loaded_settings = locator.get_settings()
        for db_type in loaded_settings:
            click.echo("\t%s - " % db_type, nl=False)
            for db_name in loaded_settings[db_type]:
                click.echo("%s, " % db_name, nl=False)
            click.echo(" ")

    # Adjust settings if needed. Othervise use settings from settings.json file
    if commercial is True or noncommercial is True or len(databases) != 0:
        loaded_settings = locator.get_settings()

        for db_type in loaded_settings:
            for db_name in loaded_settings[db_type]:
                if commercial:
                    try:
                        loaded_settings["commercial"][db_name]["active"] = True
                    except KeyError:
                        loaded_settings["noncommercial"][db_name]["active"] = False
                elif noncommercial:
                    try:
                        loaded_settings["commercial"][db_name]["active"] = False
                    except KeyError:
                        loaded_settings["noncommercial"][db_name]["active"] = True
                else:
                    if "*" in databases:
                        loaded_settings[db_type][db_name]["active"] = True
                    elif db_name in databases:
                        loaded_settings[db_type][db_name]["active"] = True
                    else:
                        loaded_settings[db_type][db_name]["active"] = False

        locator.set_settings(loaded_settings)

    # Show running configuration.
    if settings:
        click.echo("\nSelected databases: ")
        loaded_settings = locator.get_settings()
        for db_type in loaded_settings:
            click.echo("\t%s - " % db_type, nl=False)
            for db_name in loaded_settings[db_type]:
                if loaded_settings[db_type][db_name]["active"]:
                    click.echo("%s, " % db_name, nl=False)
            click.echo(" ")

    click.echo(" ")

    # If no IP address provided show help and exit
    if ip_address is not None:

        # Split ip address into octets
        octets = ip_address.split(".")
        # Ceck number of octets
        if len(octets) != 4:
            click.echo("IP address is not valid!\nProvided IP address does not have four octets.", err=True)
            exit(1)
        # Validate ip address
        for index, octet in enumerate(octets):
            int_octet = int(octet)
            if int_octet not in range(0, 256):
                click.echo("IP address is not valid!\n%i octet value must be between 0 and 255" % index, err=True)
                exit(1)

        # Find location data for provided IP address
        locator.fetch_locations(ip_address)
        # Get dictionary of found locations
        locations = locator.get_locations()

        # No location found
        if len(locations) == 0:
            click.echo("\nNo record for IP address %s in selected databases." % ip_address)
            exit(0)

        # No calculation selected, return location data
        if (average is False and clustering is False and median is False):
            click.echo("\nApplication retrieved %i DB responses." % len(locations))
            for location in locations:
                click.echo("Location data from %s database - Latitude: %.3f, Longitude %.3f, Country: %s, Region: %s, City: %s"% (location, locations[location].latitude, locations[location].longitude,
                                                                                                                                  locations[location].country, locations[location].region,
                                                                                                                                  locations[location].city))
        # Run calculations and retun location data
        else:
            calculated_locations = locator.calculate(average=average, clustering=clustering, median=median)
            # Reprot for successfull calculation
            if calculated_locations is not None:
                click.echo("\nCalculated location(s) were estimated from %i DB responses." % len(locations))
                for calc_loc in calculated_locations:
                    click.echo("Location estimated by %s calculation method is: Latitude - %f, Longitude - %f" % (calc_loc, calculated_locations[calc_loc].latitude,
                                                                                                                  calculated_locations[calc_loc].longitude))
            # Report for unsuccessfull calculation
            else:
                click.echo("\nCalculation has not been finished. Returning location data. Please review logs form more datails.")
                for location in locations:
                    click.echo("Location data from %s database - Latitude: %.3f, Longitude %.3f, Country: %s, Region: %s, City: %s" % (location, locations[location].latitude,
                                                                                                                                       locations[location].longitude,
                                                                                                                                       locations[location].country,
                                                                                                                                       locations[location].region,
                                                                                                                                       locations[location].city))

        # Inform user about saved location file
        if generate_map:
            click.echo("\nAll location data saved into %s.html file. You can now open it in your web browser." % filename)

    # Inform user aboud saved settings
    if save:
        click.echo("Settings are saved in settings.json file.")
        locator.save_settings()
    # Handling for empty IP address parameter
    if ip_address is None:
        click.echo("No IP address provided. Use --help to see available options of application.")
        exit(0)
