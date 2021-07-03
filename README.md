# Venue Finder - API Comparison

## Objective
Compare venue searching APIs: **[Yelp](https://www.yelp.com/developers/documentation/v3/get_started) vs. [Foursquare](https://developer.foursquare.com/places)**.

Determine which API provides:
1. The best city-wide coverage for finding venues.
2. The most accessible and reliable option for building application interfaces.

## Approach
1. Find overlapping categories between the APIs
2. Pull venue data from each API for cities: Vancouver BC Canada, New Westminster BC Canada, Toronto ON Canada, New York NY USA.
3. Store data in SQLite database.
4. Analyze differences to answer objectives.

## Stack
* APIs - Python (requests, json)
* Database - Python (sqlite3) / SQL
* Analysis - Python (numpy, pandas) / SQL
