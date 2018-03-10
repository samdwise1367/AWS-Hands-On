Author: Samson Oni(soni5@umbc.edu)
Language: Python

Instructions:
1. The solution was written in python3. Major module used is Boto3.
2, Prerequisite for using this solution are creating a programmable user on aws console management,give the user programmable access and full access to services needed like ECS, Elasticache, setting up aws cli configuration on your linux machine.
3. THe solution contains 4 files namely:
- Create_Resource.py - This script is for creating all resources stated in the question.
- configuration.ini - THis is a configuration file, here a user just set parameters needed to run the script. THis file will help when we want to add more functions and make our code clean.
- List_Resource.py - This script is used to query aws to describe those serves we created and other services there.
- Delete_Resource.py - This script is used to delete all the services that was created with Create_Resource.py.

Note: Kindly pay attention to the region you are using, especially when you are creating, copy ami_id from the region you decide to use and be consistent with it.

