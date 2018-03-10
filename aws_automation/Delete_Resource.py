#Author: Samson oni(soni5@umbc.edu, www.samdwise.com)
import boto3
import configparser

class DeleteResource:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')
        self.autoscaling_name = config['AutoScalingGroup']['Name']
        self.elb_name = config['ELB']['Name']
        self.launch_config_name = config['LaunchConfiguration']['Name']
        self.elastic_name = config['Redis']['Name']
##############################################################################

    '''Below function is to create client session that will be used for all needed services'''
    def boto_session(self, resource):
        client_session = boto3.Session()
        return client_session.client(resource)
############################################################################

    """Detach load balacer from autoscaling group"""
    def detach_load_balacer_from_autoscaling(self):
        attach_client = self.boto_session('autoscaling')
        parameters = {}
        parameters['AutoScalingGroupName'] = self.autoscaling_name
        parameters['LoadBalancerNames'] = [self.elb_name]
        return attach_client.detach_load_balancers(**parameters)

###########################################################################
    """Delete a load balancer."""
    def delete_elastic_load_balancer(self):
        client = self.boto_session("elb")
        parameters = {}
        parameters["LoadBalancerName"] = self.elb_name
        return client.delete_load_balancer(**parameters)

###########################################################################
    """Delete autoscaling group"""
    def delete_auto_scaling_group(self):
        client = self.boto_session("autoscaling")
        force_delete = True
        parameters = {}
        parameters["AutoScalingGroupName"] = self.autoscaling_name
        parameters["ForceDelete"] = force_delete
        return client.delete_auto_scaling_group(**parameters)
###########################################################################

    """Delete Launch configuration"""
    def delete_launch_configuration(self):
        client = self.boto_session("autoscaling")
        parameters = {}
        parameters["LaunchConfigurationName"] = self.launch_config_name
        return client.delete_launch_configuration(**parameters)
#######################################################################

    def delete_elastic_cluster(self):
        client = self.boto_session("elasticache")
        parameters={}
        parameters["CacheClusterId"] = self.elastic_name
        return client.delete_cache_cluster(**parameters)
##########################################################################
try:
    """Invoking the delete funstions"""

    deleteObject  = DeleteResource()
    print('\n=============Detaching load balancer from autoscaling group=============================\n')
    print(deleteObject.detach_load_balacer_from_autoscaling())
    print('\n=============Deleting Elastic Load balancer=============================\n')
    print(deleteObject.delete_elastic_load_balancer())
    print('\n=============Deleting auto scaling group=============================\n')
    print(deleteObject.delete_auto_scaling_group())
    print('\n=============Deleting lauch configuration=============================\n')
    print(deleteObject.delete_launch_configuration())
    print('\n=============Deleting elastic cache=============================\n')
    print(deleteObject.delete_elastic_cluster())
except Exception as error:
    print(error)


