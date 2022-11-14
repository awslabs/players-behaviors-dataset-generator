# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from datetime import date
import click
from pbdg.common import PlayerEventField, PlayerEventType
import pbdg.events as e
import pbdg.features as f

# events

DEFAULT_EVENTS_FILENAME='events'
DEFAULT_EVENTS_DATE=str(date.today())
DEFAULT_EVENTS_PLAYERS=10
DEFAULT_EVENTS_DAYS=7

# metrics

DEFAULT_METRICS_FILENAME='metrics'

# features

DEFAULT_FEATURES_FILENAME='features'
DEFAULT_FEATURES_CHURN_DAYS=5
DEFAULT_FEATURES_LAST_MINUTES=0
DEFAULT_FEATURES_LAST_HOURS=0
DEFAULT_FEATURES_LAST_DAYS=7
DEFAULT_FEATURES_LAST_WEEKS=3
DEFAULT_FEATURES_LAST_MONTHS=2

# common

DEFAULT_SEED=0
DEFAULT_PLOT=False
DEFAULT_OVERWRITE=False
DEFAULT_DEBUG=False

@click.group()
@click.version_option()
def main():
    pass

@main.command(help=f'''
Generate game events of types ({','.join(PlayerEventType.names())}) with fields ({','.join(PlayerEventField.names())}) in a specified csv filename (default={DEFAULT_EVENTS_FILENAME}).
''')
@click.option('--date', type=click.DateTime(formats=["%Y-%m-%d"]), default=DEFAULT_EVENTS_DATE, help='The players acquisition starting date (default=today)')
@click.option('--players', default=DEFAULT_EVENTS_PLAYERS, help=f'The number of daily acquired players (default={DEFAULT_EVENTS_PLAYERS})')
@click.option('--days', default=DEFAULT_EVENTS_DAYS, help=f'The number of acquisition days (default={DEFAULT_EVENTS_DAYS})')
@click.option('--seed', default=DEFAULT_SEED, help=f'The random seed (default={DEFAULT_SEED})')
@click.option('--plot/--no-plot', default=DEFAULT_PLOT, help=f'The plot flag (default={DEFAULT_PLOT})')
@click.option('--overwrite/--no-overwrite', default=DEFAULT_PLOT, help=f'The overwrite flag (default={DEFAULT_OVERWRITE})')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help=f'The debug flag (default={DEFAULT_DEBUG})')
@click.argument('filename', default=DEFAULT_EVENTS_FILENAME)
def events(filename, date, players, days, seed, plot, overwrite, debug):
    e.generate(filename, date, players, days, seed, plot, overwrite, debug)

@main.command(help=f'''
Generate metrics from game events (not implemented yet)
''')
@click.option('--seed', default=DEFAULT_SEED, help=f'The random seed (default={DEFAULT_SEED})')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help=f'The debug flag (default={DEFAULT_DEBUG})')
@click.option('--events', default=DEFAULT_EVENTS_FILENAME, help=f'The csv filename of the input game events (default={DEFAULT_EVENTS_FILENAME})')
@click.argument('filename', default=DEFAULT_METRICS_FILENAME)
def metrics(filename, events, seed, debug):
    click.echo('not implemented yet!')

@main.command(help=f'''
Generate machine learning features ({','.join(f.FeatureName.names())}) with variants ({','.join(f.FeatureVariant.names())}) for each event type ({','.join(f.PlayerEventType.names())}) in a specified csv filename (default={DEFAULT_FEATURES_FILENAME})
''')
@click.option('--churn-days', default=DEFAULT_FEATURES_CHURN_DAYS, help=f'The number of inactivity days to be flagged as churn (default={DEFAULT_FEATURES_CHURN_DAYS})')
@click.option('--last-minutes', default=DEFAULT_FEATURES_LAST_MINUTES, help=f'The number of minutes to sample before last event date (default={DEFAULT_FEATURES_LAST_MINUTES})')
@click.option('--last-hours', default=DEFAULT_FEATURES_LAST_HOURS, help=f'The number of hours to sample before last event date (default={DEFAULT_FEATURES_LAST_HOURS})')
@click.option('--last-days', default=DEFAULT_FEATURES_LAST_DAYS, help=f'The number of days to sample before last event date (default={DEFAULT_FEATURES_LAST_DAYS})')
@click.option('--last-weeks', default=DEFAULT_FEATURES_LAST_WEEKS, help=f'The number of minutes to sample before last event date (default={DEFAULT_FEATURES_LAST_WEEKS})')
@click.option('--last-months', default=DEFAULT_FEATURES_LAST_MONTHS, help=f'The number of months to sample before last event date (default={DEFAULT_FEATURES_LAST_MONTHS})')
@click.option('--events', default=DEFAULT_EVENTS_FILENAME, help=f'The csv filename of the input game events (default={DEFAULT_EVENTS_FILENAME})')
@click.option('--seed', default=DEFAULT_SEED, help=f'The random seed (default={DEFAULT_SEED})')
@click.option('--overwrite/--no-overwrite', default=DEFAULT_PLOT, help=f'The overwrite flag (default={DEFAULT_OVERWRITE})')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help=f'The debug flag (default={DEFAULT_DEBUG})')
@click.argument('filename', default=DEFAULT_FEATURES_FILENAME)
def features(filename, events, churn_days, last_minutes, last_hours, 
                last_days, last_weeks, last_months, 
                seed, overwrite, debug):
    f.generate(filename, events, churn_days, last_minutes, last_hours, 
                last_days, last_weeks, last_months, 
                seed, overwrite, debug)

if __name__ == '__main__':
    main()