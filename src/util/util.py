import pickle
import socket
import re
from os import environ

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5555
moodle_words = { 'opens': 'se abre', 'closes': 'se cierra' }


def create_server_socket(unserialized_data, host=SOCKET_HOST, port=SOCKET_PORT):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    data = pickle.dumps(unserialized_data)
    while True:
        server_socket.listen()
        client_socket, _ = server_socket.accept()
        client_socket.send(data)


def get_data_from_server(host=SOCKET_HOST, port=SOCKET_PORT):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    webservice_data = client_socket.recv(4096)
    client_socket.close()
    return pickle.loads(webservice_data)


def convert_events_to_readable_text(events):
    events_info = []
    for event in events:
        date = re.sub('<.*?>', '', event['formattedtime'])
        events_info.append(date + ' ' + event['name'])
    return events_info


def text_to_speech(string_array):
    text = ''
    for string in string_array:
        text = text + string + '.\n'
    return translate_moodle_words(text)


def translate_moodle_words(string):
    if environ['lang'] == 'es-es':
        for k, v in moodle_words.items():
            string = re.sub(k, v, string)
    return string

def get_course_id_by_name(course_to_find, user_courses):
    for course_id, name in user_courses:
        if course_to_find.upper() in name:
            return str(course_id)
    return None
