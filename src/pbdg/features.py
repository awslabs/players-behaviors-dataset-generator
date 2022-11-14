# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from os.path import exists
import random
import pandas as pd
from enum import Enum
from functools import reduce, partial
from pbdg.common import *

ONE_MINUTE_IN_SECONDS = 60
ONE_HOUR_IN_SECONDS = ONE_MINUTE_IN_SECONDS * 60
ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24
ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7
ONE_MONTH_IN_SECONDS = ONE_WEEK_IN_SECONDS * 4

class Counter:
    def __init__(self, count, total):
        self.count = count
        self.total = total

    def __iadd__(self, increment):
        self.count += increment
        return self    

class FeatureName(Enum):
    cohort_id = 0
    cohort_day_of_week = 1
    player_id = 2
    player_type = 3
    player_lifetime = 4
    player_churn = 5
    session_count = 6
    last_minute = 7
    last_hour = 8
    last_day = 9
    last_week = 10
    last_month = 11

    @classmethod
    def last_minute_suffix(cls, minute, prefix):
        return f'_{prefix}_{cls.last_minute.name}(-{minute})'

    @classmethod        
    def last_hour_suffix(cls, hour, prefix):
        return f'_{prefix}_{cls.last_hour.name}(-{hour})'        

    @classmethod
    def last_day_suffix(cls, day, prefix):
        return f'_{prefix}_{cls.last_day.name}(-{day})'

    @classmethod
    def last_week_suffix(cls, week, prefix):
        return f'_{prefix}_{cls.last_week.name}(-{week})'

    @classmethod
    def last_month_suffix(cls, month, prefix):
        return f'_{prefix}_{cls.last_month.name}(-{month})'

    @classmethod
    def names(cls):
        return list(map(lambda e: e.name, cls))

class FeatureVariant(Enum):
    count = 0
    time_of_day_mean = 1
    time_of_day_std = 2

    @classmethod
    def names(cls):
        return list(map(lambda e: e.name, cls))

def extract_cohort_id(player_events):
    first_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[0]
    return {FeatureName.cohort_id.name: first_session_timestamp.strftime("%Y_%m_%d")}

def extract_cohort_day_of_week(player_events):
    first_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[0]
    return {FeatureName.cohort_day_of_week.name: first_session_timestamp.day_of_week}   

def extract_player_type(player_events):
    player_type = player_events[PlayerEventField.player_type.name].iat[0]
    return {FeatureName.player_type.name: player_type}

def extract_player_session_count(player_events):
    player_session_count = player_events[PlayerEventField.session_id.name].drop_duplicates().size
    return {FeatureName.session_count.name: player_session_count}

def extract_player_lifetime(player_events):
    first_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[0]
    last_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[-1]
    player_lifetime = (last_session_timestamp - first_session_timestamp).total_seconds()
    return {FeatureName.player_lifetime.name: player_lifetime}  

def extract_player_churn(player_events, timestamp, days):
    features = dict()
    
    last_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[-1]
    inactive_days = (timestamp - last_session_timestamp).days
    if inactive_days > days:
        features[FeatureName.player_churn.name] = True
    else:
        features[FeatureName.player_churn.name] = False

    return features

def extract_player_events_by_time_periods(player_events, minutes, hours, days, weeks, months, operator, prefix):
    
    def extract_player_events_by_time_period(player_events_by_elapsed_time_periods, time_period, suffixer):
        features = dict()
    
        for time in range(0, time_period):
            feature_suffix = suffixer(time+1)
            if time in player_events_by_elapsed_time_periods.groups:
                player_events_by_elapsed_time_period = player_events_by_elapsed_time_periods.get_group(time).groupby(PlayerEventField.event_type.name)
                for event_type in PlayerEventType:
                    feature_name = f'{event_type.name.lower()}{feature_suffix}'
                    if event_type.name in player_events_by_elapsed_time_period.groups:  
                        player_events_by_elapsed_time_period_and_event_type = player_events_by_elapsed_time_period.get_group(event_type.name)
                        features[feature_name] = operator(player_events_by_elapsed_time_period_and_event_type)
                    else:
                        features[feature_name] = 0
            else:
                for event_type in PlayerEventType:
                    features[f'{event_type.name.lower()}{feature_suffix}'] = 0
        
        return features
    
    features = dict()

    last_session_timestamp = player_events[PlayerEventField.timestamp.name].iat[-1]

    elapsed_time_in_seconds = 'elapsed_time_in_seconds'
    elapsed_time_in_minutes = 'elapsed_time_in_minutes'
    elapsed_time_in_hours = 'elapsed_time_in_hours'
    elapsed_time_in_days = 'elapsed_time_in_days'
    elapsed_time_in_weeks = 'elapsed_time_in_weeks' 
    elapsed_time_in_months = 'elapsed_time_in_months' 

    player_events[elapsed_time_in_seconds] = player_events[PlayerEventField.timestamp.name].apply(lambda d: int((last_session_timestamp-d).total_seconds()))
    player_events[elapsed_time_in_minutes] = player_events[elapsed_time_in_seconds] // ONE_MINUTE_IN_SECONDS 
    player_events[elapsed_time_in_hours] = player_events[elapsed_time_in_seconds] // ONE_HOUR_IN_SECONDS
    player_events[elapsed_time_in_days] = player_events[elapsed_time_in_seconds] // ONE_DAY_IN_SECONDS
    player_events[elapsed_time_in_weeks] = player_events[elapsed_time_in_seconds] // ONE_WEEK_IN_SECONDS
    player_events[elapsed_time_in_months] = player_events[elapsed_time_in_seconds] // ONE_MONTH_IN_SECONDS

    features.update(extract_player_events_by_time_period(player_events.groupby(elapsed_time_in_minutes), minutes, partial(FeatureName.last_minute_suffix, prefix=prefix)))
    features.update(extract_player_events_by_time_period(player_events.groupby(elapsed_time_in_hours), hours, partial(FeatureName.last_hour_suffix, prefix=prefix)))
    features.update(extract_player_events_by_time_period(player_events.groupby(elapsed_time_in_days), days, partial(FeatureName.last_day_suffix, prefix=prefix)))
    features.update(extract_player_events_by_time_period(player_events.groupby(elapsed_time_in_weeks), weeks, partial(FeatureName.last_week_suffix, prefix=prefix)))
    features.update(extract_player_events_by_time_period(player_events.groupby(elapsed_time_in_months), months, partial(FeatureName.last_month_suffix, prefix=prefix)))

    return features

def extract_player_events_count(player_events_by_elapsed_time_period_and_event_type):
    return player_events_by_elapsed_time_period_and_event_type[PlayerEventField.id.name].count()

def extract_player_events_time_of_day_mean(player_events_by_elapsed_time_period_and_event_type):
    timestamp = player_events_by_elapsed_time_period_and_event_type[PlayerEventField.timestamp.name].mean()
    timedelta = timestamp - pd.Timestamp(year=timestamp.year, month=timestamp.month, day=timestamp.day)
    return timedelta.total_seconds()
    
def extract_player_events_time_of_day_std(player_events_by_elapsed_time_period_and_event_type):
    return player_events_by_elapsed_time_period_and_event_type[PlayerEventField.timestamp.name].std().total_seconds()

def extract_features(player_events, extractors, counter):
    def extract(features, extractor):   
        extracted_features = extractor(player_events)
        return {**features, **extracted_features}

    counter += 1
    print_progress_bar(counter.count, counter.total+1, prefix = 'generating features:', suffix = '', length = 50)
    
    return pd.Series(reduce(extract, extractors, dict()))

class FeaturesOptions:

    def __init__(self, churn_days, last_minutes, last_hours, lasy_days,
                                last_weeks, last_months):
        self.churn_days = churn_days
        self.last_minutes = last_minutes
        self.last_hours = last_hours
        self.last_days = lasy_days
        self.last_weeks = last_weeks
        self.last_months = last_months

def generate_player_features(game_events, features_options):

    game_events[PlayerEventField.timestamp.name] = pd.to_datetime(game_events[PlayerEventField.timestamp.name])
    game_events = game_events.sort_values(by=[PlayerEventField.timestamp.name])
    game_events_by_player_id = game_events.groupby(PlayerEventField.player_id.name)

    # add player ids

    player_count = len(game_events_by_player_id.indices)
    player_features = pd.DataFrame()
    player_features[FeatureName.player_id.name] = game_events[PlayerEventField.player_id.name].drop_duplicates()
    player_features.set_index(keys=FeatureName.player_id.name, inplace=True)

    # extract features

    churn_timestamp = game_events[PlayerEventField.timestamp.name].iat[-1]
    churn_days = features_options.churn_days

    extract_player_events = partial(
        extract_player_events_by_time_periods, 
        minutes=features_options.last_minutes, 
        hours=features_options.last_hours, 
        days=features_options.last_days, 
        weeks=features_options.last_weeks, 
        months=features_options.last_months, 
    )
    
    counter = Counter(1, player_count)
    
    features_extractor = partial(
        extract_features, 
        extractors=[
            extract_cohort_id,
            extract_cohort_day_of_week,
            extract_player_type,
            extract_player_lifetime,
            extract_player_session_count,
            partial(extract_player_churn, 
                    timestamp=churn_timestamp, 
                    days=churn_days),
            partial(extract_player_events,
                    operator=extract_player_events_count,
                    prefix=FeatureVariant.count.name),
            partial(extract_player_events,
                    operator=extract_player_events_time_of_day_mean,
                    prefix=FeatureVariant.time_of_day_mean.name),
            partial(extract_player_events,
                    operator=extract_player_events_time_of_day_std,
                    prefix=FeatureVariant.time_of_day_std.name)
        ],
        counter = counter
    )
    
    print_progress_bar(counter.count, counter.total+1, prefix = 'generating features:', suffix = '', length = 50)
    
    extracted_features = game_events_by_player_id.apply(features_extractor)
    player_features = pd.merge(player_features, extracted_features, left_index=True, right_index=True)

    return player_features

def generate(filename, events, churn_days, last_minutes, last_hours, 
             last_days, last_weeks, last_months, seed, overwrite, debug):
    
    # set seed

    random.seed(seed)

    # load game events

    print('loading events...')
    events_file = f'{events}.csv'
    if not exists(events_file):
        print(f'{events_file} does not exist!')
        return
    events_dataframe = pd.read_csv(events_file)
    print('events loaded!')

    # generate machine learning features

    features_file = f'{filename}.csv'
    
    if not exists(features_file) or overwrite:
        
        features_options = FeaturesOptions(
            churn_days,
            last_minutes,
            last_hours,
            last_days,
            last_weeks,
            last_months
        )
        features_dataframe = generate_player_features(events_dataframe, features_options)

        print('storing features...')
        features_dataframe.to_csv(features_file)
        print(f'features stored in {features_file}!')
        
    else:
        
        print(f'{features_file} already exists, use --overwrite to replace the current features!')