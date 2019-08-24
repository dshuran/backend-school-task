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
    def test_patch_request(self):
        import_id = 1
        citizen_id = 1
        self.requests_tester(welcome_message='PATCH REQUEST TESTS',
                             request_dirname='patch_requests', command='PATCH',
                             request_url='/imports/' + str(import_id) + '/citizens/' + str(citizen_id))

    def test_post_request(self):
        self.requests_tester(welcome_message='POST REQUEST TESTS',
                             request_dirname='post_requests', command='POST', request_url='/imports')

    def request_sender(self, path, input_file_name, output_file_name, command, request_url):
        input_dirname = 'input'
        full_filename = os.path.join(path, input_dirname, input_file_name)
        print('testing ', full_filename)
        with open(full_filename, 'r') as input_file:
            data = json.load(input_file)
        headers = {'content-type': 'application/json'}
        if command == 'POST':
            response = requests.post(server_url + request_url, data=json.dumps(data), headers=headers)
        elif command == 'PATCH':
            response = requests.patch(server_url + request_url, data=json.dumps(data), headers=headers)
        # Тесты
        self.assertEqual(response.ok, True)
        parsed_json = json.loads(response.text)
        output_dirname = 'output'
        with open(os.path.join(path, output_dirname, output_file_name), 'w') as output_file:
            json.dump(parsed_json, output_file)

    def requests_tester(self, welcome_message, request_dirname, command, request_url):
        print(welcome_message)
        counter = 1
        path = os.path.dirname(os.path.abspath(__file__))
        post_dir = os.path.join(path, request_dirname)
        for input_file in os.listdir(os.path.join(post_dir, 'input')):
            if input_file.endswith(".txt"):
                output_file = "result" + str(counter) + ".txt"
                self.request_sender(path=post_dir, input_file_name=input_file,
                                    output_file_name=output_file, command=command, request_url=request_url)
                counter += 1
            else:
                continue


def main():
    unittest.main()


if __name__ == '__main__':
    main()
