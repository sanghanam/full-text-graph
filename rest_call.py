import requests
import json
import socket
import json

def call_frame(text):
      targetURL = "http://143.248.135.188:1107/frameBERT"
      headers = {'Content-Type': 'application/json; charset=utf-8'}
      requestJson = {
          "text": text,
          "result_format": "textae"
      }
      response = requests.post(targetURL, data=json.dumps(requestJson), headers=headers)
      print("[FRAME responseCode] " + str(response.status_code))
      # print(response.json())
      return response.json()


def call_surface(text):
    targetURL = "http://wisekb.kaist.ac.kr:47361/surface-parser"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requestJson = {
        "text": text
    }
    response = requests.post(targetURL, data=json.dumps(requestJson), headers=headers)
    print("[SURFACE responseCode] " + str(response.status_code))
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

def getETRI(text):
    if text == "":
        print("ETRI input with blank string")
        return None
    host = '143.248.135.146'
    port = 44444
    ADDR = (host, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
    except KeyboardInterrupt:
        return None
    except Exception:
        print("ETRI connection failed")
        return None
    try:
        clientSocket.sendall(str.encode(text))
        buffer = bytearray()
        while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            buffer.extend(data)
        result = json.loads(buffer.decode(encoding='utf-8'))

        return result
    except KeyboardInterrupt:
        return None
    except Exception:
        print("ETRI connection lost")
        return None
    finally:
        clientSocket.close()


# text = "헤밍웨이는 1899년 7월 21일 미국 일리노이에서 태어났고, 62세에 미국 아이다호에서 자살로 사망했다."
# call_frame(text)
# call_l2k(text)