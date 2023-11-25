from testu import *

def get_recent_problems(dim, filled_information):
    for name,info in filled_information.items():
            if(name == 'PROBLEMS'):
                answer=[]
                problems = []
                dates = []
                # remove the first empty bracket
                problems_rows = filled_information['PROBLEMS']['Table Rows']
                problems_rows.pop(0)
                for row in problems_rows:
                    if(row[2] != ''):
                        problems.append(row[0].split(",")[0])
                        dates.append(row[2])
                match dim:
                    case 1:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
                    case 2:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
                    case 5:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
            else:
                pass
    return False
print(get_recent_problems(1,filled_information))