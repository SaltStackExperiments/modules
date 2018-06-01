enable_rss_beacon:
  beacon.present:
    - save: True
    - name: rss
    - interval: 5
    - url: http://rss.cnn.com/rss/cnn_topstories.rss
