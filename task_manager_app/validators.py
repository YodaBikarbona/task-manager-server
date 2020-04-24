class Validation:

    @staticmethod
    def login_validation(data):
        try:
            str(data['username'])
            str(data['password'])
            return True
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    def edit_task(data):
        try:
            str(data['title'])
            int(data['percent'])
            int(data['estimate'])
            int(data['priority_id'])
            int(data['tracker_roadmap'])
            int(data['department_id'])
            int(data['role_id'])
            int(data['assigned_to'])
            str(data['content'])
            str(data['start_date'])
            str(data['end_date'])
            return True
        except Exception as ex:
            print(ex)
            return False
