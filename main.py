import heapq
from typing import NamedTuple, List
from datetime import datetime
import json


class NotFoundAthletesInfo(Exception):
    """ An exception occurs when there is no personal data for the athletes in the json file """


class NoCorrectDateString(Exception):
    """ An exception occurs when the string date object contains an incorrect character """

class Participant(NamedTuple):
    """ Stores the participant's personal information """
    
    first_name :str = None
    last_name :str = None

class ResultRun(NamedTuple):
    """ Stores the results of the participant's race """
    
    number :int = None
    time :datetime =None
    participant :Participant = None
    

def create_participant_object(participant_json_data :dict) -> Participant:
    """ Creates an object with participant data """
    
    return Participant(first_name=participant_json_data.get("Name", ""),
                       last_name= participant_json_data.get("Surname", ""))
    

def fill_heap(path_results_athletes :str, path_info_athletes :str) -> list:
    """ The method fills the heap list with 
        the results of the participant 
    """
    
    heap = []
    
    with open(path_info_athletes) as comp_file:
        personal_info_athletes_dict :dict = json.load(comp_file)
    
    with open(path_results_athletes) as result_file:
        
        tmp_time :datetime = None
        
        for line in result_file:
            
            number, _, time_str = line.split(" ")
            try:
                time :datetime = datetime.strptime(time_str.strip(), "%H:%M:%S,%f")
            except:
                raise NoCorrectDateString(f"""The format of the string date about 
                                          the participant number {number} contains incorrect characters""")
            if tmp_time is None:
                tmp_time = time
                continue 
            
            participant_json_data :dict = personal_info_athletes_dict.get(number)
            if not participant_json_data:
                raise NotFoundAthletesInfo(f"""There is no information about the participant under 
                                              the number in the personal data file {number} """)
            participant :Participant = create_participant_object(participant_json_data)
            result_run = ResultRun(number=number, 
                                   time=time-tmp_time, 
                                   participant=participant)
            heapq.heappush(heap, (result_run.time, result_run))
            tmp_time = None
            
    return heap

def print_result_participants(headers :List[str], heap :list):
    """ Prints the results of the participants to the console """
    
    result_data = []
    i = 0 
    while heap:
        i+=1
        time, result_run = heapq.heappop(heap)
        result_data.append((i, result_run.number,result_run.participant.first_name, result_run.participant.last_name, time) )
    
    print('\n')
    print_pretty_table([headers, *result_data])
    
def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    """ Formatted output """
    
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [str(data[row][col]) for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    separator = "-+-".join('-' * n for n in col_width)

    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            print(separator)

        result = []
        for col in range(cols):
            item = str(data[row][col]).rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))

def main():
    
    try:
        heap :list = fill_heap("results_RUN.txt", "competitors2.json")
        print_result_participants(["Занятое место", "Нагрудный номер", "Имя", "Фамилия", "Результат"], heap)
    except NotFoundAthletesInfo as e:
        print(e)
    except NoCorrectDateString as e:
        print(e)
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main()