enable_rss_beacon:
  beacon.present:
    - save: True
    - name: rss
    - interval: 5
    - url: http://rss.cnn.com/rss/cnn_topstories.rss

add_beacon_if_not_there:
  module.run:
    - beacons.add:
      name: rss
      beacon_data:
        interval: 5
        url: http://rss.cnn.com/rss/cnn_topstories.rss
    - onfail:
      - enable_rss_beacon
