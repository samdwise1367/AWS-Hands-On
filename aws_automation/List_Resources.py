#Author: Samson oni(soni5@umbc.edu, www.samdwise.com)
import boto3

class view_resources:
    def __init__(self):
        print('\n================Following are Launch configurations available(if any):==========================\n')
        print(self.get_launch_configurations())
        print('\n================Following are Autoscaling group available(if any):==========================\n')
        print(self.get_auto_scaling_groups())
        print('\n================Following are Load balancers available(if any):==========================\n')
        print(self.get_load_balancers())
        print('\n================Following are Elastic clusters available(if any):==========================\n')
        print(self.get_elastic_cluster())
############################################################################
    def boto_session(self,service):
        session = boto3.Session()
        return session.client(service)

###########################################################################
    """List all Launch configurations"""
    def get_launch_configurations(self):
        client = self.boto_session("autoscaling")
        return client.describe_launch_configurations()

###########################################################################
    """List all Autoscaling gropus"""
    def get_auto_scaling_groups(self):
        """List info about all auto scaling groups."""
        client = self.boto_session("autoscaling")
        return client.describe_auto_scaling_groups()
###########################################################################

    """List all load balancers"""
    def get_load_balancers(self):
        client = self.boto_session("elb")
        return client.describe_load_balancers()

################################################################################

    """List all elastic clusters available"""
    def get_elastic_cluster(self):
        client    = self.boto_session('elasticache')
        return client.describe_cache_clusters()
################################################################################
"""Invoke listing functions"""
get_list = view_resources()
