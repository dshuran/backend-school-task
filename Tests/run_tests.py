import unittest
import requests
import json
import os

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

    def send_post_request(self, path, input_dirname, input_file_name, output_file_name):
        print('testing ', os.path.join(path, input_dirname, input_file_name))
        with open(os.path.join(path, input_dirname, input_file_name), 'r') as input_file:
            data = json.load(input_file)
        headers = {'content-type': 'application/json'}
        response = requests.post(server_url + '/imports', data=json.dumps(data), headers=headers)
        # Тесты
        self.assertEqual(response.ok, True)
        parsed_json = json.loads(response.text)
        output_dirname = 'output'
        with open(os.path.join(path, output_dirname, output_file_name), 'w') as output_file:
            json.dump(parsed_json, output_file)

    def test_post_request(self):
        print('POST TESTS (1)')
        counter = 1
        path = os.path.dirname(os.path.abspath(__file__))
        post_dir = os.path.join(path, 'post_requests')
        for input_file in os.listdir(os.path.join(post_dir, 'input')):
            if input_file.endswith(".txt"):
                output_file = "post_result" + str(counter) + ".txt"
                self.send_post_request(post_dir, 'input', input_file, output_file)
                counter += 1
            else:
                continue



    def request_sender(self, path, input_dirname, input_file_name, output_file_name, command, request_url):
        with open(os.path.join(path, input_dirname, input_file_name), 'r') as input_file:
            data = json.load(input_file)
        headers = {'content-type': 'application/json'}
        if command == 'POST':
            response = requests.post(server_url + '/imports', data=json.dumps(data), headers=headers)
        elif command == 'PATCH':

        # Тесты
        self.assertEqual(response.ok, True)
        parsed_json = json.loads(response.text)
        output_dirname = 'output'
        with open(os.path.join(path, output_dirname, output_file_name), 'w') as output_file:
            json.dump(parsed_json, output_file)

    def requests_tester(self, welcome_message, request_dirname, ):
        print(welcome_message)
        counter = 1
        path = os.path.dirname(os.path.abspath(__file__))
        post_dir = os.path.join(path, request_dirname)
        for input_file in os.listdir(os.path.join(post_dir, 'input')):
            if input_file.endswith(".txt"):
                output_file = "result" + str(counter) + ".txt"
                self.send_post_request(post_dir, 'input', input_file, output_file)
                counter += 1
            else:
                continue



def main():
    unittest.main()


if __name__ == '__main__':
    main()
