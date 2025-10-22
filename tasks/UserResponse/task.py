[sys.path.append(os.path.join(os.getcwd(), folder)) for folder in variables.get("dependent_modules_folders").split(",")]
import proactive_helper as ph
import json
import random

class UserResponse:
    def __init__(self):
        # Hardcoded response configuration
        self.accept_string = "accept"
        self.reject_string = "reject"
        self.case_sensitive = False
        self.default_response = "accept"

    def check_user_response(self, user_response: str) -> bool:
        resp = user_response if self.case_sensitive else user_response.lower()
        accept = self.accept_string if self.case_sensitive else self.accept_string.lower()
        reject = self.reject_string if self.case_sensitive else self.reject_string.lower()

        if resp == accept:
            return True
        if resp == reject:
            return False
        if self.default_response == "accept":
            return True
        if self.default_response == "reject":
            return False
        return False

    def process_selected_users(self, selected_users_json: str) -> list:
        """
        Process selected users and simulate their responses.
        Returns users who accepted the alert.
        Hardcoded: 80% acceptance rate for simulation.
        """
        try:
            selected_users = json.loads(selected_users_json)
            accepted_users = []
            
            for user in selected_users:
                # Simulate user response (80% acceptance rate - hardcoded)
                accepted = random.random() < 0.8
                
                if accepted:
                    user_with_response = user.copy()
                    user_with_response['accepted'] = True
                    accepted_users.append(user_with_response)
            
            return accepted_users
        except Exception as e:
            print(f"Error processing selected users: {e}")
            return []

if __name__ == '__main__':
    # Get selected users from SelectUsers task
    selected_users_json = variables.get("SELECTED_USERS")
    
    if selected_users_json:
        print(f"Received selected users: {selected_users_json}")
        
        manager = UserResponse()
        accepted_users = manager.process_selected_users(selected_users_json)
        
        print(f"Users who accepted: {len(accepted_users)}")
        print(f"Accepted users: {accepted_users}")
        
        resultMap.put("USER_RESPONSE_ACCEPTED", json.dumps(accepted_users))
    else:
        print("No selected users received from SelectUsers task")
        resultMap.put("USER_RESPONSE_ACCEPTED", json.dumps([]))