import json
import os
import unittest

import requests

# todo: изменить url, если изменится хост/порт
server_url = 'http://localhost:8080'


class TestGETCitizensRequest(unittest.TestCase):

    def do_get_full_request(self, import_id):
        self.requests_tester(welcome_message='GET FULL REQUEST TESTS',
                             request_dirname='get_full_requests', command='GET', request_url='/imports/' + str(import_id) + '/citizens')

    def do_get_presents_request(self, import_id):
        self.requests_tester(welcome_message='GET PRESENTS REQUEST TESTS',
                             request_dirname='get_presents_requests', command='GET',
                             request_url='/imports/' + str(import_id) + '/citizens/birthdays')

    def do_get_percentiles_request(self, import_id):
        self.requests_tester(welcome_message='GET PERCENTILES REQUEST TESTS',
                             request_dirname='get_percentiles_requests', command='GET',
                             request_url='/imports/' + str(import_id) + '/towns/stat/percentile/age')

    def do_patch_request(self, import_id):
        citizen_id = 1
        self.requests_tester(welcome_message='PATCH REQUEST TESTS',
                             request_dirname='patch_requests', command='PATCH',
                             request_url='/imports/' + str(import_id) + '/citizens/' + str(citizen_id))

    def do_post_requests(self):
        self.requests_tester(welcome_message='POST REQUEST TESTS',
                             request_dirname='post_requests', command='POST', request_url='/imports')

    def test_requests(self):
        min_id = 1
        max_id = 2
        # Проходит по всем файлам в директории
        self.do_post_requests()
        # Запускает тесты только по определённым выгрузкам.
        for cit_id in range(min_id, max_id + 1):
            self.do_patch_request(cit_id)
            self.do_get_full_request(cit_id)
            self.do_get_percentiles_request(cit_id)
            self.do_get_presents_request(cit_id)

    def request_sender(self, path, input_file_name, output_file_name, command, request_url, good_request=True):
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
        elif command == 'GET':
            response = requests.get(server_url + request_url, data=json.dumps(data), headers=headers)
        else:
            assert False
        # Тесты
        if good_request:
            self.assertEqual(response.ok, True)
        else:
            self.assertEqual(response.ok, False)
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
