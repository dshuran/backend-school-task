import unittest
import requests
import json

server_url = 'http://localhost:5000'


# Второй запрос из задания
class TestGETCitizensRequest(unittest.TestCase):

    """
     def test_get_citizens_request(self):
        response = requests.get(server_url + '/imports/1/citizens')
        parsed_json = json.loads(response.text)
        with open('get_citizens_request_result.txt', 'w') as outfile:
            json.dump(parsed_json, outfile)
    """

    def test_post_request(self):
        with open('post_request.txt', 'r') as input_file:
            data = json.load(input_file)
        headers = {'content-type': 'application/json'}
        print(data)
        response = requests.post(server_url + '/imports', data=json.dumps(data), headers=headers)
        print(response.text)
        self.assertEqual(response.ok, True)
        parsed_json = json.loads(response.text)

        with open('post_request_result.txt', 'w') as outfile:
            json.dump(parsed_json, outfile)


if __name__ == '__main__':
    unittest.main()
