import requests
import json

def call_frame(text):
      targetURL = "http://143.248.135.188:1107/frameBERT"
      headers = {'Content-Type': 'application/json; charset=utf-8'}
      requestJson = {
            "text": text
      }
      response = requests.post(targetURL, data=json.dumps(requestJson), headers=headers)
      print("[FRAME responseCode] " + str(response.status_code))
      # print(response.json())
      return response.json()


def call_l2k(text):
      targetURL = "http://wisekb.kaist.ac.kr:2451/open-api"
      headers = {'Content-Type': 'application/json; charset=utf-8'}
      requestJson = {
            "text": text
      }
      response = requests.post(targetURL, data=json.dumps(requestJson), headers=headers)
      print("[L2K responseCode] " + str(response.status_code))
      # print(response.json())
      return response.json()

# text = "헤밍웨이는 1899년 7월 21일 미국 일리노이에서 태어났고, 62세에 미국 아이다호에서 자살로 사망했다."
# call_frame(text)
# call_l2k(text)