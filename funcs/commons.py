from os.path import join as join_path
import notice
import json

def formatted_state(state_msgs, target_group, target_state):
    return state_msgs["status"][target_state].format(state_msgs["group"][target_group])

def assert_referable(dict, ref, cause, *args):
    if not ref in dict:
        try:
            dict[ref] = cause(*args)
        except KeyError as AssignFailure:
            raise AssignFailure
    return dict[ref]

async def grab_data(data_path, data_file):
    try:
        data_file = open(join_path(data_path, "data", "auth", data_file), "r")
        data_buff = data_file.read()
        data_file.close()
        return json.loads(data_buff)
    except:
        notice.gen_ntc(
            'critical', 'title',
            "".join([
                "Critical failure in loading data file '",
                data_file,
                "'. Have the folders been organized as 'data/auth'?"
            ])
        )
        raise FileNotFoundError