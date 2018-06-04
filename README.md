# RSS Beacons

This repo contains a simple RSS beacon for use with [SaltStack](https://saltstack.com/). 

You configure a beacon to watch one or more RSS feeds that will be monitored for changes. An event will be published when a change is seen in any of the configured RSS feeds.

## Requirements

[FeedParser](https://pypi.org/project/feedparser/)

## How to Use it

- Add gitfs to Salt see [this link](https://docs.saltstack.com/en/develop/topics/tutorials/gitfs.html) for a walkthrough on doing this

```
# /etc/salt/master.d/fileserver.conf
fileserver_backend:
  - roots
  - git
```

- Add this repo to your gitfs repos

```
# /etc/salt/master.d/gitfs.conf
gitfs_remotes:
  - https://github.com/SaltStackExperiments/rss_beacon.git
```

- Install the [FeedParser](https://pypi.org/project/feedparser/) library for the Python version you are using
- Add a configuration for this beacon to /etc/salt/minion.d/beacons.conf
  - see `enable_beacon/files/rss_beacon.conf` for an example

```
beacons:
  rss:
    url: 
      - https://xkcd.com/rss.xml
      - https://www.brainyquote.com/link/quotebr.rss
    interval: 1800 # Every 30 minutes
```
  
- Setup a reactor to monitor for rss events. The tag will look something like `salt/beacon/<master_id>/rss/<rss_url>/newentry`

- Watch for all events like this:
  - tag: `salt/beacon/*/rss/*/newentry`

```yaml
# /etc/salt/master.d/reactor.conf
reactor:                              # Master config section "reactor"
  - 'salt/beacon/*/rss/*/newentry':   # Match tag 
    - /srv/reactor/event_received.sls # Things to do when a new RSS entry event is seen
```
