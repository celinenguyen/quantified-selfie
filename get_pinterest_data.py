import requests, json
import csv
from datetime import datetime
design_board = "design-and-illustration"
pleats_board = "pleats-please"

pin_fields = [
    'created_at',
    # 'description',
    'dominant_color',
    'image_square_url',
    'image_medium_url',
    'is_repin',
    'repin_count',
    'like_count'
    # 'link',
    # 'domain'
  ]

def utf8ify(d):
    return dict((k.encode('utf-8'), v.encode('utf-8')) for k, v in d.iteritems())

def request_boards():
  return "https://api.pinterest.com/v3/users/celinenguyen/boards/"

def request_pins (board = "NONE"):
  if (board == "NONE"):
    return "https://api.pinterest.com/v3/users/celinenguyen/pins/"
  else:
    return "https://api.pinterest.com/v3/boards/celinenguyen/" + board + "/pins/"

# def get_boards:
#   payload = {
#     'access_token': 'MTQzMTU5NDoxMTcwOTM3OTY0NzAwNjMxMDU6MnwxMzY3MTc3NDQ1OjAtLWMxZjliNGFjOTk0YzRmYWI1OTk4NjFmOTRmYzIxYzBhYTVlOGY1Mjk=',
#   }
#   board_fields = [
#     'name'
#     'medium_url
#   ]

def get_pins (board = "NONE"):
  payload = {
    'access_token': 'MTQzMTU5NDoxMTcwOTM3OTY0NzAwNjMxMDU6MnwxMzY3MTc3NDQ1OjAtLWMxZjliNGFjOTk0YzRmYWI1OTk4NjFmOTRmYzIxYzBhYTVlOGY1Mjk=',
    'add_fields': 'pin.dominant_color(),pin.like_count(),pin.link()'
  }

  r = requests.get(request_pins(board), params = payload)

  all_pins = []
  get_pins = True
  # store information for each pin
  while (get_pins):
    rjson = r.json()
    for pin in rjson['data']:
      for field in pin_fields:
        if (field == 'created_at'):
          t = pin["created_at"] # format like "Sat, 15 Feb 2014 22:17:17 +0000"
          # creates a struct_time: http://docs.python.org/2/library/time.html#time.struct_time
          time = datetime.strptime(t[:-6], '%a, %d %b %Y %H:%M:%S') # format string: http://docs.python.org/2/library/time.html#time.strftime
          pin_dict = {}
          pin_dict['created_at'] = time
        else:
          f = pin[field]
          if isinstance(f, str):
            f = f.encode('utf-8')
          pin_dict[field] = f
      if pin_dict['dominant_color']:
        all_pins.append(pin_dict)
      # print pin['description']
    # get bookmark
    if rjson.get('bookmark', []):
      bookmark = rjson['bookmark']
      bookmark_payload = payload
      bookmark_payload['bookmark'] = rjson['bookmark']
      r = requests.get(request_pins(board), params = bookmark_payload)
      # print "bookmark"
    else:
      # print "no bookmark"
      get_pins = False
  return all_pins

if __name__ == '__main__':
  # get_boards()
  # all_pins = get_pins(design_board)

  # FOR GETTING ALL PINS

  all_pins = get_pins()
  with open('allpins-color.csv', 'wb') as f:
    dict_writer = csv.DictWriter(f, pin_fields)
    dict_writer.writer.writerow(pin_fields)
    dict_writer.writerows(all_pins)

  # 